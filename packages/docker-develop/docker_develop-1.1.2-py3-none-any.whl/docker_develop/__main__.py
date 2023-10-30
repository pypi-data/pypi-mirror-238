#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

__author__ = "Tomasz Bogdal, Michal Gora"
__copyright__ = "Copyright 2023, Cledar"
__credits__ = ["Tomasz Bogdal", "Michal Gora"]

__license__ = "MPL 2.0"
__version__ = "1.1.2"
__maintainer__ = "Tomasz Bogdal"

__email__ = "tomek@cledar.com"
__status__ = "Production"

import argparse
import hashlib
import os
import signal
import sys
import re
import zlib

from argparse import ArgumentParser
from collections import Counter
from collections import namedtuple
from datetime import datetime
from functools import reduce
from glob import glob
from itertools import chain
from shutil import rmtree
from subprocess import Popen, PIPE
from zipfile import ZipFile

import logging
from logging import debug, info, warning, error

try:
    import cpickle as pickle
except ImportError:
    import pickle

try:
    from yaml import load, dump
except ImportError:
    print('Missing required PyYAML, please install with:')
    print()
    print('   pip install pyyaml')
    sys.exit(1)

try:
    from yaml import CLoader as Loader, CDumper as Dumper, CFullLoaded as FullLoader
except ImportError:
    from yaml import Loader, Dumper, FullLoader

if os.system('docker compose version 2>&1 > /dev/null') > 0:
    if os.system('docker-compose version 2>&1 > /dev/null') > 0:
        print('Missing docker-compose or docker compose, please install...')
        sys.exit(1)
    else:
        DOCKER_COMPOSE_VERSION = 1
else:
    DOCKER_COMPOSE_VERSION = 2


class RepositoryGroup:
    selector = None
    regex = None

    def __init__(self, selector='*', regex=None):
        self.selector = selector
        self.regex = regex


BASE_ROOT_RPATH = '../'

PROJECT_NAME = 'develop'

BASE_DOCKER_COMPOSE = 'docker-compose.yml'

DEVELOP_DIR = "develop"
VAULT_FILENAME = 'vault.zip'

PROJECT_DOCKER_COMPOSE = 'docker-compose.dev.yml'
PROJECT_DOCKERFILE = 'Dockerfile_local'
PROJECT_DOCKER_COMPOSE_OVERRIDE_GLOB = 'docker-compose.dev.*.yml'
PROJECT_OVERRIDE_NAME_REGEX = re.compile('docker-compose\\.dev\\.(.*)\\.yml')
PROJECT_OVERRIDE_NAME = 'docker-compose.dev.{override_name}.yml'

AUXILIARY_DOCKER_COMPOSE_GLOB = 'docker-compose.*.yml'
AUXILIARY_DOCKER_COMPOSE_OVERRIDE_GLOB = 'docker-compose.aux.{auxiliary_name}.dev.*.yml'
AUXILIARY_OVERRIDE_NAME_REGEX = 'docker-compose\\.aux\\.{auxiliary_name}\\.dev\\.(.*)\\.yml'
AUXILIARY_NAME_REGEX = re.compile('docker-compose\\.aux\\.([a-zA-Z-_]*)\\.yml')

PORTS_PRINT_SERVICE_REGEX = re.compile('.*-(api|ui)$')

SHELL_PROFILES = ['.zshrc', '.bashrc', '.bash_profile']

DockerComposeProject = namedtuple(
        'DockerComposeProject', 'name base_path docker_path overrides')
DockerComposeOverride = namedtuple(
        'DockerComposeProjectOverride', 'name project base_path docker_path')
DockerComposeAuxiliary = namedtuple(
        'DockerComposeAuxiliary', 'name base_path docker_path overrides')

State = namedtuple('State', 'base_path project_name selected')
Configs = namedtuple('Configs', 'projects auxiliaries')
DockerConfig = namedtuple('DockerConfig', 'parsed yaml profiles')

CONFIG_NAME = 'docker-develop.yml'
CONFIG_DIR = DEVELOP_DIR


class Config:
    base_dir = None

    config_dir = None
    config_path = None

    search_paths = None
    repository_groups = None

    @property
    def base_name(self):
        return os.path.basename(self.base_dir) if self.base_dir else PROJECT_NAME

    @classmethod
    def exists(cls, base_path, config_name=CONFIG_NAME):
        return os.path.isfile(cls.resolve(base_path, config_name))

    @staticmethod
    def resolve(base_path, config_name=CONFIG_NAME):
        return os.path.abspath(os.path.join(base_path, CONFIG_DIR, config_name))

    @staticmethod
    def walk_path(path):
        new_path = os.path.abspath(os.path.join(path, '..'))
        return None if new_path == path else new_path

    def load(self, config_path):
        if not self.exists(config_path):
            return
        self._load(config_path)

    def find_and_load(self, path, config_name=CONFIG_NAME):
        current_path = path

        while current_path is not None:
            config_path = self.resolve(current_path, config_name)
            if os.path.isfile(config_path):
                return self._load(config_path)
            else:
                current_path = self.walk_path(current_path)
        else:
            raise RuntimeError("Could not find any configurations, aborting...")

    def _load(self, config_path):
        with open(config_path, 'r') as config_file:
            raw_config = load(config_file, Loader=FullLoader) or {}

            self.config_path = config_path
            self.config_dir = os.path.dirname(config_path)

            self.base_dir = os.path.dirname(self.config_dir)

            self._parse(raw_config)

    def _parse(self, raw_config):
        self._parse_search_paths(raw_config)
        self._parse_repository_groups(raw_config)

    def _parse_search_paths(self, raw_config):
        if 'search-paths' in raw_config and raw_config['search-paths']:
            self.search_paths = []
            for search_path in raw_config['search-paths']:
                full_path = os.path.abspath(os.path.join(self.config_dir, search_path))
                if os.path.isdir(full_path):
                    self.search_paths.append(full_path)

    def _parse_repository_groups(self, raw_config):
        if 'repository-groups' in raw_config and raw_config['repository-groups']:
            self.repository_groups = {}
            for group in raw_config['repository-groups']:
                group_data = raw_config['repository-groups'][group]
                self.repository_groups[group] = RepositoryGroup(
                        selector=group_data['selector'] if 'selector' in group_data else None,
                        regex=group_data['regex'] if 'regex' in group_data else None)


class CmdUtility:

    def __init__(self, command_types):
        self.command_types = command_types

    def main(self, base_path):
        args, rest_args, commands = self.init(base_path)

        return self.dispatcher(commands, args, rest_args)

    def init(self, base_path):
        self._pre_init(base_path)

        commands = [self._init_command(command_type) for command_type in self.command_types]
        args, rest_args = self._parse_command_args(commands)

        self._post_init(args, rest_args)

        return args, rest_args, commands

    def dispatcher(self, commands, args, rest_args):
        if not args.command:
            self._dispatch_no_command(args, rest_args)
        else:
            self._dispatcher(commands, args, rest_args)

    def _dispatcher(self, commands, args, rest_args):
        for command in commands:
            if args.command == command.NAME or args.command in command.ALIASES:
                return self._dispatch_command(command, args, rest_args)
        raise NotImplementedError(f'{args.command} command is not supported.')

    def _dispatch_command(self, command, args, rest_args):
        return command.dispatch(args, rest_args)

    def _dispatch_no_command(self, args, rest_args):
        pass

    def _pre_init(self, base_path):
        pass

    def _post_init(self, args, rest_args):
        pass

    def _init_command(self, command_type):
        return command_type.from_init()

    def _parse_command_args(self, commands):
        parser = argparse.ArgumentParser()

        self._register_args(parser)

        # noinspection PyTypeChecker
        subparsers = parser.add_subparsers(title=None, dest='command', metavar='COMMAND')

        for command in commands or []:
            subparser = subparsers.add_parser(command.NAME,
                                              help=command.DESCRIPTION,
                                              add_help=command.HELP,
                                              aliases=command.ALIASES)
            command.register_command_args(subparser)

        return parser.parse_known_args()

    def _register_args(self, parser: ArgumentParser):
        raise NotImplementedError()


class CmdUtilityCommand:
    HELP = True
    NAME = ''
    DESCRIPTION = ''
    ALIASES = []

    def __init__(self, *args, **kwargs):
        pass

    def register_command_args(self, parser: ArgumentParser):
        raise NotImplementedError(f'{self.NAME} command not implemented')

    def dispatch(self, *args, **kwargs):
        raise NotImplementedError(f'{self.NAME} command not implemented')

    @classmethod
    def from_init(cls, *args, **kwargs):
        return cls(*args, **kwargs)


class DockerDevelop(CmdUtility):

    def __init__(self):
        self._commands = [
            InitCommand,
            VaultCommand,

            ListCommand,
            SelectCommand,
            EnableCommand,
            DisableCommand,
            ResetCommand,
            ServicesCommand,

            PortsCommand,
            EachCommand,

            ComposeCommand,
            ConfigCommand,
            StatusCommand,
            LogsCommand,
            UpCommand,
            DownCommand,
            BuildCommand,
            RebuildCommand,
            RestartCommand,
        ]
        super().__init__(self._commands)

        self.config = None
        self.state = None
        self.detected_configs = None

    def _pre_init(self, base_path):
        self.config = self.load_config(base_path)

    def _init_command(self, command_type):
        return command_type.from_init(self.config)

    def _post_init(self, args, rest_args):
        init_logging(args)
        debug((args, rest_args))

        self.state = state_load(args, self.config)
        self.detected_configs = detect_configs(args)

        if args.install:
            install_command()
        if args.version:
            version_command()

    def _dispatch_no_command(self, args, rest_args):
        print_configurations(self.state, self.detected_configs, selected=True)

    def _dispatch_command(self, command, args, rest_args):
        return command.dispatch(args, rest_args, self.state, self.detected_configs)

    def _register_args(self, parser: ArgumentParser):
        search_paths = ', '.join(self.config.search_paths)
        parser.add_argument('-v', '--verbosity',
                            action='count',
                            default=0,
                            help=f'increase verbosity of output')
        parser.add_argument('--install',
                            action="store_true",
                            help='Install docker-develop on the shell PATH.'
                            )
        parser.add_argument('-c', '--config-dir',
                            default=self.config.config_dir,
                            help=f'base configuration directory (defaults to {self.config.config_dir})')
        parser.add_argument('-s', '--search-path',
                            nargs='*',
                            default=self.config.search_paths,
                            help=f'search path for detecting configurations (defaults to {search_paths})')
        parser.add_argument('--version',
                            default=False,
                            action="store_true",
                            help="Print current version.")

    @classmethod
    def load_config(cls, base_path):
        config = Config()
        try:
            config.find_and_load(base_path)
        except RuntimeError as e:
            print(e)
            exit(1)
        return config


class DockerDevelopCommand(CmdUtilityCommand):

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def register_command_args(self, parser: ArgumentParser):
        pass

    def dispatch(self, args, rest_args, state, detected_configs):
        raise NotImplementedError(f'docker-develop {self.NAME} command not implemented')

    @classmethod
    def from_init(cls, config, *args, **kwargs):
        return cls(config)


class InitCommand(DockerDevelopCommand):
    HELP = True
    NAME = 'init'
    DESCRIPTION = 'Initialize a docker-develop configuration'

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('-f', '--force',
                            default=False,
                            action="store_true",
                            help="Force overwriting of existing configuration files")
        parser.add_argument("-o", '--with-override-for',
                            type=str,
                            nargs='*',
                            help="List of Configuration Names to generate overrides for")

    # noinspection PyTypeChecker
    def dispatch(self, args, rest_args, state, detected_configs):
        init_command(state, detected_configs, args)


class ComposeCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'compose'
    DESCRIPTION = ''

    def dispatch(self, args, rest_args, state, detected_configs):
        compose_command(state, detected_configs, rest_args)


class VaultCommand(DockerDevelopCommand):
    HELP = True
    NAME = 'vault'
    DESCRIPTION = 'Manage vault of secrets'

    def register_command_args(self, parser: ArgumentParser):
        # noinspection PyTypeChecker
        vault_subparsers = parser.add_subparsers(title=None,
                                                 dest='vault_command',
                                                 metavar='VAULT_COMMAND')

        vault_create_parser = vault_subparsers.add_parser('create',
                                                          help='Create vault')
        vault_create_parser.add_argument('vault_file',
                                         type=str,
                                         nargs='*',
                                         help="Files to be added to vault")
        _vault_diff_parser = vault_subparsers.add_parser('diff',
                                                         help='Diff vault with filesystem')
        vault_extract_parser = vault_subparsers.add_parser('extract',
                                                           help='Extract vault to filesystem')
        vault_extract_parser.add_argument('-f', '--force',
                                          action="store_true",
                                          default=False,
                                          help="Force operation.")
        vault_status_parser = vault_subparsers.add_parser('status',
                                                          help='Status of vault vs filesystem')
        vault_status_parser.add_argument('vault_file',
                                         type=str,
                                         nargs='*',
                                         help="Files to be added to vault")
        vault_update_parser = vault_subparsers.add_parser('update',
                                                          help='Update vault from filesystem, and optionally add new'
                                                               'items to vault')

        vault_update_parser.add_argument('vault_file',
                                         type=str,
                                         nargs='*',
                                         help="Files to be added to vault")
        vault_update_parser.add_argument('-f', '--force',
                                         action="store_true",
                                         default=False,
                                         help="Force operation.")

    # noinspection PyTypeChecker
    def dispatch(self, args, rest_args, state, detected_configs):
        vault_command(state, detected_configs, args)


class PortsCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'ports'
    DESCRIPTION = 'List ports of services'

    def dispatch(self, state, detected_configs, args, rest_args):
        ports_command(state, detected_configs)


class EachCommand(DockerDevelopCommand):
    HELP = True
    NAME = 'each'
    DESCRIPTION = 'Run command in each configuration directory.'

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('-g', '--group',
                            default=None,
                            dest='each_group',
                            type=str,
                            choices=self.config.repository_groups.keys() if self.config.repository_groups else None,
                            help='narrow directories by group')
        parser.add_argument('-r', '--regex',
                            default=None,
                            dest='each_regex',
                            type=str,
                            help='narrow directories using regex')

        # noinspection PyTypeChecker
        each_subparsers = parser.add_subparsers(title=None,
                                                dest='each_command')
        each_exec_parser = each_subparsers.add_parser('exec',
                                                      help='execute command')
        each_exec_parser.add_argument('-c', '--command',
                                      dest='each_exec_command',
                                      help='command to be executed')

        each_pr_parser = each_subparsers.add_parser('pr',
                                                    help='opens pull request on github; requires github'
                                                         ' cli to be installed and configured')
        each_pr_parser.add_argument('from_branch')
        each_pr_parser.add_argument('into_branch')

        _each_list_parser = each_subparsers.add_parser('list',
                                                       help='lists all repositories')

        _each_status_parser = each_subparsers.add_parser('status',
                                                         help='status for all repositories')

    # noinspection PyTypeChecker
    def dispatch(self, args, rest_args, state, detected_configs):
        each_command(state, args, self.config, rest_args)


class UpCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'up'
    DESCRIPTION = 'Start docker-compose environment'

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(
                state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'up', '--remove-orphans', '-d', *rest_args, selected=True, capture_output=False)


class DownCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'down'
    DESCRIPTION = 'Shutdown docker-compose environment.'

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(
                state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'down', '--remove-orphans', *rest_args, selected=True, capture_output=False)


class RestartCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'restart'
    DESCRIPTION = 'Restart docker-compose service.'

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(
            state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'restart', *rest_args, selected=True, capture_output=False)


class BuildCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'build'
    DESCRIPTION = 'Build docker-compose service.'

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(
            state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'build', *rest_args, selected=True, capture_output=False)


class RebuildCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'rebuild'
    DESCRIPTION = 'Build and start docker-compose service.'

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(
            state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'build', *rest_args, selected=True, capture_output=False)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'up', '--remove-orphans', '-d', *rest_args, selected=True, capture_output=False)


class StatusCommand(DockerDevelopCommand):
    NAME = 'status'
    DESCRIPTION = 'Display status of docker-compose services...'

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'ps', *rest_args, selected=True, capture_output=False)


class LogsCommand(DockerDevelopCommand):
    HELP = False
    NAME = 'logs'
    DESCRIPTION = 'Display logs of docker-compose services... '

    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(state, detected_configs, selected=True)
        docker_compose(state, detected_configs, selected_docker_config.profiles,
                       'logs', '--tail', '50', '--follow', *rest_args, selected=True, capture_output=False)


class SelectCommand(DockerDevelopCommand):
    HELP = True
    NAME = 'select'
    DESCRIPTION = 'Select a configuration (enable/disable/reset).'
    ALIASES = ['setup']

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('config_or_profile',
                            type=str,
                            nargs='*',
                            help="Configuration name or Docker Profile to be enabled")
        parser.add_argument('--reset',
                            default=False,
                            action="store_true",
                            help="Reset all previously enabled selections")
        parser.add_argument('-r', '--remove',
                            default=False,
                            action="store_true",
                            help="Remove provided Configuration names or Docker Profiles...")

    # noinspection PyUnresolvedReferences
    def dispatch(self, args, rest_args, state, detected_configs):
        selected_set = set(state.selected or [] if not args.reset else [])

        if args.remove:
            new_selection = list(selected_set.difference(set(args.config_or_profile)))
        else:
            new_selection = list(selected_set.union(set(args.config_or_profile)))

        reconfigure_command(state, detected_configs, new_selection)

        search_paths = '\n             '.join(args.search_path)
        info(f'Config Path: {args.config_dir}')
        info(f'Search Path: {search_paths}')
        info('')


class EnableCommand(DockerDevelopCommand):
    HELP = True
    NAME = 'enable'
    DESCRIPTION = 'Enable a configuration'
    ALIASES = ['add']

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('config_or_profile',
                            type=str,
                            nargs='*',
                            help="Configuration name or Docker Profile to be enabled")
        parser.add_argument('-a', '--all',
                            default=False,
                            action="store_true",
                            help="Enable all configurations.")

    # noinspection PyUnresolvedReferences
    def dispatch(self, args, rest_args, state, detected_configs):
        selected_set = set(state.selected or [])

        if args.all:
            config_names = list(detected_configs.projects.keys()) + list(detected_configs.auxiliaries.keys())
            new_selection = [config_name for config_name in config_names]
        else:
            new_selection = list(selected_set.union(set(args.config_or_profile)))

        reconfigure_command(state, detected_configs, new_selection)


class DisableCommand(DockerDevelopCommand):
    NAME = 'disable'
    DESCRIPTION = 'Disable a configuration'
    ALIASES = ['remove']

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('config_or_profile',
                            type=str,
                            nargs='*',
                            help="Configuration name or Docker Profile to be enabled")
        parser.add_argument('-a', '--all',
                            default=False,
                            action="store_true",
                            help="Disable all configurations.")

    # noinspection PyUnresolvedReferences
    def dispatch(self, args, rest_args, state, detected_configs):
        selected_set = set(state.selected or [])

        if args.all:
            new_selection = []
        else:
            new_selection = list(selected_set.difference(set(args.config_or_profile)))

        reconfigure_command(state, detected_configs, new_selection)


class ResetCommand(DockerDevelopCommand):
    NAME = 'reset'
    DESCRIPTION = 'Reset all configurations.'
    ALIASES = ['clear']

    def dispatch(self, args, rest_args, state, detected_configs):
        new_selection = []

        reconfigure_command(state, detected_configs, new_selection)


class ServicesCommand(DockerDevelopCommand):
    NAME = 'services'
    DESCRIPTION = 'Display docker-compose services and profiles.'
    ALIASES = []

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('-a', '--all',
                            default=False,
                            action="store_true",
                            help="Show all docker-compose services, not just enabled.")

    # noinspection PyUnresolvedReferences
    def dispatch(self, args, rest_args, state, detected_configs):
        detected_docker_config = docker_compose_config(state, detected_configs)
        selected_docker_config = docker_compose_config(state, detected_configs, selected=True)

        print_docker_config(detected_docker_config, selected_docker_config, selected=not args.all)


class ListCommand(DockerDevelopCommand):
    NAME = 'list'
    DESCRIPTION = 'Display detected configurations.'
    ALIASES = ['ls', 'info']

    def dispatch(self, args, rest_args, state, detected_configs):
        print_configurations(state, detected_configs)


class ConfigCommand(DockerDevelopCommand):
    NAME = 'config'
    DESCRIPTION = 'Show docker-compose configuration'

    def register_command_args(self, parser: ArgumentParser):
        parser.add_argument('--cache-only',
                            action="store_true",
                            help='Generate cached version of docker-compose configuration.'
                            )

    # noinspection PyUnresolvedReferences
    def dispatch(self, args, rest_args, state, detected_configs):
        selected_docker_config = docker_compose_config(
                state, detected_configs, selected=True)
        result = docker_compose(state, detected_configs, selected_docker_config.profiles,
                                'config', *rest_args, capture_output=args.cache_only, selected=True)
        if args.cache_only:
            cache_path = os.path.join(state.base_path, CACHE_DIR_NAME, CACHE_DOCKER_COMPOSE)
            with open(cache_path, 'wb') as f:
                f.write(result)
                info(f'Writen cached version of docker-compose config to {cache_path}')


def install_command():
    for shell_profile in SHELL_PROFILES:
        shell_profile_path = os.path.join(os.environ['HOME'], shell_profile)
        if os.path.exists(shell_profile_path):
            docker_develop_path = os.path.abspath(os.path.dirname(__file__))
            export_command = f'export PATH="{docker_develop_path}:$PATH"'
            is_installed = any([export_command in line for line in open(shell_profile_path).readlines()])
            if not is_installed:
                response = None
                while not response or response.upper() not in ['', 'YES', 'NO']:
                    response = input(f'Install {sys.argv[0]} in ~/{shell_profile}? (NO/yes) ')
                info('')
                if response.upper() == 'YES':
                    info(f'Installing in {sys.argv[0]} in ~/{shell_profile}...')
                    with open(shell_profile_path, 'a') as f:
                        f.write(export_command)
                    info('Installed successfully, for changes to take affect please restart your shell or run:')
                    info(f'\n   source {shell_profile_path}\n')
            else:
                info(f'You are all set, {sys.argv[0]} already installed in ~/{shell_profile}!')
            break
    sys.exit(0)


def version_command():
    print(__version__)
    sys.exit(0)


def init_logging(args):
    level = logging.INFO - (args.verbosity * 10)
    logging.basicConfig(level=level if level >= 0 else 0, format="%(message)s")


def init_command(_state, _detected_configs, args):
    config_path = os.path.abspath(os.path.curdir)
    config_name = os.path.basename(config_path)
    parent_path = os.path.dirname(config_path)

    on_config_path = config_path in [os.path.dirname(args.config_dir)]
    on_search_path = parent_path in args.search_path

    if not on_search_path and not on_config_path:
        search_paths = '\n'.join(args.search_path)
        error(f'Initialization failure, not on a search paths: \n\n{search_paths}')
        exit(1)

    project_path_env = config_name.upper().replace('-', '_').replace(' ', '_') + '_PATH'
    template_args = {
        'project_name': config_name,
        'project_path_env': project_path_env,
    }

    init_config_file(config_path, PROJECT_DOCKER_COMPOSE, args.force, INIT_DOCKER_COMPOSE_DEV, **template_args)
    init_config_file(config_path, PROJECT_DOCKERFILE, args.force, INIT_DOCKERFILE_LOCAL, **template_args)

    for override_name in args.with_override_for or []:
        override_filename = PROJECT_OVERRIDE_NAME.format(
                override_name=override_name)
        template_args = {
            'project_name': config_name,
            'project_path_env': project_path_env,
            'override_name': override_name,
        }
        init_config_file(config_path, override_filename, args.force, INIT_DOCKER_COMPOSE_DEV_OVERRIDE, **template_args)


def init_config_file(config_base_path, config_filename, force, template, **template_args):
    config_path = os.path.join(config_base_path, CONFIG_DIR, config_filename)
    config_exists = os.path.exists(config_path)

    if force or not config_exists:
        info(f'{"Overwriting" if config_exists else "Creating"}... {config_path}')
        if not os.path.exists(os.path.dirname(config_path)):
            os.mkdir(os.path.dirname(config_path))
        with open(config_path, 'w') as config_fd:
            config_fd.write(template.format(**template_args))
    else:
        warning(f'Skipping, exists... {config_path}')

    return config_path


def reconfigure_command(state, detected_configs, selection):
    new_state = State(state.base_path, state.project_name, selection)
    new_selected_docker_config = docker_compose_config(new_state, detected_configs, selected=True)

    state_save(new_state, detected_configs, new_selected_docker_config.profiles)

    print_configurations(new_state, detected_configs)


def compose_command(state, detected_configs, rest_args):
    selected_docker_config = docker_compose_config(
            state, detected_configs, selected=True)
    print_services_ports(selected_docker_config)

    signal.signal(signal.SIGINT, lambda x, y: info('CTRL-C'))
    docker_compose(state, detected_configs, selected_docker_config.profiles,
                   *rest_args, capture_output=False, selected=True)


# noinspection PyInterpreter
def vault_command(state, _detected_configs, args):
    vault_state = vault_check(
            state.base_path, args.vault_file if 'vault_file' in args else [])
    if args.vault_command in [None, 'status']:
        vault_status_print(vault_state)
    elif args.vault_command == 'diff':
        vault_diff(state, vault_state)
    elif args.vault_command == 'create':
        vault_create(state, vault_state)
    elif args.vault_command == 'update':
        vault_update(state, vault_state, force=args.force)
    elif args.vault_command == 'extract':
        vault_extract(state, vault_state, force=args.force)


def ports_command(state, detected_configs):
    selected_docker_config = docker_compose_config(
            state, detected_configs, selected=True)
    print_services_ports(selected_docker_config)


def each_command(state, args, config, rest_args):
    if args.each_command == 'exec':
        each_exec_command(state, args, config, rest_args)
    elif args.each_command == 'pr':
        each_pr_command(state, args, config)
    elif args.each_command == 'list':
        each_list_command(state, args, config)
    elif args.each_command == 'status':
        each_status_command(state, args, config)


def each_exec_command(_state, args, config, rest_args):
    directories = find_repositories(
            args.search_path, args.each_group, args.each_regex, config)
    if args.each_exec_command:
        execute_bash_in_each_directory(directories, args.each_exec_command)
    else:
        command = ' '.join(rest_args) if rest_args else input(
                'Please provide command to be executed in each repository: ')
        execute_bash_in_each_directory(directories, command)


def each_pr_command(_state, args, config):
    directories = find_repositories(
            args.search_path, args.each_group, args.each_regex, config)
    into_branch = args.into_branch
    from_branch = args.from_branch
    execute_bash_in_each_directory(directories,
                                   f'gh pr create --base {into_branch} --head {from_branch} '
                                   f'--title "{from_branch} -> {into_branch}" --body ""'
                                   )


def each_list_command(_state, args, config):
    directories = find_repositories(
            args.search_path, args.each_group, args.each_regex, config)
    execute_bash_in_each_directory(
            directories,
            '')


def each_status_command(_state, args, config):
    directories = find_repositories(
            args.search_path, args.each_group, args.each_regex, config)
    execute_bash_in_each_directory(directories, 'git status -sb')


def parse_command_args(config, commands=None):
    search_paths = ', '.join(config.search_paths)

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbosity',
                        action='count',
                        default=0,
                        help=f'increase verbosity of output')
    parser.add_argument('--install',
                        action="store_true",
                        help='Install docker-develop on the shell PATH.'
                        )
    parser.add_argument('-c', '--config-dir',
                        default=config.config_dir,
                        help=f'base configuration directory (defaults to {config.config_dir})')
    parser.add_argument('-s', '--search-path',
                        nargs='*',
                        default=config.search_paths,
                        help=f'search path for detecting configurations (defaults to {search_paths})')
    # noinspection PyTypeChecker
    subparsers = parser.add_subparsers(title=None, dest='command', metavar='COMMAND')

    for command in commands or []:
        subparser = subparsers.add_parser(command.NAME,
                                          help=command.DESCRIPTION,
                                          add_help=command.HELP,
                                          aliases=command.ALIASES)
        command.register_command_args(subparser)

    return parser.parse_known_args() + tuple([parser.print_help])


def detect_configs(args):
    detected_projects, detected_auxiliaries = detect_docker_projects(args.search_path)

    detected_auxiliaries = {
        **detected_auxiliaries,
        **detect_docker_auxiliary(args.config_dir)
    }

    detected_projects = filter_project_overrides(
            detected_projects, detected_auxiliaries)
    detected_auxiliaries = filter_auxiliaries_overrides(
            detected_projects, detected_auxiliaries)

    return Configs(projects=detected_projects, auxiliaries=detected_auxiliaries)


def detect_docker_projects(search_paths):
    projects = {}
    auxiliaries = {}
    for search_path in search_paths:
        for candidate_path in glob(os.path.join(search_path, '*')):
            if not os.path.isdir(candidate_path):
                continue

            project_name = os.path.basename(candidate_path)
            docker_compose_path = os.path.join(
                    candidate_path, CONFIG_DIR, PROJECT_DOCKER_COMPOSE)
            if not os.path.exists(docker_compose_path):
                continue

            projects[project_name] = docker_compose_path

            overrides = detect_docker_overrides(project_name, os.path.join(candidate_path, CONFIG_DIR),
                                                PROJECT_DOCKER_COMPOSE_OVERRIDE_GLOB,
                                                PROJECT_OVERRIDE_NAME_REGEX)

            auxiliaries = {
                **auxiliaries,
                **detect_docker_auxiliary(os.path.join(candidate_path, CONFIG_DIR)),
            }

            projects[project_name] = DockerComposeProject(
                    project_name, candidate_path, docker_compose_path, overrides)

    return projects, auxiliaries


def detect_docker_overrides(name, search_path, name_glob, name_regex):
    overrides = {}
    for override_path in glob(os.path.join(search_path, name_glob)):
        override_file = os.path.basename(override_path)
        regex_match = name_regex.match(override_file)
        if regex_match:
            override_name = regex_match.group(1)
            overrides[override_name] = DockerComposeOverride(
                    override_name, name, search_path, override_path)

    return overrides


def detect_docker_auxiliary(search_path):
    auxiliaries = {}
    for auxiliary_path in glob(os.path.join(search_path, AUXILIARY_DOCKER_COMPOSE_GLOB)):
        auxiliary_file = os.path.basename(auxiliary_path)
        regex_match = AUXILIARY_NAME_REGEX.match(auxiliary_file)
        if regex_match:
            auxiliary_name = regex_match.group(1)

            override_regex = re.compile(
                    AUXILIARY_OVERRIDE_NAME_REGEX.format(auxiliary_name=auxiliary_name))

            overrides = detect_docker_overrides(auxiliary_name, search_path,
                                                AUXILIARY_DOCKER_COMPOSE_OVERRIDE_GLOB.format(
                                                        auxiliary_name=auxiliary_name),
                                                override_regex)
            auxiliaries[auxiliary_name] = DockerComposeAuxiliary(
                    auxiliary_name, search_path, auxiliary_path, overrides)

    return auxiliaries


def detect_docker_profiles(docker_config):
    docker_profiles = {}
    for service_name in docker_config['services']:
        if 'profiles' not in docker_config["services"][service_name]:
            continue
        for profile in docker_config["services"][service_name]["profiles"]:
            if profile not in docker_profiles:
                docker_profiles[profile] = []
            docker_profiles[profile].append(service_name)

    return docker_profiles


def filter_project_overrides(projects, auxiliaries):
    filtered_projects = {}
    for project_name in projects:
        project = projects[project_name]
        filtered_overrides = {}
        for override in project.overrides or {}:
            if override in projects or override in auxiliaries:
                filtered_overrides[override] = project.overrides[override]
        filtered_projects[project_name] = DockerComposeProject(project.name, project.base_path, project.docker_path,
                                                               filtered_overrides)

    return filtered_projects


def filter_auxiliaries_overrides(projects, auxiliaries):
    filtered_auxiliaries = {}
    for auxiliary_name in auxiliaries:
        auxiliary = auxiliaries[auxiliary_name]
        filtered_overrides = {}
        for override in auxiliary.overrides or {}:
            if override in projects or override in auxiliaries:
                filtered_overrides[override] = auxiliary.overrides[override]
        filtered_auxiliaries[auxiliary_name] = DockerComposeAuxiliary(auxiliary.name, auxiliary.base_path,
                                                                      auxiliary.docker_path,
                                                                      filtered_overrides)

    return filtered_auxiliaries


def docker_compose(state, configs, profiles=None, *args, capture_output=True, selected=False, ignore_cache=False):
    # NOTE: Executing docker-compose is very intensive (about 0.6s), most of execution time (99%) is spent here
    config_paths = [os.path.join(state.base_path, BASE_DOCKER_COMPOSE)]
    config_paths += docker_compose_paths(state, configs, selected=selected)

    config_args = docker_compose_path_args(config_paths)
    profile_args = docker_compose_profiles_args(profiles)

    # TODO: Not best place for setting this, maybe move it somewhere else because we will execute more commands...
    setup_config_env_variables(state, configs)

    if not ignore_cache:
        config_args, profile_args = cached_config_args(state, config_args, profile_args, config_paths)

    command_args = config_args + profile_args

    debug_docker_compose_args(args, command_args)

    def exec_command(raise_exception=False):
        docker_command = ['docker', 'compose'] if DOCKER_COMPOSE_VERSION > 1 else ['docker-compose']
        return execute_command(*docker_command, *command_args, *args, capture_output=capture_output,
                               throw_on_failed=raise_exception, cwd=state.base_path)

    if not capture_output:
        result = exec_command()
    else:
        result = cached_result(state.base_path, config_paths, exec_command)

    return result


def setup_config_env_variables(state, configs):
    os.environ['PWD'] = os.path.join(state.base_path, '..')
    os.environ['COMPOSE_PROJECT_NAME'] = state.project_name

    debug('#------------- ENV START -----------------#')
    for project_name in configs.projects:
        project = configs.projects[project_name]
        project_env_name = project.name.upper().replace(' ', '_').replace('-', '_') + '_PATH'
        os.environ[project_env_name] = project.base_path
        debug(f'export {project_env_name}="{project.base_path}"')
    for aux_name in configs.auxiliaries:
        aux = configs.auxiliaries[aux_name]
        aux_env_name = aux.name.upper().replace(' ', '_').replace('-', '_') + '_PATH'
        os.environ[aux_env_name] = aux.base_path
        debug(f'export {aux_env_name}="{aux.base_path}"')
    debug('#-----------------------------------------#')


def debug_docker_compose_args(args, docker_compose_args):
    debug('#------------- CMD START -----------------#')
    name = 'docker compose' if DOCKER_COMPOSE_VERSION > 1 else 'docker-compose'
    debug(''.join([
        f'{name} \\\n   ',
        ' '.join(docker_compose_args).replace(' -f ', ' \\\n   -f ').replace(' --', ' \\\n   --'), '\\\n  ',
        ' '.join(args)
    ]))
    debug('#-----------------------------------------#')


CACHE_DIR_NAME = '.cache'
CACHE_DOCKER_COMPOSE = 'docker-compose.yml'


def cache_is_stale(cache_path, *config_paths):
    cache_path_mtime = os.path.getmtime(cache_path) if os.path.exists(cache_path) else 0
    paths_mtimes = [os.path.getmtime(path) for path in config_paths if os.path.exists(path)]
    paths_max_mtime = max(paths_mtimes) if paths_mtimes else cache_path_mtime + 1

    return cache_path_mtime < paths_max_mtime


def cached_result(base_path, paths, func):
    cache_dir, cached_results_path = cache_result_path(base_path, paths)

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    if cache_is_stale(cached_results_path, *paths):
        debug('Running, caching result...')
        try:
            result = func(True)
        except RuntimeError as e:
            error('Failed, skipping caching result')
            return e.args[0]

        with open(cached_results_path, 'wb') as cache_file:
            pickle.dump(result, cache_file, 0)
        return result
    else:
        debug(f'Loading from cache... {cached_results_path}')
        with open(cached_results_path, 'rb') as cache_file:
            return pickle.load(cache_file)


def cache_result_path(base_path, paths):
    paths_hash = hashlib.md5(''.join(path for path in sorted(paths)).encode()).hexdigest()

    cache_dir = os.path.join(base_path, CACHE_DIR_NAME)
    cache_path = os.path.join(cache_dir, paths_hash)

    return cache_dir, cache_path


def cached_config_args(state, config_args, profile_args, config_paths):
    try:
        cache_dir, cached_result_path = cache_result_path(state.base_path, config_paths)

        cache_path = os.path.join(cache_dir, CACHE_DOCKER_COMPOSE)
        lock_path = os.path.join(state.base_path, STATE_CMD_NAME)

        if cache_is_stale(cache_path, *config_paths, cached_result_path, lock_path):
            # FIXME: Might not have environment variables set...
            docker_command = ['docker', 'compose'] if DOCKER_COMPOSE_VERSION > 1 else ['docker-compose']
            result = execute_command(*docker_command, *config_args, *profile_args,
                                     'config',
                                     capture_output=True, throw_on_failed=True, cwd=state.base_path)

            with open(cache_path, 'wb') as f:
                f.write(result)
                info(f'Writen cached version of docker-compose config to {cache_path}')
        info(f'Using cached version of docker-compose config from {cache_path}')

        return ('-f', cache_path), profile_args
    except RuntimeError:
        return config_args, profile_args


def docker_compose_config(state, configs, selected=False):
    if DOCKER_COMPOSE_VERSION > 1:
        raw_config = docker_compose(state, configs, None,
                                    '--profile', '*', 'config', selected=selected, ignore_cache=True)
    else:
        raw_config = docker_compose(state, configs, None,
                                    'config', selected=selected, ignore_cache=True)
    if raw_config:
        parsed = load(raw_config, Loader=Loader)
        profiles = docker_compose_config_profiles(
                state, parsed, selected=selected)
        return DockerConfig(parsed, raw_config, profiles)
    return DockerConfig({'services': {}}, '', {})


def docker_compose_paths(state, configs, selected=False):
    all_selected = filter_config_by_selected(state, configs, selected=selected)

    return list(map(lambda item: item.docker_path, all_selected))


def docker_compose_path_args(paths):
    return reduce(lambda args, path: args + ('-f', path), paths or [], ())


def docker_compose_profiles_args(profiles):
    return reduce(lambda args, path: args + ('--profile', path), profiles or [], ())


def docker_compose_config_profiles(state, docker_config_parsed, selected=False):
    selected_profiles = {}
    for service_name in docker_config_parsed['services']:
        if 'profiles' not in docker_config_parsed["services"][service_name]:
            continue

        for profile in docker_config_parsed["services"][service_name]['profiles']:
            if selected and state.selected is not None and profile not in state.selected:
                continue
            if profile not in selected_profiles:
                selected_profiles[profile] = []
            selected_profiles[profile].append(service_name)

    return selected_profiles


def filter_config_by_selected(state, configs, selected=False):
    selected = select_all_defined(
            configs) if not selected else (state.selected or [])
    selected_projects = filter_by_names(configs.projects.values(), selected)
    selected_overrides = filter_by_names(chain(*[project.overrides.values() for project in selected_projects]),
                                         selected)
    selected_auxiliaries = filter_by_names(
            configs.auxiliaries.values(), selected)
    selected_auxiliaries_overrides = filter_by_names(
            chain(*[auxiliary.overrides.values() for auxiliary in selected_auxiliaries]),
            selected)

    all_selected_configs = selected_projects + selected_auxiliaries
    all_selected_overrides = selected_overrides + selected_auxiliaries_overrides

    _all = as_sorted_by_override_count(
            all_selected_configs, all_selected_overrides)

    return _all


def as_sorted_by_override_count(configs, overrides):
    stats = Counter(override.name for override in overrides)

    # Sort by override count
    def _sorted(_configs):
        return list(
                sorted(_configs, key=lambda config: stats[config.name], reverse=True))

    grouped_overrides = {}
    # Overrides, group by name
    for override in overrides:
        if override.name not in grouped_overrides:
            grouped_overrides[override.name] = []
        grouped_overrides[override.name].append(override)

    # Overrides, re-group/re-order by project name
    for group_name in grouped_overrides:
        new_group_override = []
        # debug(grouped_overrides[group_name])
        for override in grouped_overrides[group_name]:
            # debug(f'{override.project}  ')
            if override.project != group_name and override.project in grouped_overrides:
                grouped_overrides[override.project].insert(0, override)
            else:
                new_group_override.append(override)
        grouped_overrides[group_name] = new_group_override

    sorted_configs = _sorted(configs)
    sorted_overrides = reduce(
        lambda acc, name: acc + grouped_overrides[name],
        sorted(grouped_overrides, key=lambda name: len(grouped_overrides[name])), []
    )

    return sorted_configs + sorted_overrides


def filter_by_names(iterable, names):
    return list(filter(lambda entry: entry.name in names, iterable))


def execute_command(*args, capture_output=True, throw_on_failed=False, cwd=None):
    debug(' '.join(args))
    cwd = cwd or os.path.dirname(os.path.abspath(__file__))
    debug(cwd)
    try:
        with Popen(args, stdout=PIPE if capture_output else None, cwd=cwd) as command:
            result = command.stdout.read() if capture_output else None
            if throw_on_failed and command.poll() != 0:
                raise RuntimeError(result)
            return result
    except KeyboardInterrupt:
        pass


def select_all_defined(configs):
    return list(chain(configs.projects.keys(), configs.auxiliaries.keys()))


def execute_bash_in_each_directory(directories, command):
    initial_directory = os.getcwd()
    for directory in directories:
        dir_basename = os.path.basename(directory)
        # header = f'{dir_basename}: {command}'
        info(f'== {dir_basename} '.ljust(79, '=') + '=')
        # info(f'\n=============================================\n{dir_basename}: {command}')
        os.chdir(directory)
        os.system(command)
    os.chdir(initial_directory)


def find_repositories(search_paths, group=None, regex=None, config=Config):
    repository_groups = config.repository_groups
    selector = '*' if not group or not repository_groups or group not in repository_groups else repository_groups[
        group].selector
    paths = []
    for search_path in search_paths:
        for candidate_git_path in glob(os.path.join(search_path, selector, '.git')):
            candidate_path = candidate_git_path[:-len('.git') - 1]
            if ((not group
                 or not repository_groups[group].regex
                 or re.fullmatch(repository_groups[group].regex, candidate_path)
            ) and (not regex or re.fullmatch(regex, candidate_path))):
                paths.append(candidate_path)
    return paths


CONFIG_TYPE_DEV_TITLE = 'dir'
CONFIG_TYPE_CONF_TITLE = 'conf'
TABLE_COLUMN_SPACING = 8

COLOR_RESET = '\x1b[0m'


# noinspection PyPep8Naming
def COLOR_ESCAPE(pallet_id, fg_color_id, bg_color_id): return '\x1b[%s;%s;%sm' % (
    pallet_id, fg_color_id, bg_color_id)


INACTIVE_COLOR = COLOR_ESCAPE(2, 37, 39)
ACTIVE_COLOR = COLOR_ESCAPE(0, 32, 38)
UPDATE_COLOR = COLOR_ESCAPE(0, 33, 33)
NEW_COLOR = COLOR_ESCAPE(5, 30, 43)

AVAILABLE = '-'
AUXILIARY = '◌'
SELECTED = '●'
OPTIONAL = '~'
OPTIONAL_SELECTED = '◆'


def print_configurations(state, configs, selected=False):
    all_selected = state.selected if state.selected else []

    config_title, config_title_width = define_column('Configuration', chain(map(len, configs.projects.keys()),
                                                                            map(len, configs.auxiliaries.keys())))

    type_title, type_title_width = define_column('Type', map(len, [CONFIG_TYPE_DEV_TITLE,
                                                                   CONFIG_TYPE_CONF_TITLE]))

    overrides_title, overrides_title_width = define_column(
            'Supports')

    shown = False
    if configs.projects:
        info(f'{config_title:<{config_title_width}} '
             f'{type_title:<{type_title_width}} '
             f'{overrides_title:<{overrides_title_width}}')
        for project in sorted(configs.projects):
            if selected and project not in all_selected:
                continue
            status = AVAILABLE if project not in all_selected else SELECTED
            color = INACTIVE_COLOR if project not in all_selected else ACTIVE_COLOR
            override_list = ", ".join(
                    [n for n in configs.projects[project].overrides])
            info(f'{color} '
                 f'{status} {project:<{config_title_width - 3}} '
                 f'{CONFIG_TYPE_DEV_TITLE:<{type_title_width}} '
                 f'{override_list}'
                 f'{COLOR_RESET}')
            shown = True

    if configs.auxiliaries:
        for auxiliary in sorted(configs.auxiliaries):
            if selected and auxiliary not in all_selected:
                continue
            status = AVAILABLE if auxiliary not in all_selected else SELECTED
            color = INACTIVE_COLOR if auxiliary not in all_selected else ACTIVE_COLOR

            parent = configs.auxiliaries[auxiliary].base_path.replace(state.base_path, '')
            if parent:
                parent = f' ({os.path.basename(os.path.dirname(parent))})'

            name = f'{auxiliary}{parent}'

            override_list = ", ".join(
                    [n for n in configs.auxiliaries[auxiliary].overrides])
            info(f'{color} '
                 f'{status} {name:<{config_title_width - 3}} '
                 f'{CONFIG_TYPE_CONF_TITLE:<{type_title_width}} '
                 f'{override_list}'
                 f'{COLOR_RESET}')
            shown = True

    if not shown:
        auxiliary = '--'
        status = AVAILABLE
        color = INACTIVE_COLOR
        type_name = '--'
        override_list = '--'

        info(f'{color} '
             f'{status} {auxiliary:<{config_title_width - 3}} '
             f'{type_name:<{type_title_width}} '
             f'{override_list}'
             f'{COLOR_RESET}')

    if not shown:
        info('')
        info('No configurations selected, use: docker-develop select')
    else:
        info('')
        info(f'Legend: {SELECTED} Selected\t{AVAILABLE} Available')
        info('')


def print_docker_config(detected_docker_config, selected_docker_config, selected=False):
    selected_profiles_set = set(selected_docker_config.profiles)
    docker_config = selected_docker_config.parsed if selected else detected_docker_config.parsed

    services_title, services_width = define_column(
            'Docker Services', map(len, docker_config['services']))
    profiles_title, profiles_width = define_column('Docker Profiles')

    info(f'{services_title:<{services_width}} {profiles_title:<{profiles_width}}')
    for service_name in sorted_by_profile(docker_config):
        is_selected = service_name in selected_docker_config.parsed['services']
        if 'profiles' in docker_config["services"][service_name]:
            profiles_set = set(
                    docker_config["services"][service_name]['profiles'])
            is_profile_selected = bool(
                    selected_profiles_set.intersection(profiles_set))

            # if not show_all and (not is_selected or not is_profile_selected):
            #     continue
            status = OPTIONAL_SELECTED if is_profile_selected else OPTIONAL
            color = ACTIVE_COLOR if is_profile_selected else INACTIVE_COLOR

            profiles_list = ", ".join(
                    sorted(docker_config["services"][service_name]["profiles"]))

            info(
                    f'{color} {status} {service_name:<{services_width - 3}} {profiles_list}{COLOR_RESET}')
        else:
            if selected and not is_selected:
                continue
            status = SELECTED if is_selected else AVAILABLE
            color = ACTIVE_COLOR if is_selected else INACTIVE_COLOR
            info(f'{color} {status} {service_name:<{services_width - 3}} -{COLOR_RESET}')
    info('')
    info(f'Legend:\t'
         f'{SELECTED} Selected\t'
         f'{AVAILABLE} Available\t'
         f'{OPTIONAL_SELECTED} Selected (by profile)\t'
         f'{OPTIONAL} Available (by profile)')
    info('')


def print_services_ports(docker_config):
    services = docker_config.parsed['services']
    for service_id in services.keys():
        if re.fullmatch(PORTS_PRINT_SERVICE_REGEX, service_id):
            service = services[service_id]
            info(service_id)
            for port in service['ports']:
                info(f'    - {port["published"]}:{port["target"]}')


def define_column(title, values=None):
    return title, max(chain(values or [], [len(title)])) + TABLE_COLUMN_SPACING


def sorted_by_profile(docker_config):
    return sorted(docker_config['services'],
                  key=lambda service_name: 'profiles' in docker_config['services'][service_name])


VAULT_SECRET_ENV = 'DOCKER_DEVELOP_VAULT_SECRET'

VAULT_IN_SYNC = 'VAULT_IN_SYNC'

VAULT_UPDATE_VAULT = 'VAULT_UPDATE_VAULT'
VAULT_ADD_VAULT = 'VAULT_ADD_VAULT'

VAULT_UPDATE_FS = 'VAULT_UPDATE_FS'
VAULT_ADD_FS = 'VAULT_ADD_FS'

VAULT_STATUS_IN_SYNC = 'VAULT_STATUS_IN_SYNC'
VAULT_STATUS_VAULT_UPDATE = 'VAULT_STATUS_VAULT_UPDATE'
VAULT_STATUS_FS_UPDATE = 'VAULT_STATUS_FS_UPDATE '
VAULT_STATUS_CONFLICT = 'VAULT_STATUS_CONFLICT'

VaultState = namedtuple('VaultState', 'status state path secret')


def vault_check(base_path, files=None):
    vault_path = os.path.join(base_path, VAULT_FILENAME)

    if not os.path.exists(vault_path):
        return None

    state = {}
    for file in files:
        if os.path.exists(file):
            _vault_state(state, VAULT_ADD_VAULT, file)

    with ZipFile(vault_path) as vault:
        for vault_file in vault.infolist():
            vault_file_fs_path = os.path.join(base_path, vault_file.filename)
            if os.path.exists(vault_file_fs_path):
                local_file_stat = os.stat(vault_file_fs_path)

                vault_file_datetime = datetime(*vault_file.date_time)
                local_file_datetime = datetime.fromtimestamp(
                        local_file_stat.st_mtime)

                local_file_crc = crc32(vault_file_fs_path)

                if local_file_crc == vault_file.CRC:
                    _vault_state(state, VAULT_IN_SYNC, vault_file.filename)
                    continue

                debug(f'{vault_file.filename} {local_file_datetime} '
                      f'{vault_file_datetime} {local_file_crc} {vault_file.CRC}')

                if local_file_datetime < vault_file_datetime:
                    _vault_state(state, VAULT_UPDATE_FS, vault_file.filename)
                elif local_file_datetime > vault_file_datetime:
                    _vault_state(state, VAULT_UPDATE_VAULT,
                                 vault_file.filename)
            else:
                _vault_state(state, VAULT_ADD_FS, vault_file.filename)

    status = VAULT_STATUS_IN_SYNC
    debug(state)

    if VAULT_UPDATE_FS in state and VAULT_UPDATE_VAULT in state:
        status = VAULT_STATUS_CONFLICT
    elif VAULT_UPDATE_FS in state and VAULT_ADD_VAULT in state:
        status = VAULT_STATUS_CONFLICT
    elif VAULT_UPDATE_VAULT in state and VAULT_ADD_FS in state:
        status = VAULT_STATUS_CONFLICT
    elif VAULT_ADD_FS in state:
        status = VAULT_STATUS_FS_UPDATE
    elif VAULT_UPDATE_VAULT in state:
        status = VAULT_STATUS_VAULT_UPDATE

    secret = os.environ[VAULT_SECRET_ENV] if VAULT_SECRET_ENV in os.environ else None

    # print(files)
    # print(VaultState(status, state, vault_path, secret))
    return VaultState(status, state, vault_path, secret)


VAULT_FILE_STATUS_MAP = {
    VAULT_IN_SYNC: 'In Sync', VAULT_UPDATE_FS: 'Update (missing changes in filesystem)',
    VAULT_UPDATE_VAULT: 'Update (missing changes in vault)',
    VAULT_ADD_VAULT: 'New    (missing file in vault)',
    VAULT_ADD_FS: 'New    (missing file in filesystem)'
}

VAULT_FILE_STATUS_COLOR_MAP = {
    VAULT_IN_SYNC: ACTIVE_COLOR,
    VAULT_UPDATE_FS: UPDATE_COLOR,
    VAULT_UPDATE_VAULT: UPDATE_COLOR,
    VAULT_ADD_VAULT: NEW_COLOR,
    VAULT_ADD_FS: NEW_COLOR
}

VAULT_STATUS_MAP = {
    VAULT_STATUS_IN_SYNC: 'In Sync',
    VAULT_STATUS_VAULT_UPDATE: 'Update Vault',
    VAULT_STATUS_FS_UPDATE: 'Update filesystem',
    VAULT_STATUS_CONFLICT: 'Conflict (changes in both vault and filesystem)'
}

VAULT_STATUS_COLOR_MAP = {
    VAULT_STATUS_IN_SYNC: ACTIVE_COLOR,
    VAULT_STATUS_VAULT_UPDATE: UPDATE_COLOR,
    VAULT_STATUS_FS_UPDATE: UPDATE_COLOR,
    VAULT_STATUS_CONFLICT: COLOR_ESCAPE(1, 31, 40)
}


def vault_status_print(vault_state):
    flat_state = _vault_flat_state(vault_state)

    filename_title, filename_width = define_column(
            'Vault File', map(lambda fstate: len(fstate[0]), flat_state))
    status_title, status_width = define_column(
            'Status', map(len, VAULT_FILE_STATUS_MAP.values()))

    info(f'Status:{VAULT_STATUS_COLOR_MAP[vault_state.status]} {VAULT_STATUS_MAP[vault_state.status]} {COLOR_RESET}\n')

    info(f'{filename_title:<{filename_width}} '
         f'{status_title:<{status_width}} ')
    for state in flat_state:
        color = VAULT_FILE_STATUS_COLOR_MAP[state[1]]
        info(f'{color}'
             f'{state[0]:<{filename_width}} '
             f'{VAULT_FILE_STATUS_MAP[state[1]]:<{status_width}}'
             f'{COLOR_RESET}')
    pass


def vault_diff(state, vault_state):
    vault_tmp = os.path.join(state.base_path, '.vault')

    if os.path.exists(vault_tmp):
        print(f'Vault Temp exists, aborting: {vault_tmp}')
        exit(1)

    try:
        if vault_state.secret:
            execute_command('unzip', '-u', '-P', vault_state.secret,
                            '-d', vault_tmp, vault_state.path, cwd=state.base_path)
        else:
            execute_command('unzip', '-u', '-d', vault_tmp, vault_state.path, cwd=state.base_path)
        flat_state = _vault_flat_state(vault_state)
        for fstate in flat_state:
            execute_command('git', '--no-pager', 'diff', '--no-index',
                            os.path.join(vault_tmp, fstate[0]),
                            os.path.join(state.base_path, fstate[0]),
                            capture_output=False,
                            cwd=state.base_path)
    finally:
        if os.path.exists(vault_tmp) and os.path.isdir(vault_tmp):
            rmtree(vault_tmp)


def _vault_state(state, status, vault_filename):
    if status not in state:
        state[status] = []
    state[status].append(vault_filename)


def _vault_flat_state(vault_state):
    return tuple((filename, state[0],) for state in vault_state.state.items() for filename in state[1])


def vault_create(state, vault_state):
    print(state, vault_state)
    if vault_state.status in [VAULT_STATUS_VAULT_UPDATE]:
        pass
    else:
        pass


def vault_extract(state, vault_state, force=False):
    debug(f'{state}, {vault_state}')
    if vault_state.status in [VAULT_STATUS_VAULT_UPDATE]:
        warning('Warning: Filesystem has changes not present in Vault...')
        warning(f'\nFiles changed in filesystem:')
        warning('   ' + '\n   '.join(vault_state.state[VAULT_UPDATE_VAULT]))
        not force and exit(1)
    if vault_state.status in [VAULT_STATUS_CONFLICT]:
        warning('Warning: Changes present in both filesystem and vault...')
        not force and exit(1)

    if vault_state.secret:
        execute_command('unzip', '-o', '-P', vault_state.secret,
                        vault_state.path, capture_output=False, cwd=state.base_path)
    else:
        execute_command('unzip', '-o', vault_state.path, capture_output=False, cwd=state.base_path)


def vault_update(state, vault_state, force=False):
    debug(f'{state}, {vault_state}')
    if vault_state.status in [VAULT_STATUS_FS_UPDATE]:
        warning('Warning: Vault has changes not present in filesystem...')

        warning(f'\nFiles changed in vault:')
        warning('   ' + '\n   '.join(vault_state.state[VAULT_UPDATE_FS]))
        not force and exit(1)
    if vault_state.status in [VAULT_STATUS_CONFLICT]:
        warning('Warning: Changes present in both filesystem and vault...')
        not force and exit(1)

    all_files = map(lambda x: x[0], _vault_flat_state(vault_state))
    if vault_state.secret:
        execute_command('zip', '-e', '-P', vault_state.secret,
                        vault_state.path, *all_files, capture_output=False, cwd=state.base_path)
    else:
        execute_command('zip', '-e', vault_state.path,
                        *all_files, capture_output=False, cwd=state.base_path)


def crc32(file_name):
    with open(file_name, 'rb') as fd:
        crc_hash = 0
        while True:
            chunk = fd.read(65536)
            if not chunk:
                break
            crc_hash = zlib.crc32(chunk, crc_hash)
        return crc_hash & 0xFFFFFFFF


STATE_CMD_NAME = 'docker-develop.lock'
STATE_CMD_SEPARATOR = ':'

STATE_CMD_DOCKER_DEVELOP_REGEX = re.compile('^DOCKER_DEVELOP="(.*)"$')
STATE_CMD_PROJECT_NAME_REGEX = re.compile('^COMPOSE_PROJECT_NAME="(.*)"$')

STATE_CMD_TEMPLATE = """#!/usr/bin/env bash

# WARNING: auto-generated file, do not modify since changes may be lost
#          when docker-develop is re-run

as_list() {{
   local SEPARATOR=""
   while IFS= read -r line; do
     echo -n "${{SEPARATOR}}${{line}}"
     SEPARATOR=":"
   done
}}

DOCKER_DEVELOP="{selected_configs}"

PWD="{docker_compose_pwd}"
COMPOSE_PROJECT_NAME="{docker_compose_project_name}"
COMPOSE_ENV_FILE=".env"
COMPOSE_FILE=$(as_list <<__END__
{docker_compose_files}
__END__)
COMPOSE_PROFILES=$(as_list <<__END__
{docker_compose_profiles}
__END__)

export COMPOSE_PROJECT_NAME COMPOSE_FILE COMPOSE_PROFILES

docker-compose --env-file "${{COMPOSE_ENV_FILE}}" ${{*}}
"""


def state_load(args, config):
    selected = None
    project_name = config.base_name

    path = os.path.join(args.config_dir, STATE_CMD_NAME)
    if not os.path.isfile(path):
        return State(args.config_dir, project_name, selected)

    with open(path) as config:
        for line in config.readlines():
            selected_match = STATE_CMD_DOCKER_DEVELOP_REGEX.match(line)
            if selected_match:
                selected = selected_match.group(1).split(STATE_CMD_SEPARATOR)
                continue

            project_name_match = STATE_CMD_PROJECT_NAME_REGEX.match(line)
            if project_name_match:
                project_name = project_name_match.group(1)
                continue

    if 'project_name' in args:
        project_name = args.project_name

    return State(args.config_dir, project_name, selected)


def state_save(state, configs, selected_profiles):
    script = STATE_CMD_TEMPLATE.format(**{
        'selected_configs': STATE_CMD_SEPARATOR.join(state.selected),
        'docker_compose_project_name': state.project_name,
        'docker_compose_pwd': os.path.join(state.base_path, '..'),
        'docker_compose_files': '\n'.join(docker_compose_paths(state, configs, selected=True)),
        'docker_compose_profiles': '\n'.join(selected_profiles.keys()),
    })
    path = os.path.join(state.base_path, STATE_CMD_NAME)

    with open(path, 'w') as config:
        config.write(script)

    os.chmod(path, 0o755)


INIT_DOCKER_COMPOSE_DEV = """\
# Main docker-compose definition for {project_name} local development, used by docker-develop
version: "3"

services:
  {project_name}:
    container_name: {project_name}
    restart: unless-stopped
    build:
      context:    ${{{project_path_env}}}
      dockerfile: develop/Dockerfile_local
"""
INIT_DOCKER_COMPOSE_DEV_OVERRIDE = """\
# Override docker-compose definition (when {override_name} is used with {project_name}, used by docker-develop
version: "3"

services:
  {project_name}:
    depends_on:
      {override_name}:
        condition: service_healthy
"""
INIT_DOCKERFILE_LOCAL = """\
# Dockerfile definition for {project_name} local development, used indirectly docker-develop

"""


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30, 38):
            s1 = ''
            for bg in range(40, 48):
                escape_format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (escape_format, escape_format)
            print(s1)
        print('\n')


def main(base_path=None):
    base_path = base_path or os.path.abspath(os.curdir)
    docker_develop = DockerDevelop()
    docker_develop.main(base_path)


if __name__ == '__main__':
    # print_format_table()

    #main(os.path.abspath(os.curdir))
    main()

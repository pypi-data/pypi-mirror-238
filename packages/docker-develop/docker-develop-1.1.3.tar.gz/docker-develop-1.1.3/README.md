# Docker-Develop

Docker-Develop is a versatile utility tool designed to simplify the management of Docker Compose configurations and make your container orchestration tasks smoother than ever. It empowers you to effortlessly work with distributed `docker-compose.yml` files scattered across multiple repositories and directories, providing a unified and efficient approach to containerized development.

## Key Features

- **Parameterized Docker Compose**: Docker-Develop streamlines the usage of `docker-compose`, ensuring the right parameters are applied based on your selections.
- **Dependency Management**: Define dependencies between configurations, enabling you to control the order in which `docker-compose.yml` files are passed to Docker Compose.
- **Environment Variable Overrides**: Customize your configurations by overriding environment variables through dependencies.
- **Docker Compose Profiles**: Seamlessly work with Docker Compose profiles to meet your specific development needs.
- **Secrets Vault**: Built-in support for securely storing sensitive information, such as environment variables, certificates, and more. All securely managed as password-protected zip files.

## Getting Started

Docker-Develop offers a wide range of commands to help you manage your Docker Compose configurations effectively. Here are some of the core commands to get you started:

- `init`: Initialize a Docker-Develop configuration.

- `vault`: Manage your vault of secrets.

- `list`: Display detected configurations.
- `select`: Choose a configuration to enable, disable, or reset.
- `services`: List Docker Compose services and profiles.
- `each`: Run a command in each configuration directory.

- `compose`: Work with Docker Compose configurations.
- `status`: Get the status of Docker Compose services.
- `logs`: View the logs of Docker Compose services.
- `up`: Start your Docker Compose environment.
- `down`: Shut down your Docker Compose environment.
- `build`: Build a Docker Compose service.
- `rebuild`: Build and start a Docker Compose service.
- `restart`: Restart a Docker Compose service.

## Installation

```shell
pip install docker-develop
```

By leveraging Docker-Develop, you can streamline your Docker Compose development workflows and make the most out of your containerized applications. Give it a try and experience a more efficient and organized approach to container orchestration.

[**Check the documentation for detailed usage instructions and examples.**](#)

[**View on GitHub**](https://github.com/Cledar/docker-develop)


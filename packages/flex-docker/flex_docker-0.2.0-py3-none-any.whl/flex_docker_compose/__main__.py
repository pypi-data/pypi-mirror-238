#!/usr/bin/env python3
# flake8: noqa
import os

from flex_framework.application import ApplicationBootstrap

from .etc.config import extend_env_variables, params
from .shell_proxy import DockerCompose


def main():
    bootstrap = ApplicationBootstrap.create(
        os.path.basename(__file__), extend_env_variables(params)
    )
    application = bootstrap.create_application(DockerCompose)
    bootstrap.run(application)


if __name__ == "__main__":
    main()

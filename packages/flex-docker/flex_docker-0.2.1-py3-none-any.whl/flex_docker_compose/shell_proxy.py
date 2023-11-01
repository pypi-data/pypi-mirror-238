import os

from flex_framework.api.application import ApplicationInterface, T
from flex_framework.console.otput import CliResponse
from flex_framework.shell.proxy import SimpleShellProxy


class DockerCompose(SimpleShellProxy, ApplicationInterface[CliResponse]):
    def launch(self) -> T:
        return CliResponse(self.execute("docker-compose"))

    def get_global_command_arguments(self) -> list:
        docker_compose_files = self.env.get("DOCKER_COMPOSE_FILES")
        docker_compose_root_dir = self.env.get("DOCKER_COMPOSE_ROOT_DIR")
        if docker_compose_files is None:
            docker_compose_files = ""
        docker_compose_files_items = docker_compose_files.split(" ")
        result = []
        for file in docker_compose_files_items:
            if len(file) > 0:
                result.append("-f")
                result.append(os.path.join(docker_compose_root_dir, file))
        return result

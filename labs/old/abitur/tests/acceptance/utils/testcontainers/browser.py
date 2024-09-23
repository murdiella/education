from testcontainers.compose import DockerCompose


with DockerCompose(
        "/",
        compose_file_name=["docker-compose.yml"],
        pull=True,
) as compose:
    ...
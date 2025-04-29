# Docker: Commands Cheat Sheet

# Docker image commands
$ docker images                               # List all images.
$ docker pull <image>                         # Pull an image from Docker Hub.
$ docker build -t <name>:<tag> .              # Build image from Dockerfile in current directory.
$ docker build -f <file> .                    # Build image from specific Dockerfile.
$ docker tag <image> <new-image>              # Create a tag for an image.
$ docker rmi <image>                          # Remove an image.
$ docker image prune                          # Remove unused images.
$ docker image inspect <image>                # Display detailed information about an image.
$ docker history <image>                      # Show the history of an image.
$ docker save <image> > <file.tar>            # Save an image to a tar archive.

# Docker container commands
$ docker ps                                   # List running containers.
$ docker ps -a                                # List all containers (running and stopped).
$ docker run <image>                          # Run a container from an image.
$ docker run -d <image>                       # Run container in detached mode.
$ docker run -p <host:container> <image>      # Run container with port mapping.
$ docker run -v <host:container> <image>      # Run container with volume mounted.
$ docker start <container>                    # Start a stopped container.
$ docker stop <container>                     # Stop a running container.
$ docker restart <container>                  # Restart a container.
$ docker rm <container>                       # Remove a container.

# Docker container interaction
$ docker logs <container>                     # Fetch the logs of a container.
$ docker logs -f <container>                  # Follow log output of a container.
$ docker exec -it <container> <command>       # Execute a command in a running container.
$ docker exec -it <container> bash            # Get a bash shell in a running container.
$ docker attach <container>                   # Attach to a running container.
$ docker cp <container>:<src> <dest>          # Copy files from container to host.
$ docker cp <src> <container>:<dest>          # Copy files from host to container.
$ docker inspect <container>                  # Display detailed info about a container.
$ docker stats                                # Display a live stream of container resource usage.
$ docker top <container>                      # Display the running processes of a container.

# Docker network commands
$ docker network ls                           # List all networks.
$ docker network create <name>                # Create a network.
$ docker network rm <name>                    # Remove a network.
$ docker network inspect <name>               # Display detailed information about a network.
$ docker network connect <network> <container> # Connect a container to a network.
$ docker network disconnect <network> <container> # Disconnect a container from a network.

# Docker volume commands
$ docker volume ls                            # List all volumes.
$ docker volume create <name>                 # Create a volume.
$ docker volume rm <name>                     # Remove a volume.
$ docker volume inspect <name>                # Display detailed information about a volume.
$ docker volume prune                         # Remove all unused volumes.

# Docker Compose commands
$ docker-compose up                           # Create and start containers defined in docker-compose.yml.
$ docker-compose up -d                        # Create and start in detached mode.
$ docker-compose down                         # Stop and remove containers, networks, images, and volumes.
$ docker-compose ps                           # List containers in the Compose project.
$ docker-compose logs                         # View output from containers.
$ docker-compose build                        # Build or rebuild services.
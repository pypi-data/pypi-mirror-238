# [[file:../org/orgweb/container.org::*Imports][Imports:1]]
import docker
from docker.errors import ImageNotFound, NotFound
# Imports:1 ends here

# [[file:../org/orgweb/container.org::*Initialize Docker][Initialize Docker:1]]
docker = docker.from_env()
# Initialize Docker:1 ends here

# [[file:../org/orgweb/container.org::*Images Utility Functions][Images Utility Functions:1]]
def build_image(img: str='localbuild:orgweb') -> None:
    """Build the orgweb image from the Dockerfile. Returns <image, logs>"""
    image, logs = docker.images.build(path='.', tag=img, rm=True)
    return image, logs


def image_exists(img: str='localbuild:orgweb') -> bool:
    """Check if the orgweb image exists in the Docker environment"""
    try:
        docker.images.get(img)
        return True
    except ImageNotFound:
        return False
# Images Utility Functions:1 ends here

# [[file:../org/orgweb/container.org::*Containers Utility Functions][Containers Utility Functions:1]]
def create_container(volume: dict, container: str='orgweb', img:
                     str='localbuild:orgweb') -> None:
    """Create the orgweb container from the orgweb image"""
    return docker.containers.run(img,
                                 detach=True,
                                 tty=True,
                                 stdin_open=True,
                                 name=container,
                                 volumes=volume)

def container_exists(container: str='orgweb') -> bool:
    """Check if the orgweb container exists in the Docker environment"""
    try:
        docker.containers.get(container)
        return True
    except NotFound:
        return False

def container_running(container: str='orgweb') -> bool:
    """Check if the orgweb container is running in the Docker environment"""
    try:
        if docker.containers.get(container).status == 'running':
            return True
        else:
            return False
    except NotFound:
        return False

def delete_container(container: str='orgweb') -> None:
    """Delete the orgweb container from the Docker environment"""
    docker.containers.get(container).remove(force=True)
# Containers Utility Functions:1 ends here

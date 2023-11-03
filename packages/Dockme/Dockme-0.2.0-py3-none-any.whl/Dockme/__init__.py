version = "0.2.0"


def hello():
    print('Hello from Dockme in Version:', version)


def get_version():
    print('Version:', version)



from .get_image import pull_image
from .run_container import run_container
from .stop_container import stop_container
from .delet_container import del_container
from .delet_image import del_image
from .run_command_in_con import run_command
from .simple_funtion import ls_image, ls_container, ls_running_container
from .start_stop_compose import stop_compose, run_compose
from .funkt_classes import nginx_container, ubuntu_container
from .run_portainer import run_portainer



__all__ = [
    'pull_image',
    'run_container',
    'stop_container',
    'del_container',
    'del_image',
    'run_command',
    'ls_images',
    'ls_container',
    'ls_running_container',
    'run_compose',
    'stop_compose',
    'nginx_container',
    'ubuntu_container',
    'run_portainer'
]
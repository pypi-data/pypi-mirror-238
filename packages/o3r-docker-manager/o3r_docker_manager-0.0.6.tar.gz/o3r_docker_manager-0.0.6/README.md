# O3R docker manager

## Why this library exists

The o3r camera system is setup to facilitate the usage of docker containers to deploy applications to the VPU (OVPxxx).

The ifm3d c++/python api allows a developer to write applications using the o3r on their local machine and then recompile those applications to run directly on the VPU with minimal overhead. This library incorporates lesson from the ifm3d.com documentation on docker implementations. For each robust production ready solution a few common tools and practices are standard. An opinionated set of these tools are provided by this o3r deployment library to facilitate convenient and reliable deployment of 3rd party applications to the o3r platform.

- System for setting up and sharing a common directory between the running application and the rest of the VPU (see docker volumes documentation)
- Reccommended log cache file structure and logging tools for python (and soon c++)
- System for collating application logs in a consistent way whenever the developer connects to the vpu to perform updates/troubleshooting
- "One-click" solution deployment scripting

The following architecture is prescribed to minimize feedback loops during the development process:

![](schematic.drawio.svg)


## Quick start (from source)

`pip install -e ./o3r_docker_manager`

Check out the deployment example for all of the components needed for a baseline production python application...

```
cd deployment_examples
docker build --platform linux/arm64 -f "python_deps.Dockerfile" . -o "type=tar,dest=docker_python_deps.tar"
python3 manage.py
```

## What's happening under the hood

The o3r_docker_manager manage() call performs a sequence of operations standard for deployment of docker containers to the VPU, It will log any system calls that it makes on the VPU so that you can see what it's up to and what might have gone wrong. The arguments are structured in order of when the information is used by the manager and when the corresponding task is accomplished.

from o3r_docker_manager --help:

```
optional arguments:
  -h, --help            show this help message and exit
  --IP IP               IP address to be used, defaults to environment variable 'IFM3D_IP' if present, otherwise camera default: '192.168.0.69'
  --log_level LOG_LEVEL
                        log file level (DEBUG,..,EXCEPTION), Defaults to 'INFO'
  --log_dir LOG_DIR     directory to store log files, no log_dir means no log file, Defaults to '~/o3r_logs'
  --get_logs_from_vpu GET_LOGS_FROM_VPU
                        specifies how to cache logs from VPU and won't cache anything if blank, Defaults to '/home/oem/share/logs>~/o3r_logs/From_VPUs'
  --set_vpu_name SET_VPU_NAME
                        What to update the name of the vpu to. If empty, will not assign a name to the attached vpu, Defaults to 'o3r_docker_manager_test_000'
  --remove_running_containers
                        Whether or not to stop and remove all running containers, Defaults to False
  --dont_remove_running_containers
  --remove_volumes      Whether or not to remove all docker volumes Defaults to False
  --dont_remove_volumes
  --remove_images       Whether or not to remove all stored docker images that have been loaded into docker, Defaults to False
  --dont_remove_images
  --mount_usb_volumes   Whether or not to trigger vpu system command to mount external storage, Defaults to False
  --dont_mount_usb_volumes
  --dirs_to_make DIRS_TO_MAKE [DIRS_TO_MAKE ...]
                        List of directories to create on the vpu, Defaults to ['~/share']
  --transfers_from_vpu TRANSFERS_FROM_VPU [TRANSFERS_FROM_VPU ...]
                        List of files/directories to transfer to the vpu as "src,dst" pairs, Defaults to []
  --transfers_to_vpu TRANSFERS_TO_VPU [TRANSFERS_TO_VPU ...]
                        List of files/directories to transfer to the vpu as "src,dst" pairs, Defaults to []
  --volume_to_setup volume_to_setup
                        Path/to/directory/to/mount and volume_name separated by comma. If empty, will not create a volume, Defaults to ''
  --image_to_import IMAGE_TO_IMPORT
                        Path/to/docker_image.tar on vpu and image_name separated by comma. If empty, will not load an image, Defaults to ''
  --items_to_cleanup ITEMS_TO_CLEANUP
                        List of files/directories to remove from the vpu as pc/path or pc/path,vpu/path, Defaults to ''
  --enable_autostart ENABLE_AUTOSTART
                        List of docker-compose.yml:service_name pairs, separated by commas. Note that --setup_docker_compose option must be used or have been used for each container previously, Defaults to ''
  --disable_autostart DISABLE_AUTOSTART
                        List of container names separated by commas, Defaults to ''
  --docker_compose_to_initialize DOCKER_COMPOSE_TO_INITIALIZE
                        Name of the docker-compose yaml file to initialize. If empty, will not (re)initialize container, Defaults to ''
  --attach_to ATTACH_TO
                        Name of the container to attach to. If empty, will not attach to container, Defaults to ''
  --run_duration RUN_DURATION
                        Duration to run container for in seconds. If 0, will run indefinitely. Defaults to 0
  --stop_upon_exit      Defaults to False
  --dont_stop_upon_exit
```

## Troubleshooting

...

## Recommended:

Use exported functions as primitives for testing applications in controlled environments directly on the vpu. Begin by understanding the structure of the basic deployment_example project.
#############################################
# Copyright 2021-present ifm electronic, gmbh
# SPDX-License-Identifier: Apache-2.0
#############################################

# %%#########################################
# Some boilerplate for automating deployment
# of dockerized applications.
#############################################

import os
from pathlib import Path
import argparse
import sys
import logging
import time
from datetime import datetime
import subprocess
import shlex
import select
import threading
from pprint import pformat

from paramiko import AutoAddPolicy
from paramiko.client import SSHClient
from scp import SCPClient, SCPException
import yaml

try:
    import ifm3dpy
    USING_IFM3DPY = True
except ImportError:
    USING_IFM3DPY = False

try:
    from oem_logging import setup_log_handler
except ImportError:
    from .oem_logging import setup_log_handler

DEFAULT_IP = "192.168.0.69"

USING_IPYTHON = "ipykernel" in sys.modules

if USING_IPYTHON:
    logger = logging.getLogger("notebook")
else:
    logger = logging.getLogger("deploy")


def configure_logging(logger: logging.Logger, log_level: str = "", log_dir: str = "~/o3r_logs")-> str:
    """
    Configures logging to console and file

    If log level is not specified, only console logging is configured and defaults to INFO level

    Parameters
    ----------
    logger : logging.Logger
        logger to configure
    log_level : str, optional
        string level representation one of {"","DEBUG","INFO","CRITICAL","EXCEPTION",...}, by default ""
    log_dir : str, optional
        path to log directory, by default "~/o3r_logs"
    """
    # Setup console logging
    log_format = "%(asctime)s:%(filename)-8s:%(levelname)-8s:%(message)s"
    datefmt = "%y.%m.%d_%H.%M.%S"
    if not log_level:
        console_log_level = logging.INFO
    else:
        console_log_level = logging.getLevelName(log_level)
    logging.basicConfig(format=log_format,
                        level=console_log_level, datefmt=datefmt)

    ts_format = "%y.%m.%d_%H.%M.%S%z"
    now = datetime.now().astimezone()
    now_local_ts = now.strftime(ts_format)
    # Add log file handler
    if log_dir:
        log_file = setup_log_handler(
            logger=logger,
            total_cached_log_size=-1, # no pruning of logs, not rollover of log file
            log_dir=log_dir,
            log_series_name="Deployments",
            t_initialized=now_local_ts,
        )
    else:
        log_file = ""
    return log_file


def device_present(IP: str = os.environ.get("IFM3D_IP", DEFAULT_IP), USING_IFM3DPY: bool= ("ipykernel" in sys.modules)) -> bool:
    if USING_IFM3DPY:
        logger.info(f"Using ifm3dpy=={ifm3dpy.__version__}")
    else:
        logger.info("ifm3dpy unavailable")

    if USING_IFM3DPY:
        o3r = ifm3dpy.O3R()
        config = o3r.get()
        logger.info(f"VPU is connected at {IP}")
        device_found = True
    else:
        logger.info("Trying to connect to VPU without ifm3d")
        with subprocess.Popen(['ping', IP], stdout=subprocess.PIPE) as process:
            # Get rid of the first line output from the ping cmd
            output = process.stdout.readline().decode()
            device_found = False
            while True:
                output = process.stdout.readline().decode()
                if "unreachable".lower() in output.lower():
                    break
                if "bytes" and IP in output:
                    device_found = True
                    break
        logger.info(
            f"Device is { {False: 'not ',True:''}[device_found]}connected at {IP}")

    return device_found


def SSH_collect_VPU_handles(oem_username: str = "oem", password: str = "oem", IP: str = DEFAULT_IP, port: int = 22, remove_known_host: bool = True) -> (SSHClient, SCPClient):
    """
    This function collects the ssh and scp handles for the vpu

    Parameters
    ----------
    oem_username : str, optional
        By default "oem"
    password : str, optional
        By default "oem"
    IP : str, optional
        By default "192.168.0.69"
    port : int, optional
        By default 22
    remove_known_hosts : bool, optionally remove the entry for this IP from the known_hosts file after connecting (useful when simultaneously sshing into system via cli),
        By default True

    Returns
    -------
    tuple[SSHClient, SCPClient]
        ssh and scp handles for the vpu

    Raises
    ------
    Exception
        If the vpu cannot be connected to
    """

    logging.getLogger("paramiko").setLevel(logging.INFO)
    logging.getLogger("scp").setLevel(logging.INFO)

    ssh: SSHClient = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh.connect(hostname=IP, username=oem_username,
                    password=password, timeout=1, port=port)
    except Exception as FailureToConnectError:
        if "timed out" in str(FailureToConnectError):
            logger.info(
                f"Attempt to connect to {oem_username}@{IP}:{port} timed out.")
        raise FailureToConnectError

    scp = SCPClient(ssh.get_transport())

    known_hosts_path = Path("~/.ssh/known_hosts").expanduser()
    if remove_known_host and known_hosts_path.exists():
        with open(known_hosts_path, "r") as f:
            lines = f.readlines()
        with open(known_hosts_path, "w") as f:
            f.write(
                "\n".join([line for line in lines if not (line.split(" ")[0] == IP)]))

    return ssh, scp


def SSH_listdir(ssh: SSHClient, path: str = "~") -> [str]:
    """
    This function lists the contents of a directory via SSH

    Parameters
    ----------
    ssh : SSHClient
        ssh library native handle
    path : str, optional
        path to check, by default "~"

    Returns
    -------
    bool
        list of contents of the directory
    """
    cmd = f"ls {path}"
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    return _stdout.read().decode().strip().split("\n")


def SSH_path_exists(ssh: SSHClient, path: str = "~") -> bool:
    """
    This function checks whether a path exists

    Parameters
    ----------
    ssh : SSHClient
        ssh library native handle
    path : str, optional
        path to check, by default "~"

    Returns
    -------
    bool
        Whether the path exists
    """
    cmd = f"cd {path}"
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    if _stderr.read():
        tokenized_path = path.split("/")
        if len(tokenized_path) > 1:
            contents_of_parent = SSH_listdir(
                ssh, "/".join(tokenized_path[:-1]))
            path_exists = tokenized_path[-1] in contents_of_parent
        else:
            path_exists = False
    else:
        path_exists = True
    return path_exists


def SSH_isdir(ssh: SSHClient, path: str = "~") -> bool:
    """
    This function checks whether a path exists and is a directory

    Parameters
    ----------
    ssh : SSHClient
        ssh library native handle
    path : str, optional
        path to check, by default "~"

    Returns
    -------
    bool
        Whether the path exists and is a directory
    """
    cmd = f"cd {path}"
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    return not bool(_stderr.read().decode())


def SSH_makedirs(ssh: SSHClient, path: str = "")-> None:
    """
    This function makes directories via SSH

    Parameters
    ----------
    ssh : SSHClient
        ssh library native handle
    path : str, optional
        path to check, by default ""

    Raises
    ------
    Exception
        If the path or one of its parents exists but is not a directory
    """
    sub_path_to_check = []
    if path[-1] != "/":
        path += "/"
    for dir in path.split("/"):
        if sub_path_to_check:
            sub_path = "/".join(sub_path_to_check)
            if not SSH_isdir(ssh, sub_path):
                if SSH_path_exists(ssh, sub_path):
                    logger.exception(
                        f"Error making directories, {path}, via SSH. {sub_path} is not a directory")
                    raise Exception(
                        f"Error making directories, {path}, via SSH. {sub_path} is not a directory")
                else:
                    _stdin, _stdout, _stderr = ssh.exec_command(
                        f"mkdir {sub_path}")
        sub_path_to_check += [dir]


def transfer_item(ssh: SSHClient,scp: SCPClient, src: str, dst: str, src_is_local: bool = True)->None:
    """
    This function transfers a file or directory between the local machine and the vpu

    Parameters
    ----------
    ssh : SSHClient
        ssh library native handle
    scp : SCPClient
        scp library native handle
    src : str
        path to source file or directory
    dst : str
        path to destination file or directory
    src_is_local : bool, optional
        Whether the source is local or remote, by default True
    """
    if src_is_local:
        if Path(src).exists():
            if Path(src).is_dir():
                dst = "/".join(dst.split("/")[:-1])
                if not SSH_path_exists(ssh, dst):
                    SSH_makedirs(ssh, dst)
                scp.put(
                    files=[src],
                    remote_path=dst, recursive=True)
            else:
                scp.put(
                    files=[src],
                    remote_path=dst)
    else:
        if SSH_path_exists(ssh, src):
            if SSH_isdir(ssh, src):
                scp.get(src, dst, recursive=True)
            else:
                scp.get(src, dst)

def get_vpu_sn(IP: str = os.environ.get("IFM3D_IP", DEFAULT_IP)) -> str:
    """
    This function gets the serial number of the vpu

    Parameters
    ----------
    IP : str, optional
        IP address of the vpu, by default os.environ.get("IFM3D_IP", DEFAULT_IP)

    Returns
    -------
    str
        serial number of the vpu
    """
    o3r = ifm3dpy.O3R(IP)
    vpu_config = o3r.get(["/device/info/serialNumber"])
    sn = vpu_config['device']["info"]["serialNumber"]
    return sn

def get_vpu_name(IP: str = os.environ.get("IFM3D_IP", DEFAULT_IP)) -> str:
    """
    This function gets the name of the vpu

    Parameters
    ----------
    IP : str, optional
        IP address of the vpu, by default os.environ.get("IFM3D_IP", DEFAULT_IP)

    Returns
    -------
    str
        name of the vpu
    """
    o3r = ifm3dpy.O3R(IP)
    vpu_config = o3r.get(["/device/info/name"])
    name = vpu_config["device"]["info"]["name"]
    return name

def get_logs(vpu_log_dir: str, local_log_cache: str, IP: str, ssh: SSHClient, scp: SCPClient) -> None:
    """
    This function caches logs from the vpu to the local machine

    Parameters
    ----------
    vpu_log_dir : str
        path to logs on vpu
    local_log_cache : str
        path to cache logs to on local machine
    IP : str
        IP address of vpu
    ssh : SSHClient
        ssh library native handle
    scp : SCPClient
        scp library native handle
    """
    if SSH_path_exists(ssh, vpu_log_dir):
        sn = get_vpu_sn(IP)
        name = get_vpu_name(IP)
        vpu_specific_log_cache_dir_name = f"sn{sn}"
        if name:
            vpu_specific_log_cache_dir_name += "_"+name

        local_log_cache = Path(local_log_cache).expanduser().absolute()
        vpu_specific_local_cache_path = local_log_cache/vpu_specific_log_cache_dir_name

        logger.info(
            f"Merging {vpu_log_dir} into {vpu_specific_local_cache_path}")
        # There is some arbitrary behavior around how directories get merged when using scp get but the following works around it
        if not vpu_specific_local_cache_path.parent.exists():
            os.makedirs(vpu_specific_local_cache_path.parent)
        elif vpu_specific_local_cache_path.exists():
            for item in SSH_listdir(ssh, vpu_log_dir):
                scp.get(vpu_log_dir+"/"+item,
                        vpu_specific_local_cache_path, recursive=True)
        else:
            scp.get(vpu_log_dir, vpu_specific_local_cache_path, recursive=True)
    else:
        logger.info(
            f"No logs found at {vpu_log_dir}, directory does not exist"
        )


def docker_cleanup(ssh, remove_running_containers, remove_volumes, remove_images) -> None:
    """
    This function stops and removes all running containers, images, and volumes

    Parameters
    ----------
    ssh : SSHClient
        ssh library native handle
    remove_running_containers : bool
        Whether to stop all running containers
    remove_volumes : bool
        Whether to remove all volume links (essential to modify a volume and does not affect the mounted directory)
    remove_images : bool
        Whether to remove all images previously loaded into docker
    """
    cmd = "docker ps -a"
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    running_containers_list = _stdout.read().decode().strip().split("\n")
    header = running_containers_list[0]
    id_index = 0
    image_index = header.index("IMAGE")
    running_containers = running_containers_list[1:]
    logger.info(f"Running containers = {running_containers}")
    if remove_running_containers:
        for running_container in running_containers:
            id = running_container[id_index:image_index].strip()
            cmd = f"docker rm -f {id}"
            logger.info(cmd)
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(f">>>{_stdout.read().decode().strip()}")

    cmd = "docker image ls"
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    cached_images_list = _stdout.read().decode().strip().split("\n")
    header = cached_images_list[0]
    cached_images = cached_images_list[1:]
    id_index = header.index("IMAGE ID")
    created_index = header.index("CREATED")
    logger.info(f"Cached images = {cached_images}")
    if remove_images:
        for cached_container in cached_images:
            id = cached_container[id_index:created_index].strip()
            cmd = f"docker image rm {id}"
            logger.info(cmd)
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(f">>>{_stdout.read().decode().strip()}")

    cmd = "docker volume ls"
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    cached_images_list = _stdout.read().decode().strip().split("\n")
    header = cached_images_list[0]
    cached_images = cached_images_list[1:]
    vol_name_index = header.index("VOLUME NAME")
    logger.info(f"Existing_volumes = {cached_images}")
    if remove_volumes:
        for cached_container in cached_images:
            id = cached_container[vol_name_index:].strip()
            cmd = f"docker volume rm {id}"
            logger.info(cmd)
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(f">>>{_stdout.read().decode().strip()}")


def docker_build(docker_build: str):
    """
    This function builds a docker container.

    Parameters
    ----------
    docker_build : str
        simplified string representation of the docker build command
    """
    if "ipykernel" in sys.modules:
        logger.info(
            """...\n...Cannot show output while building container via ipython...\n...If desired, try running the command in a separate terminal: """)

    logger.info(f"Attempting docker build")

    dockerfile_path, docker_build_output_path = docker_build.split(">")
    timeout_building_docker = 1000

    if Path(dockerfile_path).absolute().exists():
        dockerfile_path
    elif not Path(dockerfile_path).exists():
        raise Exception(f"No dockerfile path found at: {dockerfile_path}")

    cmd = f'docker build --platform linux/arm64 -f "{dockerfile_path}" . -o "type=tar,dest={docker_build_output_path}"'
    if os.name == "nt":
        logger.info(f"Attempting docker build via WSL...")
        cmd = "wsl " + cmd

    logger.info(cmd)

    start = time.perf_counter()
    with subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    ) as process:
        buffer = ""
        while time.perf_counter() < start+timeout_building_docker:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                buffer += output
                print(output.strip().decode())


def run_read_print_ssh_loop(ip: str, cmd: str, stop_loop, timeout: int = 0, output_buffer: str = "") -> str:
    """
    This function runs a command on the remote device and prints the output to the console

    Parameters
    ----------
    ip : str
        IP address of the remote device
    cmd : str
        command to run on the remote device
    timeout : int, optional
        How long to print output with 0 being indefinite, by default 0

    Returns
    -------
    str
        output of the command
    """
    ssh, scp = SSH_collect_VPU_handles(IP=ip)
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.exec_command(cmd)

    start = time.perf_counter()
    while not channel.exit_status_ready() and (not timeout or time.perf_counter() < start+timeout) and not stop_loop():
        rl, wl, xl = select.select([channel], [], [], 0.0)
        if len(rl) > 0:
            # Must be stdout
            output = channel.recv(1024).decode()
            if output:
                print(output, end="")
                output_buffer += [output]
    return output_buffer


def stop_container(ssh, container_name):
    cmd = f"docker rm -f {container_name}"
    logger.info(f"Stopping container with: {cmd}")
    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
    logger.info(">>>" + _stdout.read().decode().strip() +
                _stderr.read().decode().strip())


def manage(
    IP: str = os.environ.get("IFM3D_IP", DEFAULT_IP),
    log_level: str = "INFO",
    log_dir: str = "~/o3r_logs",
    get_logs_from_vpu: str = "/home/oem/share/logs>~/o3r_logs/From_VPUs",
    set_vpu_name: str = "o3r_docker_manager_test_000",

    remove_running_containers: bool = False,
    remove_volumes: bool = False,
    remove_images: bool = False,

    mount_usb_volumes: bool = False,
    dirs_to_make: list[str] = ["~/share"],
    transfers_from_vpu: list[str] = [],
    transfers_to_vpu: list[str] = [],

    volume_to_setup: str = "",
    image_to_import: str = "",
    items_to_cleanup: str = "",

    enable_autostart: str = "",
    disable_autostart: str = "",

    docker_compose_to_initialize: str = "",
    attach_to: str = "",
    run_duration: int = 0,
    stop_upon_exit: bool = False,

    **kwargs
):
    ...
    # %%#####################################
    # Check Arguments, most default arguments are overridden if running interactively
    #########################################
    if USING_IPYTHON:

        # for testing in ipython... copy arguments from above into here so that ipython testing works
        ...

    else:
        parser = argparse.ArgumentParser(
            description="""Wrapper of O3R docker functionality for somewhat opinionated deployment of dockerized applications. Functions are executed in order of their appearance in the help message.""",
        )

        parser.add_argument(
            "--IP", type=str, default=DEFAULT_IP, help=f"IP address to be used, defaults to environment variable 'IFM3D_IP' if present, otherwise camera default: '{DEFAULT_IP}'"
        )
        parser.add_argument(
            "--log_level", type=str, default=log_level, help=f"log file level (DEBUG,..,EXCEPTION), Defaults to '{log_level}'"
        )
        parser.add_argument(
            "--log_dir", type=str, default=log_dir, help=f"directory to store local deployment log files, no log_dir means no log file, Defaults to '{log_dir}'"
        )
        parser.add_argument(
            "--get_logs_from_vpu", type=str, default=get_logs_from_vpu, help=f"specifies how to cache logs from VPU and won't cache anything if blank, Defaults to '{get_logs_from_vpu}'"
        )
        parser.add_argument(
            "--set_vpu_name", type=str, default=set_vpu_name, help=f"What to update the name of the vpu to. If empty, will not assign a name to the attached vpu, Defaults to '{set_vpu_name}'"
        )

        parser.add_argument('--remove_running_containers', action='store_true',
                            help=f"Whether or not to stop and remove all running containers, Defaults to {remove_running_containers}")
        parser.set_defaults(remove_running_containers=remove_running_containers)

        parser.add_argument('--remove_volumes', action='store_true',
                            help=f"Whether or not to remove all docker volumes Defaults to {remove_volumes}")
        parser.set_defaults(remove_volumes=remove_volumes)

        parser.add_argument('--remove_images', action='store_true',
                            help=f"Whether or not to remove all stored docker images that have been loaded into docker, Defaults to {remove_images}")
        parser.set_defaults(remove_images=remove_images)

        parser.add_argument('--mount_usb_volumes', action='store_true',
                            help=f"Whether or not to trigger vpu system command to mount external storage, Defaults to {mount_usb_volumes}")
        parser.set_defaults(mount_usb_volumes=mount_usb_volumes)
        parser.add_argument("--dirs_to_make", type=str, nargs="+", default = dirs_to_make, help=f"List of directories to create on the vpu, Defaults to {dirs_to_make}")
        parser.add_argument('--transfers_from_vpu', action='store', type=str, nargs="+", default = transfers_from_vpu, help=f'List of files/directories to transfer to the vpu as "src,dst" pairs, Defaults to {transfers_from_vpu}')
        parser.add_argument('--transfers_to_vpu', action='store', type=str, nargs="+", default = transfers_to_vpu, help=f'List of files/directories to transfer to the vpu as "src,dst" pairs, Defaults to {transfers_to_vpu}')

        parser.add_argument(
            "--volume_to_setup", type=str, default=volume_to_setup, help=f"Path/to/directory/to/mount and volume_name separated by comma. If empty, will not create a volume, Defaults to '{volume_to_setup}'"
        )
        parser.add_argument(
            "--image_to_import", type=str, default=image_to_import, help=f"Path/to/docker_image.tar on vpu and image_name separated by comma. If empty, will not load an image, Defaults to '{image_to_import}'"
        )
        parser.add_argument(
            "--items_to_cleanup", type=str, default=items_to_cleanup, help=f"List of files/directories to remove from the vpu as pc/path or pc/path,vpu/path, Defaults to '{items_to_cleanup}'"
        )

        parser.add_argument(
            "--enable_autostart", type=str, default=enable_autostart, help=f"List of docker-compose.yml:service_name pairs, separated by commas. Note that --setup_docker_compose option must be used or have been used for each container previously, Defaults to '{enable_autostart}'",
        )
        parser.add_argument(
            "--disable_autostart", type=str, default=disable_autostart, help=f"List of container names separated by commas, Defaults to '{disable_autostart}'",
        )

        parser.add_argument(
            "--docker_compose_to_initialize", type=str, default=docker_compose_to_initialize, help=f"Name of the docker-compose yaml file to initialize. If empty, will not (re)initialize container, Defaults to '{docker_compose_to_initialize}'"
        )
        parser.add_argument(
            "--attach_to", type=str, default=attach_to, help=f"Name of the container to attach to. If empty, will not attach to container, Defaults to '{attach_to}'"
        )
        parser.add_argument(
            "--run_duration", type=int, default=run_duration, help=f"Duration to run container for in seconds. If 0, will run indefinitely. Defaults to {run_duration}"
        )
        parser.add_argument(
            "--stop_upon_exit", action='store_true', help=f"Defaults to {stop_upon_exit}"
        )
        parser.set_defaults(stop_upon_exit=stop_upon_exit)
        
        args = parser.parse_args()

        IP = args.IP
        log_dir = args.log_dir
        log_level = args.log_level
        get_logs_from_vpu = args.get_logs_from_vpu
        set_vpu_name = args.set_vpu_name

        remove_running_containers = args.remove_running_containers
        remove_volumes = args.remove_volumes
        remove_images = args.remove_images

        mount_usb_volumes = args.mount_usb_volumes
        dirs_to_make = args.dirs_to_make
        transfers_from_vpu = args.transfers_from_vpu
        transfers_to_vpu = args.transfers_to_vpu

        volume_to_setup = args.volume_to_setup
        image_to_import = args.image_to_import
        items_to_cleanup = args.items_to_cleanup

        enable_autostart = args.enable_autostart
        disable_autostart = args.disable_autostart

        docker_compose_to_initialize = args.docker_compose_to_initialize
        attach_to = args.attach_to
        run_duration = args.run_duration
        stop_upon_exit = args.stop_upon_exit

    # %%#####################################
    # Configure logging to file
    #########################################
    log_file_path = configure_logging(logger, log_level, log_dir)

    # %%#####################################
    # Check if vpu is present
    #########################################

    if not device_present(IP, USING_IFM3DPY):
        logger.info("device not found, exiting...")
        sys.exit(0)

    # %%#####################################
    # configure ssh and scp handles
    #########################################

    ssh, scp = SSH_collect_VPU_handles(IP=IP)

    # %%#####################################
    # make directories as specified
    #########################################

    for dir_to_make in dirs_to_make:
        if not SSH_path_exists(ssh, dir_to_make):
            cmd = f"mkdir {dir_to_make}"
            logger.info(cmd)
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(
                f">>> {_stderr.read().decode().strip()} {_stdout.read().decode().strip()}")

    # %%#####################################
    # Perform any file transfers called for explicitly by arguments
    #########################################
    
    def expand_pc_path(pc_path):
        pc_path = pc_path.replace("~", str(Path().home()))
        pc_path = pc_path.replace(
            "./", str(Path(os.getcwd()))+"/").replace("\\", "/")
        return pc_path
    def expand_vpu_path(vpu_path):
        vpu_path = vpu_path.replace("~", "/home/oem")
        return vpu_path

    for transfer_to_vpu in transfers_to_vpu:
        src, dst = transfer_to_vpu.split(",")
        src = expand_pc_path(src)
        dst = expand_vpu_path(dst)
        if Path(src).exists():
            logger.info(
                f"transferring {src} to {dst}")
            transfer_item(
                ssh, scp, src, dst, True)
        else:
            logger.info(f"file not found '{src}'")

    for transfer_from_vpu in transfers_from_vpu:
        src = expand_vpu_path(src)
        dst = expand_pc_path(dst)
        src, dst = transfer_to_vpu.split(",")
        if SSH_path_exists(ssh, src):
            logger.info(
                f"Transferring {src} to {dst}")
            transfer_item(
                ssh, scp, src, dst, False)
        else:
            logger.info(f"file not found '{src}'")

    # %%#####################################
    # set device name if desired
    #########################################

    if USING_IFM3DPY and set_vpu_name:
        logger.info(f"Setting device name to {set_vpu_name}")
        o3r = ifm3dpy.O3R(IP)
        o3r.set({"device": {"info": {"name": set_vpu_name}}})

    # %%#####################################
    # stop/remove/delete all other containers
    #########################################

    docker_cleanup(ssh, remove_running_containers,
                         remove_volumes, remove_images)
    
    # %%#####################################
    # Sync logs from vpu if requested
    #########################################

    if USING_IFM3DPY and get_logs_from_vpu:
        vpu_log_dir, local_log_cache = get_logs_from_vpu.split(">")

        get_logs(
            vpu_log_dir=vpu_log_dir,
            local_log_cache=local_log_cache,
            IP=IP,
            scp=scp,
            ssh=ssh,
        )

    # %%#####################################
    # mount any usb devices (run corresponding command on vpu)
    #########################################

    if mount_usb_volumes:
        cmd = f"mount"
        logger.info(cmd)
        _stdin, _stdout, _stderr = ssh.exec_command(cmd)
        logger.info(">>>"+_stdout.read().decode().strip() +
                    _stderr.read().decode().strip())

    # %%#####################################
    # setup volume
    #########################################
    if volume_to_setup:
        # setup volume as specified
        path_for_volume_to_mount, volume_name = volume_to_setup.split(",")
        cmd = f'docker volume create --driver local -o o=bind -o type=none -o device="{path_for_volume_to_mount}" {volume_name}'
        _stdin, _stdout, _stderr = ssh.exec_command(cmd)
        logger.info(cmd)
        if _stdout.read().decode().strip() == volume_name:
            logger.info("Success!")
        else:
            logger.info("Issue encountered while setting up shared volume")
            raise Exception(_stderr.read().decode().strip())
        
    # %%#####################################
    # load docker image
    #########################################
    if image_to_import:
        # load image
        docker_image_fname = Path(image_to_import).name
        logger.info("importing image into vpu docker storage")
        cmd = f"cat {image_to_import}| docker import - {docker_image_fname[:-4]}"
        logger.info(cmd)
        _stdin, _stdout, _stderr = ssh.exec_command(cmd)
        logger.info(">>>"+_stdout.read().decode().strip() +
                    _stderr.read().decode().strip())
        
    # %%#####################################
    # remove files after setting up docker eg. .tar file
    #########################################
    if items_to_cleanup:
        for item_to_cleanup in items_to_cleanup.split(","):
            if SSH_path_exists(ssh, item_to_cleanup):
                logger.info(f"Removing {item_to_cleanup}")
                if SSH_isdir(ssh, item_to_cleanup):
                    cmd = f"rm -r {item_to_cleanup}"
                    logger.info(cmd)
                    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
                    logger.info(_stdout.read().decode().strip() +
                                _stderr.read().decode().strip())
                else:
                    cmd = f"rm {item_to_cleanup}"
                    logger.info(cmd)
                    _stdin, _stdout, _stderr = ssh.exec_command(cmd)
                    logger.info(_stdout.read().decode().strip() +
                                _stderr.read().decode().strip())

    # %%#####################################
    # enable or disable autostart as specified
    #########################################

    if enable_autostart:
        for container_info in enable_autostart.split(","):
            docker_compose_fname, container_name = container_info.split(":")
            # check if symlink already exists
            docker_compose_dir = f"/usr/share/oem/docker/compose/deploy/"

            docker_compose_vpu_path = docker_compose_dir+"/docker-compose.yml"

            if not SSH_path_exists(ssh, docker_compose_vpu_path):
                logger.info(
                    "no docker-compose symlink for auto-start found, setting it up now")
                SSH_makedirs(ssh, docker_compose_dir)
                docker_compose_home = "~/"+docker_compose_fname
                cmd = f"ln -s {docker_compose_home} {docker_compose_vpu_path}"
                logger.info(cmd)
                _stdin, _stdout, _stderr = ssh.exec_command(cmd)
                logger.info(
                    f">>> {_stderr.read().decode().strip()} {_stdout.read().decode().strip()}")

            logger.info("Enabling autostart...")
            cmd = f'systemctl --user enable oem-dc@{container_name}'
            logger.info(cmd)
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(
                f">>> {_stderr.read().decode().strip()} {_stdout.read().decode().strip()}")

    if disable_autostart:
        for container_name in disable_autostart.split(","):
            logger.info("disabling autostart...")
            cmd = f'systemctl --user disable oem-dc@{container_name}'
            logger.info(cmd)
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(
                f">>> {_stderr.read().decode().strip()} {_stdout.read().decode().strip()}")

    # %%#####################################
    # initialize and/or attach to a container
    #########################################

    initialized = False
    if docker_compose_to_initialize:
        docker_compose_fname, service_name = docker_compose_to_initialize.split(":")

        with open(docker_compose_fname, "r") as f:
            docker_compose = yaml.load(f, yaml.BaseLoader)
        logger.info(pformat(docker_compose))
        if "logging" in docker_compose["services"][service_name]:
            # detach from the container immediately
            cmd = f"docker-compose -f {docker_compose_fname} up --detach"
            _stdin, _stdout, _stderr = ssh.exec_command(cmd)
            logger.info(cmd)
            logger.info(
                f">>> {_stderr.read().decode().strip()} {_stdout.read().decode().strip()}")
            logger.info(
                f"{service_name} initialized from {docker_compose_fname}")

            initialized = True

    output_lines_from_container = []
    if attach_to:

        if not docker_compose_to_initialize or initialized:
            logger.info(f"Now Attempting to show output from {attach_to}...")
            cmd = f"docker attach {attach_to}"
        else:
            cmd = f"docker-compose -f {docker_compose_fname} up"
            logger.info(
                f"Initializing and showing output of container as it appears to be using the standard logger... {cmd}")

        stop_loop = False
        print_loop_thread = threading.Thread(
            target=run_read_print_ssh_loop,
            args=(IP, cmd, lambda: stop_loop, 0, output_lines_from_container),
            daemon=True
        )
        print_loop_thread.start()
        start_t = time.perf_counter()
        while not stop_loop:
            try:
                time.sleep(0.2)
                if run_duration and time.perf_counter() > start_t+run_duration:
                    logger.info(
                        f"run_duration of {run_duration} seconds has been reached, detaching from container...")
                    stop_loop = True
            except KeyboardInterrupt:
                logger.info(
                    "KeyboardInterrupt detected, Detaching from container...")
                stop_loop = True

        if stop_upon_exit:
            logger.info("Stopping container...")
            stop_container(ssh, container_name=attach_to)
            time.sleep(0.5)
        time.sleep(0.5)
        if not print_loop_thread.is_alive():
            print_loop_thread.join()
        else:
            logger.info(
                "Failed to stop container monitor thread... it will exit with the program exit")

        output_lines_from_container = output_lines_from_container.copy()
        del (print_loop_thread)
        time.sleep(1)
        time.sleep(1)

    # %%#####################################
    # return!
    ##########################################

    return {
        "log_file_path": log_file_path,
        "output_from_container": output_lines_from_container,
    }

    # %%#####################################
    # handle indent level in jupyter mode...
    #########################################


if __name__ == "__main__":
    manage()

# %%#####################################
#
##########################################

from RemoteOrchestratorPy import (RemoteTaskActionSequence,
                                  doit_taskify,
                                  get_leaf_task_label,
                                  FileConfig,
                                  setup_remote_debian 
                                  )
import sys
from fabric import Connection, Config
from pathlib import Path
import os
from doit.tools import run_once
import logging

# Configure logging
logging.basicConfig(
    filename='unit_test.log',        # Log file name
    level=logging.DEBUG,       # Minimum log level to capture
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    filemode='a'               # File mode: 'a' for append, 'w' for overwrite
)



ip = "192.168.0.102"
# === create rtas with fabric conn for 2 ssh users root and adming ===
cluster_resources_datadir="/home/adming/cluster_resources"
adming_public_key_file = "adming_ssh_rsa_public_key"
connect_kwargs = {
    "key_filename": f"{cluster_resources_datadir}/{adming_public_key_file}",
}
fabric_config = Config(overrides={
    'connect_kwargs': connect_kwargs,
    'run': {
        'hide': True,
        'warn': True,
        'echo': True
    },
})


fabric_conn_adming = Connection(host=ip,
                                user="adming",
                                config=fabric_config
                         )

rtas = RemoteTaskActionSequence(ip, ("adming", fabric_conn_adming),
                                
                                os_type="linux"
                                )
rtas.set_active_user("adming")

all_rtas = [rtas]

from . import remote_actions

openbsd_version="76"

remote_workdir = "/home/adming/netboot_admin"

@doit_taskify(all_rtas)
def setup_remote(rtas):
    yield from setup_remote_debian(rtas,
                                   "/home/adming/DrivingRange/CloudWorks/netboot_admin",
                                   remote_workdir,
                                   remote_actions,
                                   "/home/adming/.ssh/id_rsa")

    

sets = ["man",
        "base", "comp", "xbase", "xfont", "xserv",
        # "xshare"
    ]

target_nfs_dir = "/nfs/aa5e7587/root"
@doit_taskify(all_rtas, task_dep=[get_leaf_task_label(setup_remote)])
def upgrade_snapshot(rtas):
    remote_task_append = rtas.set_task_remote_step_iter()
    #  argument order
    #  the tuple for remote func execution command
    #  task label
    #  task kwargs
    for aset in sets: 
        remote_task_append(("wget_url",
                            [f"https://cdn.openbsd.org/pub/OpenBSD/snapshots/arm64/{aset}{openbsd_version}.tgz"],
                            {}
                            ),
                           f"{aset}_download_tgz", 
                           targets=[f"{remote_workdir}/{aset}{openbsd_version}.tgz"]
                           )
    remote_task_append(("wget_url",
                            [f"https://cdn.openbsd.org/pub/OpenBSD/snapshots/arm64/bsd.mp"],
                            {}
                            ),
                           f"bsd_mp_download", 
                           targets=[f"{remote_workdir}/bsd.mp"]
                           )        
        
    for aset in sets:
        remote_task_append(f"cd {target_nfs_dir}; sudo tar xzphf {remote_workdir}/{aset}{openbsd_version}.tgz",
                           f"untar_{aset}",
                           #uptodate=[run_once],
                           file_dep=[f"{remote_workdir}/{aset}{openbsd_version}.tgz"]

                           )
    remote_task_append(f"cd {target_nfs_dir}; sudo  cp {remote_workdir}/bsd.mp bsd",
                       f"update_bsd",
                       file_dep=[f"{remote_workdir}/bsd.mp"]
                       #uptodate=[run_once]
                       )
    
    yield from rtas

def task_final():
    return { 'actions': None,
             'task_dep': [
                 get_leaf_task_label(upgrade_snapshot)
             ]

        }        

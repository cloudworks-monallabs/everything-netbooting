from addict import Dict
import tomllib
import os
from pathlib import Path
from addict import Dict
from fabric import Connection, Config
from RemoteOrchestratorPy import (RemoteTaskActionSequence,
                                  doit_taskify,
                                  )


# the working directory on remote machine for deployment 
deployment_workdir=Path("/home/adming/deployment_store")
local_workdir=Path("/home/adming/DrivingRange/CloudWorks/deployment_service")
# the working directory for running doit pipeline
DOIT_WORKDIR = Path(os.environ['DOIT_WORKDIR'])
CLUSTER_RESOURCES_DATADIR= Path(os.environ['CLUSTER_RESOURCES_DATADIR'])

netboot_CCCmachine_ip="192.168.0.139"

connect_kwargs = {
    "key_filename": f"{CLUSTER_RESOURCES_DATADIR}/adming_ssh_rsa_public_key",
}
fabric_config = Config(overrides={
    'connect_kwargs': connect_kwargs,
    'run': {
        'hide': True,
        'warn': True,
        'echo': True
    },
})

netboot_CCCmachine_rtas=RemoteTaskActionSequence(netboot_CCCmachine_ip)
        #rtas_by_ip[ip].add_ssh_user("root", fabric_conn_root)
fabric_conn_adming = Connection(host=netboot_CCCmachine_ip,
                                user="adming",
                                config=fabric_config
                                )
netboot_CCCmachine_rtas.add_ssh_user("adming", fabric_conn_adming)
        
rtas_by_ip = { netboot_CCCmachine_ip: netboot_CCCmachine_rtas



    }

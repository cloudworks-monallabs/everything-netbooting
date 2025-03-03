from pathlib import Path
from .homelab_config import netboot_CCCmachine_rtas, CLUSTER_RESOURCES_DATADIR, deployment_workdir
from RemoteOrchestratorPy import (RemoteTaskActionSequence,
                       doit_taskify,
                       get_leaf_task_label,
                                  get_dangling_task,
                                  FileConfig,
                       )


from doit.tools import run_once


MACHINE_ID="aa5e7587"
BASE_DIR=f"/mnt/zfs_pool/nfs_data/per_machine_netboot_filesystem/{MACHINE_ID}"
MACHINE_IP="192.168.0.144"
temp_etc_exports_filepath = Path("/tmp/etc_exports")
@doit_taskify([netboot_CCCmachine_rtas])
def create_netboot_raspian_filesystem(rtas):

    def local_step_pre():
        exports_str="""/mnt/zfs_pool/nfs_data/netboot_raspian_root_common *(ro,no_subtree_check,no_root_squash,crossmnt,insecure)
"""
        for adir in ["etc", "home",  "root",  "var"]:
            exports_str += f"""{BASE_DIR}/{adir} {MACHINE_IP}(rw,sync,no_subtree_check,no_root_squash)

        
"""
        temp_etc_exports_filepath.write_text("/mnt/zfs_pool/nfs_data/netboot_raspian_root_common *(ro,no_subtree_check,no_root_squash,crossmnt,insecure)"

                )

        print (exports_str)
        temp_etc_exports_filepath.write_text(exports_str)
        
    rtas.set_task_local_step_pre(local_step_pre)

    rtas.set_task_ship_files_iter([FileConfig(temp_etc_exports_filepath,
                                             False,
                                             False,
                                             deployment_workdir/f"etc_exports_{MACHINE_ID}"

        )
                                   ],
                                  deployment_workdir

        )
    remote_task_append = rtas.set_task_remote_step_iter()
    remote_task_append(f"""
    # Create the base directory for the machine
    mkdir -p {BASE_DIR}

    # Essential directories to override
    mkdir -p "{BASE_DIR}/etc"
    mkdir -p "{BASE_DIR}/etc/network"
    mkdir -p "{BASE_DIR}/etc/netplan"
    mkdir -p "{BASE_DIR}/etc/ssh"

    mkdir -p "{BASE_DIR}/var"
    mkdir -p "{BASE_DIR}/var/log"
    mkdir -p "{BASE_DIR}/var/tmp"

    # Other machine-specific state (depends on your needs)
    mkdir -p "{BASE_DIR}/root"

    # If you want machine-specific user directories (like /home/<user>), do:
    mkdir -p "{BASE_DIR}/home"

    # Optional: Other directories you want to machine-specify
    mkdir -p "{BASE_DIR}/etc/systemd/system"
    mkdir -p "{BASE_DIR}/etc/cron.d"
    mkdir -p "{BASE_DIR}/etc/cron.daily"

    """,
                       "create_machine_specific_dirs",
                       uptodate=[run_once]
                       )

    remote_task_append(f"""sudo cp {deployment_workdir}/etc_exports_{MACHINE_ID} /etc/exports

    """,
                       "deploy_nfs_config",
                       file_dep=[f"{deployment_workdir}/etc_exports_{MACHINE_ID}"],
                       targets=["/etc/exports"]

        )

    yield from rtas

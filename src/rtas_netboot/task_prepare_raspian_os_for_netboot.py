#cluster_resources: Homelab
#. install dnsmasq
#. sudo apt-get install rsync dnsmasq nfs-util
#mkdir /tftpboot
#template dnsmasq.conf
#build dnsmasq.conf based on machines in the config toml

# upload dnsmasq.conf
#.
import pickle
from pathlib import Path
from .homelab_config import netboot_CCCmachine_rtas, CLUSTER_RESOURCES_DATADIR, deployment_workdir
from RemoteOrchestratorPy import (RemoteTaskActionSequence,
                       doit_taskify,
                       get_leaf_task_label,
                                  get_dangling_task,
                                  FileConfig,
                       )

#TODO: missing setup -- as of now mkdir deployment_store is done manually
#TODO: turn this into proper temp file with teardown
#TODO: define all the mount points in a config file
temp_etc_exports_filepath = Path("/tmp/etc_exports")
from doit.tools import run_once
@doit_taskify([netboot_CCCmachine_rtas])
def prepare_raspian_os_for_netboot(rtas):
    # ===================== prepare /etc/exports =====================

    def local_step_pre():

        nfs_export_directives = {}
        nfs_export_directives["/mnt/zfs_pool/nfs_data/netboot_raspian_root_common"] = "*(rw,sync,no_subtree_check,no_root_squash,crossmnt,insecure)"

        pickle.dump(nfs_export_directives,
                    Path(CLUSTER_RESOURCES_DATADIR/"exports.pickle").open("wb")
                    )

        temp_etc_exports_filepath.write_text("/mnt/zfs_pool/nfs_data/netboot_raspian_root_common *(ro,no_subtree_check,no_root_squash,crossmnt,insecure)"

                )
    rtas.set_task_local_step_pre(local_step_pre,
                                 targets=[CLUSTER_RESOURCES_DATADIR/"exports.pickle"
                                     ]

        )
    rtas.set_task_ship_files_iter([FileConfig(temp_etc_exports_filepath,
                                             False,
                                             False,
                                             deployment_workdir/"etc_exports"

        )
                                   ],
                                  deployment_workdir

        )
        
    remote_task_append = rtas.set_task_remote_step_iter()
    remote_task_append("""sudo apt-get install -y nfs-kernel-server

    """,
                       "install_nfs_service_package",
                       uptodate=[run_once]
                       
                       )

    # remote_task_append(f"sudo rsync -xa --progress --exclude /nfs/38136513 \     --exclude /etc/systemd/network/10-eth0.netdev \     --exclude /etc/systemd/network/11-eth0.network \     --exclude /etc/dnsmasq.conf \     / /nfs/38136513/"
    #                    )
    remote_task_append("""sudo rsync -aAXv /* /mnt/zfs_pool/nfs_data/netboot_raspian_root_common \
    --exclude=/dev/* \
    --exclude=/proc/* \
    --exclude=/sys/* \
    --exclude=/tmp/* \
    --exclude=/run/* \
    --exclude=/mnt/* \
    --exclude=/media/* \
    --exclude=/lost+found \
    --exclude=/etc/machine-id \
    --exclude=/etc/network/* \
    --exclude=/etc/netplan/* \
    --exclude=/var/log/* \
    --exclude=/var/tmp/* \
    --exclude=/var/cache/apt/archives/* \
    --exclude=/root/.bash_history \
    --exclude=/home/ \
    --exclude=/etc/ssh/ssh_host_* \
    --exclude=/swapfile \
    --numeric-ids \
    """,
                       "populate_root_partition",
                       uptodate=[run_once]
                       )

    remote_task_append(f"""sudo cp {deployment_workdir}/etc_exports /etc/exports

    """,
                       "deploy_nfs_config",
                       file_dep=[f"{deployment_workdir}/etc_exports"],
                       targets=["/etc/exports"]

        )
        # TODO: you probably need to edit /etc/nfs.conf to enable udp but we will see about that 
    

    remote_task_append(f"""sudo systemctl restart nfs-server

        """,
                           "start_nfs_server"
                           )


    yield from rtas
    
    
    pass

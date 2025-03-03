import os
import sys

#from . import upgrade_openbsd_snapshot
from . import doit_tasks
from .homelab_config import netboot_CCCmachine_rtas, rtas_by_ip
from RemoteOrchestratorPy import (RemoteTaskActionSequence,
                                  doit_taskify,
                                  get_leaf_task_label,
                                  FileConfig,
                                  setup_remote_debian,
                                  RTASExecutionError
                                  )

from doit_extntools.precompute_remote_file_md5sum import (pickle_compute_md5_remote_target_set,
                                                          precompute_remote_files_md5
                                                          )


from doit.cmd_base import ModuleTaskLoader
from doit.doit_cmd import DoitMain

DOIT_WORKDIR = os.environ['DOIT_WORKDIR']


def run():
    os.chdir(DOIT_WORKDIR)
    try:
        doit_main = DoitMain(ModuleTaskLoader(doit_tasks))
        precompute_remote_files_md5(rtas_by_ip)
        doit_main.run(sys.argv[1:]
                      )
    except Exception as e:
        print (f"Exception happend during task creation phase: {e}")

    finally:

        print ("deployment workflow executed without known errors")

    
    if netboot_CCCmachine_rtas.task_failed_abort_execution:
        raise RTASExecutionError(str(netboot_CCCmachine_rtas.task_failed_exception), netboot_CCCmachine_rtas)

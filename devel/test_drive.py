from rtas_netboot import run
import logging
logging.basicConfig(
    filename='everything_netboot.log',        # Log file name
    level=logging.DEBUG,       # Minimum log level to capture
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    filemode='a'               # File mode: 'a' for append, 'w' for overwrite
)

import sys

# if __name__ == "__main__":
#     from doit.cmd_base import ModuleTaskLoader
#     from doit.doit_cmd import DoitMain


#     try:
#         DoitMain(ModuleTaskLoader(sys.modules[__name__])).run(sys.argv[1:])
#     except Exception as e:
#         print (f"Exception happend during task pipeline execution: {e}")

#     finally:

#         print ("in final")





#get_compute_instances()
run()
#analyse()



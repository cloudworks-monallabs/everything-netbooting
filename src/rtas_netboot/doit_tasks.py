from .task_prepare_raspian_os_for_netboot import prepare_raspian_os_for_netboot
from .task_create_netboot_raspian_filesystem import create_netboot_raspian_filesystem

DOIT_CONFIG = {
    "verbosity": 2,
    'default_tasks' :  [#"prepare_raspian_os_for_netboot",
                        "create_netboot_raspian_filesystem"
                        
                        ],
    'continue': True
    
    
    }

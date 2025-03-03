
.. code-block::
   // copy the env of deployment service
   cd /home/adming/DrivingRange/CloudWorks/homelab_deployment
   export DOIT_WORKDIR=/home/adming/DrivingRange/CloudWorks/homelab_deployment
   export CLUSTER_RESOURCES_DATADIR=/home/adming/DrivingRange/CloudWorks/homelab_deployment/cluster_resources/
   export PYTHONPATH=/home/kabira/Development/cloudworks-monallabs/everything-netbooting/src:$PYTHONPATH
   export PYTHONPATH=/home/kabira/Development/cloudworks-monallabs/RemoteOrchestratorPy/src:$PYTHONPATH 


   rm deployment.log;  python3    /home/kabira/Development/cloudworks-monallabs/everything-netbooting/devel/test_drive.py

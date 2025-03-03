#. How to run
   .. code-block::
      export DOIT_WORKDIR=/home/adming/DrivingRange/CloudWorks/netboot_admi
      export PYTHONPATH=/home/kabira/Development/cloudworks-monallabs/everything-netbooting/src:$PYTHONPATH
      python3 -c "from rtas_netboot import pipeline_runner_main; pipeline_runner_main.run()"


#. Selecting the target machine 
   looking at the /etc/dnsmasq.conf  the target directory is /nfs/aa5e7587
   
   .. code-block::
      dhcp-host=dc:a6:32:4a:df:d9,set:obsd144,192.168.0.144
      dhcp-boot=tag:obsd144,aa5e7587/BOOTAA64.EFI


      sudo tar xzphf ~/xshare76.tgz 
      sudo tar xzphf ~/xserv76.tgz 
      sudo tar xzphf ~/xfont76.tgz 
      sudo tar xzphf ~/xbase76.tgz 
      sudo tar xzphf ~/comp76.tgz 
      sudo tar xzphf ~/base76.tgz

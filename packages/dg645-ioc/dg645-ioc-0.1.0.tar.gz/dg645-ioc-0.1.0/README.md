EPICS-IOC for the Stanford DG645 Delay Generator
================================================

Quick 'n dirty:

 - Download via PyPI: `pip install dg645-ioc` or via GitLab: `git clone https://gitlab.com/kmc3-xpp/kronos-ioc`
 
 - Configure at least the IP address and the EPICS prefix and start via shell:
   ```
   $ export DG645_EPICS_PREFIX="BEAMLINE:DG645:"
   $ export DG645_HOST="10.0.0.17"
   $ DG645-ioc
   INFO:kronos.ioc:Stanford Research Systems,DG645,s/n001776,ver1.14.10E
   INFO:root:Starting IOC, PV list following
   [...]
   INFO:caproto.ctx:Server startup complete.
   ```
   
 - ...or create container and start via Docker or Podman:
   ```
   $ podman build -t dg645-ioc -f kronos-ioc/Dockerfile -v $PWD/kronos-ioc:/kronos_src:z
   $ podman run -ti --rm \
       -e DG645_EPICS_PREFIX="BEAMLINE:DG645:" \
	   -e DG645_HOST=10.0.0.17\
	   --name fridge dg645-ioc:latest
   [...]
   ```
   
 Here's a list of environment variables that might help:
 
  - `DG645_HOST`: host name or IP of the DG645 controller
  
  - `DG645_PORT`: this is better left blank (the default). In that
    case, the IOC will create a "TCPIP::<host>::INSTR" PyVISA device
	name. If the port is specified, it will create a
	"TCPIP::<host>::<ip>::SOCKET" device name instead.
  
  - `DG645_VISA_DEV`: PyVISA device to connecto to, instead of the
    TCP/IP device. If set, overrides host/port.
	
  - `DG645_VISA_RMAN`: PyVISA resource manager. Defaults to "@py".
    If you've got this far, you know what this is good for ;-)
	
  - `DG645_EPICS_PREFIX`: EPICS PV prefix to use. Include trailing column
    (`:`) if you need one. Defaults to `KMC3:XPP:DG645:`.
	
  - `DG645_LOGGING`: one of "error", "warn", "info" or "debug". Defaults
    to "info".
	
  - `DG645_LOG_STATUS`: if set to "yes", the IOC will periodically
    (about once per second) log the
    current status of all variables it observes to the "info" logging
	facility. The default is not to do that.
 
   
 Enjoy.



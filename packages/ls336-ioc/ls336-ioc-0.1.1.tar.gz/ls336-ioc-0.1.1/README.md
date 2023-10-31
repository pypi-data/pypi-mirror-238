EPICS-IOC for the Lakeshore 336 Temperature Controller
======================================================

Quick 'n dirty:

 - Download via PyPI: `pip install ls336-ioc` or via GitLab: `git clone https://gitlab.com/kmc3-xpp/fridge`
 
 - Configure at least the IP address and the EPICS prefix and start via shell:
   ```
   $ export LS336_EPICS_PREFIX="BEAMLINE:LS336:"
   $ export LS336_HOST="10.0.0.17"
   $ ls336-ioc
   INFO:fridge.ioc:Lake Shore Model 336 version: 2.5
   INFO:root:Starting IOC, PV list following
   [...]
   INFO:caproto.ctx:Server startup complete.
   ```
   
 - ...or create container and start via Docker or Podman:
   ```
   $ podman build -t ls336-ioc -f fridge/Dockerfile -v $PWD/fridge:/fridge_src:z
   $ podman run -ti --rm \
       -e LS336_EPICS_PREFIX="BEAMLINE:LS336:" \
	   -e LS336_HOST=10.0.0.17\
	   --name fridge ls336-ioc:latest
   [...]
   ```
   
 Here's a list of environment variables that might help:
 
  - `LS336_HOST`: host name or IP of the LS336 controller
  - `LS336_PORT`: port to connect to (typically 7777)
  - `LS336_VISA_DEV`: PyVISA device to connecto to, instead of the
    TCP/IP device. If set, overrides host/port.
  - `LS336_VISA_RMAN`: PyVISA resource manager. Defaults to "@py".
    If you've got this far, you know what this is good for ;-)
  - `LS336_EPICS_PREFIX`: EPICS PV prefix to use. Include trailing column
    (`:`) if you need one. Defaults to `KMC3:XPP:LS336:`.
  - `LS336_LOGGING`: one of "error", "warn", "info" or "debug". Defaults
    to "info".
  - `LS336_LOG_STATUS`: if set to "yes", the IOC will periodically
    (about once per second) log the
    current status of all variables it observes to the "info" logging
	facility. The default is not to do that.
 
   
 Enjoy.



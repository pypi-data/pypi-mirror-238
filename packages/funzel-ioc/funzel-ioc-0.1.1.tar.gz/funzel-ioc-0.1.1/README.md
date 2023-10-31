EPICS-IOC for Pharos Laser Controller
=====================================

This is an unofficial package without ties to, support from, or 
warranty of the official
[Pharos manufacturer, Light Conversion](https://lightcon.com).

This is essentially an it-works-for-me version, written at the
KMC3-XPP beamline of BESSY-II. It is being updated and supported
for as long as the authors are responsible for that beamline.
We publish this under the GNU GPL or later.

That said, we try to document as much as possible in the hope
that this will be useful. If you find yourself many years into
the future :) stumbling over this, and wishing "gee, I wish it
was still supported...", feel free to drop us a line. Chances 
are we're going to answer one question or the other, if you're
a fellow scientist. Or that we'll even be available for a more
extensive development on commission basis, if you're a
commercial entity.


Installation and usage
----------------------

### Obtaining Funzel-IOC

Download the latest version either via `pip` from
[PyPI](https://pypi.org/projects/funzel-ioc):
```
pip install funzel-ioc
```

...or form Gitlab:
```
git clone git@gitlab.com:codedump2/funzel
pip install funzel/
```

### Configuring the Host

The Funzel-IOC connects to the Pharos control hardware via its
serial interface. It uses PyVISA for this.

Chances are that the current setup is as limited as of the writing
of this README (November 2023), this means that:

 - the EPICS prefix currently is `KMC3:XPP:PHAROS:`, and

 - the VISA address at which Funzel-IOC expects to find the laser
   interface is `"ASRL/dev/funzel::INSTR"`, meaning that you
   need a symlink from the corresponding `/dev/ttyUSB?` device
   to `/dev/funzel`.

You can automatically set up the correct symlink by virtue 
of a udev rule, e.g. in `/etc/udev/rules.d/99-funzel.rules`:
```
ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ATTRS{serial}=="AL01FC2E", \
SUBSYSTEM=="tty", MODE="0666", SYMLINK+="funzel"
```

You may want to change the following:

 - `ATTRS{serial}==...`: set this to the serial of your device. The Pharos device
   uses a generic built-in USB-to-Serial converter (FT232R), so the vendor and
   product IDs might not be enough to identify it, if you have several similar
   pieces of equipment attached. Using the self-reported Pharos serial number
   will nail this down effectively.
   (You can track down the serial number with `dmesg`, `lsusb` or
   `udevadm info -a /dev/ttyUSB...`).

 - `MODE="..."`: the mode of `0666` here allows every user on your system
   to access the laser device. This is most likely not what you want. Instead,
   consider restricting this to a specific user and group:
   `"OWNER="...", GROUP="...", MODE="0660"`.

### Running the IOC on the Host

On the host, just type:
```
funzel-ioc
```

And it should result in the IOC outputting its control variables,
and then a regular (about once per second) status.

### Running the IOC in a Docker Container

After you've downloaded the sources into `./funzel`, e.g. from GitLab
(see above), try this:

```
podman build -t funzel-ioc -f funzel/Dockerfile -v $PWD/funzel:/funzel_src:z
podman run -ti --rm --device /dev/funzel:/dev/funzel funzel-ioc:latest
```

IOC Usage and Laser Control
---------------------------

Some notable EPICS process variables:

  - ...(fixme?)

How to turn the laser on / off:

  - ...(fixme?)

How to check if the laser is running:

  - ...(yep; this one's a fixme too...)

Bugs
----

Feel free to report any. We may be able to help, but keep in mind:
It Works For Me (tm) 🤷

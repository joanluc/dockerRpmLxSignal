# dockerRpmLxSignal
Portage of Signal App with docker for RPM based Linux

Signal 
https://www.signal.org/en/download/

* Install Signal on Linux
  Unfortunaly Signal is only available in Linux in the DEB format so it can't be used in RPM based distribution, i found a flatpak installation process at https://www.howtogeek.com/709784/how-to-install-signal-desktop-on-linux/ and tryed it in  my Fedora box but it ended on an error.
  
  It why i decided to try to use docker to install and run Signal in my Fedora box.

* Install Signal in Fedora or over RPM based Linux
  ** Prerequisit
     Install docker and launch docker daemon
     <code>
     #!/usr/bin/env bash
     sudo dnf install -y moby-engine
     sudo service docker restart
     </code>

  ** Get Dockerfile and build Signal 
     git clone 
     <code>
     cd $(dirname Dockerfile)
     docker build -t signal_fedora .
     </code>

  ** Run Signal
     We must run Signal as unprivileged user, create signal_user
     <code>
     SIGNALUSER=$(whoami)
     docker run -it signal_fedora useradd $SIGNALUSER
     </code>

  ** Signal musr run in graphic context
     <code>
     xauth list
     read -p "Xauth cookie  ? " COOKIE
     docker run -it --net=host -e DISPLAY -v /tmp/.X11-unix --name="signal_fedora" -u $SIGNALUSER xauth add $COOKIE
     </code>

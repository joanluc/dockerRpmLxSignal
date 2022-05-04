# SIGNALUSER=$(whoami)
# Dockerfile to install and run Signal in Fedora or RPM based Linux
# Docs Signal: https://www.signal.org/docs/
# Set the base image to Debian
FROM debian
# Update the repository sources list and install  apt-utils wget gpg xauth sudo
RUN apt-get update && apt-get install -y apt-utils wget gpg xauth
# Get and install Signal official public software signing key
RUN wget -O- https://updates.signal.org/desktop/apt/keys.asc |\
gpg --dearmor > signal-desktop-keyring.gpg
# RUN cat signal-desktop-keyring.gpg | sudo tee -a /usr/share/keyrings/signal-desktop-keyring.gpg > /dev/null
RUN cat signal-desktop-keyring.gpg | tee -a /usr/share/keyrings/signal-desktop-keyring.gpg > /dev/null
# Add Signal repository to repositories' list
# RUN echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/signal-desktop-keyring.gpg] https://updates.signal.org/desktop/apt xenial main' | sudo tee -a /etc/apt/sources.list.d/signal-xenial.list
RUN echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/signal-desktop-keyring.gpg] https://updates.signal.org/desktop/apt xenial main' | tee -a /etc/apt/sources.list.d/signal-xenial.list
# Update the repository sources list and install signal
RUN apt-get update && apt-get install -y libdrm2 libgbm-dev signal-desktop
# Create non privileged user to run app
RUN  groupadd -r signal && useradd -G signal joanluc # $SIGNALUSER
ENTRYPOINT usr/bin/signal-desktop

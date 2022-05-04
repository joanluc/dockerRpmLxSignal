#!/usr/bin/env python
import os
class Docker_Run_Signal():
    """
    * install docker
    * start Docker daemon
    * build dockerSignal
    * add signal User and group 
    * run dockerSignal

(
 build_dockerSignal
 run_dockerSignal
)

    """
    def __init__(self,User="",MAGIC_COOKIE=""):
        self.SIGNALUSER=User
        self.COOKIE=MAGIC_COOKIE
    
    def __Error__(self,ErrorStr):
        print(ErrorStr)
        
    def __Exec__(self,ErrorStr,command):
        from os import system
        try:
            self.__Error__(ErrorStr)
            result=system("exec "+command)
        except IOError as e:
           result=self.__Error__("Error:"
                                  +command+":"
                                  +e)
        finally:
            return(result)

    
    def __services__(self,check_filename,ok_message,exec_message,
                     exec_command):
        if os.exist(check_filename):
            self.__Error__(ok_message)
        else: 
            self.__Exec__(exec_message,
                          exec_command)

    
    def install_Docker(self):
        """
        Verify if docker is installed and installs it if not
        """
        self.__services__("/usr/bin/docker","Docker installed",
                          "Installing docker",
                          "sudo dnf install -y moby-engine")

    def run_Docker_daemon (self):
        """
        Verify if docker daemon is running and launches it if not 
        """
        self.__services__("/var/run/docker.sock","Docker daemon running",
                          "Restarting docker service",
                          "sudo service docker restart")

    def build_dockerSignal(self):
        """
        Go into Dockerfile's directory and build Signal for Fedora
        """
        # cd $(dirname $0);
        DockerfileDir=os.getcwd("../Signal/Dockerfile")
        os.chdir(DockerfileDir)
        self.__Exec__("building dockerSignal",
                      "docker build -t signal_fedora .")

    def add_signalUser(self):
        """
        SIGNALUSER=$(whoami)
        docker run -it signal_fedora useradd $SIGNALUSER
        """
        from os import getlogin
        if self.SIGNALUSER=="":
            self.SIGNALUSER=getlogin()
        self.__Exec__("Creating signal user "+
                      self.SIGNALUSER,
                      "docker run -it signal_fedora useradd "+
                      self.SIGNALUSER)

    def run_dockerSignal (self):
        """
        # cd $(dirname $0)
        # RUN xauth add $COOKIE
        
        xauth list
        read -p "Xauth cookie  ? " COOKIE
        # [0426/221306.698593:FATAL:electron_main_delegate.cc(291)] Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
        docker run -it --net=host -e DISPLAY -v /tmp/.X11-unix --name="signal_fedora" -u $SIGNALUSER xauth add $COOKIE
        # ERROR
        # Unable to find image 'xauth:latest' locally
        # docker: Error response from daemon: pull access denied for xauth, repository does not exist or may require 'docker login': denied: requested access to the resource is denied.
        # See 'docker run --help'.
        """
        if self.COOKIE=="":
            self.__Exec__("Getting xauth list","xauth list")    
            self.COOKIE=input("Xauth cookie  ? ")
        self.__Exec__("","docker run -it --net=host -e DISPLAY -v /tmp/.X11-unix --name='signal_fedora' -u "+
                      self.SIGNALUSER+" xauth add "+self.COOKIE)
        

    
def test_Docker_Run_Signal():
    mySignalApp=Docker_Run_Signal()
    mySignalApp.install_Docker()
    mySignalApp.run_Docker_daemon ()
    mySignalApp.build_dockerSignal()
    mySignalApp.add_signalUser()
    mySignalApp.run_dockerSignal ()
    
if __name__=="__name__":
    test_Docker_Run_Signal()

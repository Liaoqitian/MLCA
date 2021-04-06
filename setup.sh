#! /bin/bash
# ============================================================
# BTC Linux and MacOS Installation Script
# for docker and cloud
#
# This code is copyrighted (c) 2020,2021 by Brainome, Inc. All Rights Reserved.
# Please contact support@brainome.ai with any questions.
#
# Usage:
#   setup -docker [-alpha|-beta] [-y] [-cpu|gpu] [-image tag]
#   setup -cloud  [-alpha|-beta] [-y] 
#
# version - 100
# version - 101 - allow to install on unsupported architectures

LOCALDIR=/usr/local
INSTALLDIR=$LOCALDIR/brainome
RUNDIR=$LOCALDIR/bin
RELEASE=latest
INSTALLTYPE="docker"
bold='[1m'
normal='(B[m'
red=${bold}'[31m'
green=${bold}'[32m'
CPU=cpu

BATCH="NO"

SUDO="sudo"
if [ `whoami` = "root" ]; then
    SUDO=""
fi

# -----------------------------------------
# installation/execution steps
# -----------------------------------------
function main() {
    echo ""
    echo "===================================================="
    echo "Brainome Table Compiler Setup (c) Brainome 2020-2021"
    echo "===================================================="
    
    process_args "$@"
    check_os
    permission_to_install
    if [ $INSTALLTYPE = docker ]; then
        download_btc-docker
        install_btc
        echo ""
        echo "${bold}Downloading docker image${normal}"
        if [ -z ${IMAGE+x} ]; then
            $RUNDIR/btc -update -image brainome/btc_local_$CPU:$RELEASE
        else
            $RUNDIR/btc -update -image $IMAGE
        fi
    else
        download_btc-cloud
        install_btc
    fi
    echo ""
    echo "${green}Installation of btc was successful.${normal}"
    echo ""
    check_path
} 

function check_path() {
    if [[ ":$PATH:" == *":$RUNDIR:"* ]]; then
        echo ""
    else
        echo "${bold}Make sure that $RUNDIR is in your path, otherwise run $RUNDIR/btc${normal}"
        echo ""
    fi

}

# -----------------------------------------
# process args
# -----------------------------------------
function process_args() {
    while [ $# -gt 0 ]
       do
       case "$1" in
           "-y"      ) BATCH="YES" ;;
           "-cpu"    ) CPU=cpu ;;
           "-gpu"    ) CPU=gpu ;;
           "-docker" ) INSTALLTYPE="docker" ;;
           "-cloud"  ) INSTALLTYPE="cloud" ;;
           "-beta"   ) RELEASE="beta" ;;
           "-alpha"  ) RELEASE="alpha" ;;
           "-image"  ) shift; IMAGE=$1 ;;
       esac
       shift
    done
}

# -----------------------------------------
# check operating system requirements
# -----------------------------------------
function check_os() {
   echo ""
   OS=`uname -s`
   if [ $OS = Darwin ]; then
       # ################################
       # macOS >= Mojave
       # ################################
       # https://en.wikipedia.org/wiki/Darwin_%28operating_system%29#History
       VERSION_ID=`uname -r`
       MAJOROSID=`echo $VERSION_ID | awk '{split($1,osrev,".") ; print(osrev[1])}'`
       OSID=darwin
       btcexec="btc_mac"
       case $MAJOROSID in
           14 ) OSNAME="OS X Yosemite" ;;
           15 ) OSNAME="OS X El Capitan" ;;
           16 ) OSNAME="macOS Sierra" ;;
           17 ) OSNAME="macOS High Sierra" ;;
           18 ) OSNAME="macOS Mojave" ;;
           19 ) OSNAME="macOS Catalina" ;;
           20 ) OSNAME="macOS Big Sur" ;;
       esac
       echo "OS detected: $OSNAME ($VERSION_ID)"
       if [ $MAJOROSID -lt 19 ]
           then
           echo "${red}Only macOS Catalina or higher is supported.${normal}"
           override_unsupported_os
       fi
   fi
   if [ $OS = Linux ]; then
       if [ -e /etc/os-release ] ; then
           VERSION_ID=`awk -F= '/^VERSION_ID=/{print $2}' /etc/os-release | sed 's/"//g'`
           MAJOROSID=`echo $VERSION_ID | awk '{split($1,osrev,".") ; print(osrev[1])}'`
           OSID=`awk -F= '/^ID=/{print $2}' /etc/os-release | sed 's/"//g'`
           OSNAME=`awk -F= '/^NAME=/{print $2}' /etc/os-release | sed 's/"//g'`
           btcexec="btc_linux"
       else
           echo "${red}Unknown $OS release. Terminating${normal}"
           exit 1
       fi
       echo "OS detected: $OSNAME ($VERSION_ID)"
       case $OSID in
           debian )
           ### Debian >= 9
               if [ $MAJOROSID -lt 9 ] ; then
                   echo "${red}Only debian version 9 or above are supported.${normal}"
                   override_unsupported_os
               fi ;;
           ubuntu )
           ### Ubuntu >= 16.04
               if [ $MAJOROSID -lt 16 ] ; then
                   echo "${red}Only ubuntu version 16.04 or above are supported.${normal}"
                   override_unsupported_os
               fi ;;
           centos )
           ### Centos >= 7
               if [ $MAJOROSID -lt 7 ] ; then
                   echo "${red}Only centos version 7 or above are supported.${normal}"
                   override_unsupported_os
               fi ;;
           rhel )
           ### RedHat >= 7
               if [ $MAJOROSID -lt 7 ] ; then
                   echo "${red}Only Red Hat version 7 or above are supported.${normal}"
                   override_unsupported_os
               fi ;;
           * )
           ### Other Linux not supported
               echo "${red}This Linux architecture is not officially supported.${normal}"
               override_unsupported_os
       esac
   fi
}

# -----------------------------------------
# ask to override unsupported OS
# -----------------------------------------
function override_unsupported_os() {
  echo ""
  if [ $BATCH = "NO" ] ; then
     while true; do
       read -p "Do you wish to continue installation anyway [Y/n] ? " yn
       case $yn in
           [Yy]* ) break;;
           [Nn]* ) echo "Installation cancelled by user. Exiting." ; exit;;
           * ) echo "Please answer yes or no.";;
       esac
     done
  fi
}

# -----------------------------------------
# ask for permission to install
# -----------------------------------------
function permission_to_install() {
  echo ""
  echo "This script requires admin permission to create and edit"
  echo "the installation directory $INSTALLDIR"
  echo ""
  if [ $BATCH = "NO" ] ; then
     while true; do
       read -p "Do you wish to continue [Y/n]? " yn
       case $yn in
           [Yy]* ) break;;
           [Nn]* ) echo "Nothing was done. Exiting." ; exit;;
           * ) echo "Please answer yes or no.";;
       esac
     done
  fi
}

# -----------------------------------------
# download the cloud client
# -----------------------------------------
function download_btc-cloud() {
    echo ""
    /bin/echo -n "${bold}Downloading $btcexec ...${normal}"
    tmpfile=/tmp/$btcexec.$$
    curl -fsSL https://download.brainome.net/btc-cli/$RELEASE/$btcexec --output $tmpfile
    echo " Done"
    if [ ! -f $tmpfile ] ; then
        echo "${red}Error while downloading. Terminating.${normal}"
        exit 1
    fi
}

# -----------------------------------------
# download the docker client
# -----------------------------------------
function download_btc-docker() {
    echo ""
    /bin/echo -n "${bold}Downloading btc-docker ...${normal}"
    tmpfile=/tmp/btc-docker.$$
    curl -fsSL https://download.brainome.net/install/btc.sh --output $tmpfile
    echo " Done"
    if [ ! -f $tmpfile ] ; then
        echo "${red}Error while downloading. Terminating.${normal}"
        exit 1
    fi
}

# -----------------------------------------
# install btc in directories
# -----------------------------------------
function install_btc() {
    # Check for install directory.
    # Create if it does not exist
    if [ ! -d $INSTALLDIR ] ; then
        echo "Creating $INSTALLDIR"
        $SUDO mkdir -p $INSTALLDIR ; $SUDO chmod a+rx $INSTALLDIR
        if [ ! -d $INSTALLDIR ] ; then
            echo "${red}Could not create $INSTALLDIR.${normal}"
            exit 1
        fi
    fi

    # If btc in install directory exists, remove it
    if [ -f $INSTALLDIR/btc ] ; then
        $SUDO rm -f $INSTALLDIR/btc
        if [ -f $INSTALLDIR/btc ] ; then
            echo "${red}Could not remove existing $INSTALLDIR/btc.${normal}"
            exit 1
        fi
    fi
    # Copy btc in install directory
    echo "Installing btc into $INSTALLDIR"
    $SUDO cp $tmpfile $INSTALLDIR/btc; $SUDO chmod a+rx-w $INSTALLDIR/btc;
    if [ ! -f $INSTALLDIR/btc ] ; then
        echo "${red}Could not create $INSTALLDIR/btc.${normal}"
        exit 1
    fi

    # Check for run directory.
    # Create if it does not exist
    if [ ! -d $RUNDIR ] ; then
        echo "Creating $RUNDIR"
        $SUDO mkdir -p $RUNDIR; $SUDO chmod a+rx $RUNDIR
    fi
    
    # Create a soft link of btc in run directory
    echo "Linking $RUNDIR/btc to $INSTALLDIR/btc"
    if [ -L $RUNDIR/btc ] ; then
        $SUDO rm $RUNDIR/btc
    fi
    if [ -e $RUNDIR/btc ] ; then
        echo "${red}A file $RUNDIR/btc already exists. Cannot link. Terminating${normal}"
        exit 1
    fi
    $SUDO ln -s $INSTALLDIR/btc $RUNDIR/.

    rm $tmpfile
    echo " "
}

main "$@"
exit

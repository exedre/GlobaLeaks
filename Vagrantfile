# ********************************************************
#   GLOBALEAKS VAGRANT CONFIG FILE
#
# 0) Install VirtualBox (https://www.virtualbox.org/) 
# 1) Install Vagrant (http://www.vagrantup.com/)
# 2) Create a dir and save this file as "Vagrantfile"
# 3) In the same dir run "vagrant up"
# 4) play :)
# 
# Based on the Installation Guide for Globaleaks to be found here:
# <https://github.com/globaleaks/GlobaLeaks/wiki/Installation-guide>
# 
# ********************************************************

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise32"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network :forwarded_port, guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network :private_network, ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  config.vm.network :public_network

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/globaleaks"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end
  #
end

$script = <<SCRIPT
date > /etc/vagrant_provisioned_at

echo "********************************************************"
echo "*   STEP 1: Install GlobaLeaks"
echo "********************************************************"

gpg --keyserver x-hkp://pool.sks-keyservers.net --recv-keys 0x24045008
gpg --export B353922AE4457748559E777832E6792624045008 | apt-key add -
/globaleaks/scripts/install-ubuntu-12_04.sh -y

echo "********************************************************"
echo "*   STEP 2 - Create Your Hidden Service"
echo "********************************************************"

cat /usr/share/globaleaks/glbackend/torrc >> /etc/tor/torrc
echo "HiddenServiceDir /var/globaleaks/torhs/" >> /etc/tor/torrc
echo "HiddenServicePort 80 127.0.0.1:8082" >> /etc/tor/torrc

/etc/init.d/tor restart

echo "********************************************************"
echo "*   STEP 3 - Start globaleaks"
echo "********************************************************"

/etc/init.d/globaleaks start

echo "********************************************************"
echo "*                PLEASE JOT DOWN THIS ADDRESS"
echo "********************************************************"

cat /var/globaleaks/torhs/hostname

echo "********************************************************"
echo "*                PLEASE JOT DOWN THIS ADDRESS"
echo "********************************************************"


SCRIPT

Vagrant.configure("2") do |config|
  config.vm.provision :shell, :inline => $script
end

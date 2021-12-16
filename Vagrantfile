# set up the default terminal
ENV["TERM"]="linux"

Vagrant.configure("2") do |config|

  # set the image for the vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"

  # st the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.56.4"
  config.vm.network "forwarded_port", guest: 6443, host: 6443 # API Access
  config.vm.network "forwarded_port", guest: 3000, host: 3000 # Grafana

  # consifure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
  config.vm.provision "shell", inline: <<-SHELL
    # install a k3s cluster
    # curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.19.2+k3s1 K3S_KUBECONFIG_MODE="644" sh -
    curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.19.3+k3s1 K3S_KUBECONFIG_MODE="644" sh -
    
    # install iptables
    sudo zypper --non-interactive install iptables
    
    # install Helm
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
    
    # install golang
    export GOPATH=$HOME/
    sudo curl -O https://storage.googleapis.com/golang/go1.17.5.linux-amd64.tar.gz
    sudo tar -xvf go1.17.5.linux-amd64.tar.gz
    sudo mv go /usr/local
    sudo echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.profile
    export PATH=$PATH:/usr/local/go/bin
    go version 

    # install unzip
    #sudo zypper --non-interactive install unzip
    
    # install protoc
    #sudo curl -O https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-x86_64.zip
    #sudo unzip protoc-3.19.1-linux-x86_64.zip
<<<<<<< HEAD
    sudo cp /vagrant/protoc-3.19.1-linux-x86_64/bin/protoc  /usr/bin
    sudo cp /vagrant/protoc-3.19.1-linux-x86_64/include  /usr/local/
=======
    sudo cp -r /vagrant/protoc-3.19.1-linux-x86_64/bin/protoc  /usr/bin
    sudo cp -r /vagrant/protoc-3.19.1-linux-x86_64/include  /usr/local/
>>>>>>> feb883b121005c30c9f223701dd241bb8df0c702
    sudo echo 'export PATH=$PATH:/usr/bin/protoc' >> ~/.profile
    chmod a+x /usr/bin/protoc
    export PATH=$PATH:/usr/bin/protoc
    protoc --version

    # install protoc-gen-go
<<<<<<< HEAD
    sudo go install github.com/golang/protobuf/protoc-gen-go@latest
    chmod a+x $HOME/go/bin
    sudo echo 'export PATH=$PATH:$HOME/go/bin/protoc-gen-go' >> ~/.profile
    export PATH=$PATH:$HOME/go/bin/protoc-gen-go

    export GOPATH=$HOME/go
    export GOROOT=/usr/local/go
    export PATH=$PATH:$GOPATH/bin
    export PATH=$PATH:$GOROOT/bin
=======
    go install github.com/golang/protobuf/protoc-gen-go@latest
    #chmod a+x $HOME/go/bin
    sudo echo 'export PATH=$PATH:$HOME/go/bin/protoc-gen-go' >> ~/.profile
    export PATH=$PATH:$HOME/go/bin/protoc-gen-go

    # export GOPATH=$HOME/go
    # export GOROOT=/usr/local/go
    # export PATH=$PATH:$GOPATH/bin
    # export PATH=$PATH:$GOROOT/bin
>>>>>>> feb883b121005c30c9f223701dd241bb8df0c702

  SHELL
end

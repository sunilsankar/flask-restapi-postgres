ENV['VAGRANT_NO_PARALLEL'] = 'yes'

Vagrant.configure(2) do |config|
  config.ssh.insert_key = false
  config.vm.synced_folder "./", "/vagrant"
   config.vm.provision "ansible_local" do |ansible|
   ansible.playbook = "minikube.yml"
  end

  # Kubernetes Master Server
  config.vm.define "minikube" do |node|
  
    node.vm.box               = "generic/ubuntu2004"
    node.vm.box_check_update  = false
    node.vm.hostname          = "minikube.example.com"

    node.vm.network "private_network", ip: "172.16.16.100"
  
    node.vm.provider :virtualbox do |v|
      v.name    = "minikube"
      v.memory  = 4096
      v.cpus    =  2
    end
  
    node.vm.provider :libvirt do |v|
      v.memory  = 4096
      v.nested  = true
      v.cpus    = 2
    end
     node.vm.provider :parallels do |v|
      v.memory  = 4096
      v.cpus    = 2
     end

     
#    node.vm.provision "ansible_local" do |ansible|
#      ansible.playbook = "ansible/master.yaml"
#    end
 end 
  end

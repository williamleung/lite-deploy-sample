## 构建服务器使用说明  

在开发环境中build工程除了编译镜像，还为deploy工程提供下载服务，需要在工程目录下执行如下命令

#### 使用步骤

1 启动vagrant环境  
* `vagrant up`

2 登陆环境  
* `vagrant ssh`

3 查看playbook    
* `cd /vagrant/dockerBuild/ansible`    
* `ls playbooks`   

4 编译Rabbitmq镜像   
* `ansible-playbook playbooks/build_rabbitmq_images.yml`

5 编译部署脚本工具  
* `ansible-playbook playbooks/build_deploy_package.yml`

6 配置启动下载服务器  
* `ansible-playbook playbooks/prepare_download_hub.yml`
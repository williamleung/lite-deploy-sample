## 使用说明

本工程演示我们通过Ansible脚本来自动化部署和配置一个分布式软件服务.  
在开发环境中我们通过build和deploy两个工程来拆分软件包的编译打包和部署启动.

### 1. 目录结构

├── InitializeHosts: 目标服务器初始化脚本   
├── README.md           
├── dockerBuild: 软件包构建工具           
├── dockerDeploy: 软件包部署脚本            
└── test: 用Vagrant模拟一个测试服务器集群,用于演示部署过程                      

#### 1.1 dockerBuild

* 通过Dockerfile编译镜像
* 启动下载服务器供deploy工程进行镜像下载
* 使用人员: 研发人员
* 使用场景: 业务模块需要做版本迭代,仅发布新版本时使用,_非现场实施部署工作,非交付物_
* 编译环境: Vagrant虚机

#### 1.2 InitialzeHosts
* 初始化目标主机环境:网络互通,ssh权限,docker环境,主控机初始化
* 使用人员: 部署实施人员
* 使用场景: 现场实施的第一步,将所有目标节点主机统一环境

#### 1.3 dockerDeploy
* 载入build工程所编译的镜像文件
* 基础服务、上传下载服务、云信服务的配置及部署

#### 1.4 test
* 测试时使用的临时资源,如特定环境的ssh登陆key

#### 说明

* dockerBuild节点主要起到镜像编译打包和下载服务器的作用
* deploy工程中各个节点依赖于docker，使用deb包进行安装，开发环境中该deb包由build工程的下载服务提供
* deploy工程依赖于build工程所产生的docker镜像文件，开发环境中镜像编译后会放置到build工程的下载服务目录

#### 软件依赖

* build和deploy工程均基于ansible和vagrant
* vagrant为便于开发和测试引入，在生产环境只需要依赖ansible，vagrant的debian8镜像文件可联系开发人员获取
* ansible由工程内脚本自动安装在控制节点上，控制节点可以是独立于客户私有环境的机器(比如负责安装交付的工程师笔记本电脑，有外网)，依赖apt-get和pip等工具

### 2 开发环境版本

virtualbox为vagrant提供虚拟机支持

#### linux或者mac环境

* vagrant
	* 1.8.3版本，https://releases.hashicorp.com/vagrant/1.8.3/vagrant_1.8.3.dmg
* virtualbox 
	* 5.0版本，http://download.virtualbox.org/virtualbox/5.0.38/VirtualBox-5.0.38-114633-OSX.dmg

#### windows环境

* vagrant
	* 1.9.5版本，https://releases.hashicorp.com/vagrant/1.9.5/vagrant_1.9.5.msi
* virtualbox 
	* 5.1版本，http://download.virtualbox.org/virtualbox/5.1.8/VirtualBox-5.1.8-111374-Win.exe

### 3. 开发分支管理

* 由于日常开发以功能模块来划分，故约定根据模块建立分支进行开发
* 当模块分支开发完成后，合并到dev分支供QA进行测试
* QA测试过程中发现的问题，小的修复可直接提交到dev分支，较大改动在模块分支进行修复后重新合并到dev分支

### 4. 部署说明

#### 交付物

所有交付物都包含在下载服务目录中，目录结构及说明如下

* nim\_dep\_ansible.tar.gz：dockerDeploy工程的压缩包
* images/：包含dockerBuild工程产生的镜像文件
* deb/：包含部署环境中初始化所依赖的软件包，如docker等

#### 部署步骤

以Vagrant环境为例进行说明   
**打包构建和下载服务器:**   
    host:nim-build-01 ip: 192.168.200.10 (不同环境该地址可以自定义，可适应不同的内部网络环境要求  
**部署工具机:**   
    host:nim-initializer-01  ip: 192.168.200.110      
**目标服务器:**   
    host: nim-node-{01~03} ip: 192.168.200.{11~13}  

**A) 在打包构建机上**   
    1. 构建修改之后的RabbitMQ软件Docker镜像
    2. 构建机上构建部署脚本
    3. 构建机上配置和启动下载服务器

**B) 准备部署环境目标服务器**  
    1. 进入test目录,将预设的vagrant测试服务器启动   
    `cd test && vagrant up`

**C) 在部署工具机上**  
    1. 下载部署脚本  
       `wget http://10.200.200.10/nim_dep_ansible.tar.gz`   
    2. 修改部署脚本中的hosts等,并配置目标服务器的登陆信息
    3. 执行部署脚本   
        `ansible-playbook ` 
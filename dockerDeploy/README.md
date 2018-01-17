## 使用说明

提供基于vagrant的测试环境，ansible目录可拷贝到真实环境中使用

### 配置说明

dockerDeploy工程遵循一般ansible工程的结构规范，配置文件主要由以下几部分组成

dockerDeploy/ansible为当前目录

0 pwd

* hosts文件：inventory文件，包含部署环境中机器地址、分组等信息
* ansible.cfg文件：ansible运行环境的配置，主要配置项包括remote\_user、private\_key\_file

1 group_vars目录

* all文件：全局配置或者不同模块相互依赖的配置项，比如自定义的服务端口
* 以inventory hosts文件中的group名命名的文件：特定group的配置，需要根据不同的部署环境进行修改

2 host_vars目录

* 以inventory hosts文件中的host名命名的文件：特定host的配置，需要根据不同的部署环境进行修改，注意文件名也需要相应修改

3 roles目录

* 不同role表示不同模块，模块目录下的defaults和vars目录中的main.yml文件：特定模块的配置，这里的配置一般不经常修改，在不同环境都能正常工作，满足在特殊情况下进行配置的需求

不同模块部署时，一般只要修改上述1和2类配置文件，下面分模块对配置项进行简要说明

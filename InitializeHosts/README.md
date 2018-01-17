# 系统初始化任务

## 描述
    对甲方交付的服务器环境环境

## 环境交付要求
    1. 服务器之间网络互通, 节点之间用hostname能互ping;
    2. 所有服务器开通ssh权限,且能通过 ssh key登陆;

## 初始化任务列表  
    * 配置apt源;
    * 安装docker软件,并配置加速镜像;
    * 安装Supervisor;
    * 时区/时间同步;
    * 安装ansible;
    * TODO
    * 把host和内网ip配置到所有节点的 /etc/hosts 文件
    * *Admin* 机器下载部署程序包,并打通到其他机器的权限

## 使用方式
    * 修改 **ansible.cfg** 重点关注 hostfile/private_key
    * 修改 上一项中hostfile中的主机资源列表 
    * 进入到 InitializeHosts 目录 执行 
        ```
        ansible all -m ping
        ```
        确认各个主机权限/网络已经联通
    * 执行环境初始化
        ```
        ansible-playbook env_initialize.yml
        ```
        执行成功即完成主机初始化
        
---

PS: 如果ssh key有密码保护,可以用下面的方式避免重复输入密码  

```
ssh-agent /bin/bash    
ssh-add ~/.ssh/theKey
```

#tag rabbitmq:3.6.9-nim
FROM library/rabbitmq:3.6.9
MAINTAINER netease.im

#replace source list file
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
COPY sources.list /etc/apt/

#install some additional software
RUN apt-get update && apt-get install -y ntpdate vim less supervisor
RUN systemctl disable supervisor.service

#update timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#copy rabbitmq configs
COPY config/* /etc/rabbitmq/

#copy supervisord configs
COPY supervisor_conf/* /etc/supervisor/conf.d/

#copy my runnable scripts
COPY scripts/* /scripts/

EXPOSE 25672 5672 5671 15672 4369

#TODO set crontab for ntpd

USER root
CMD ["/usr/bin/supervisord","-n","-c","/etc/supervisor/supervisord.conf"]

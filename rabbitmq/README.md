# 在Centos7上安装RabbitMQ

```
# yum -y install epel-release
# yum -y update
```
## 安装 Erlang

下载repository

```
wget http://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
```

添加repository，注意如果这个rpm包不安装则后续会产生erlang和rabbitmq版本不匹配的问题，目前erlang和rabbitmq版本匹配关系可以查看rabbitmq官网：https://www.rabbitmq.com/which-erlang.html

```
# rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
```

安装erlang及其依赖的库
```
# yum -y install erlang socat logrotate
```

## 安装RabbitMQ

下载RabbitMQ的rpm安装包

```
# wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.8/rabbitmq-server-3.8.8-1.el6.noarch.rpm
```

添加签名

```
# rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
```

安装rabbitmq-server

```
# rpm -Uvh rabbitmq-server-3.8.8-1.el6.noarch.rpm
```

启动RabbitMQ

```
# systemctl start rabbitmq-server
```

把RabbitMQ加入开机自启

```
# systemctl enable rabbitmq-server
```

## RabbitMQ Web页面管理

开启RabbitMQ web management console

```
# rabbitmq-plugins enable rabbitmq_management
```

更改rabbitmq目录的权限

```
# chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/
```

创建一个用户名为admin，密码为password的用户，password可根据实际情况自己确定。

```
# rabbitmqctl add_user admin password
```

把创建的admin用户授权为administrator

```
# rabbitmqctl set_user_tags admin administrator
# rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```

用刚才设定的用户名和密码登录rabbitmq的web页面

```
http://Your_Server_IP:15672
```


详细安装请参考github链接：
https://gist.github.com/fernandoaleman/fe34e83781f222dfd8533b36a52dddcc


# python 关于rabbitmq的模块安装

## 用pip命令安装rabbitmq的模块
```
# pip install pika -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
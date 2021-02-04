# 使用docker安装apollo和mysql

## docker安装指南
参考： https://yeasy.gitbook.io/docker_practice/install/centos

## docker-compose安装
```
# curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# chmod +x /usr/local/bin/docker-compose
# ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
# docker-compose --version
```

## clone apollo项目源码到/opt目录
```
# cd /opt
# git clone https://github.com/ctripcorp/apollo.git
```

## 进入项目目录并使用docker-compose启动apollo项目
```
# cd /opt/docker-quick-start
# nohup docker-compose up &
```
参考： https://ctripcorp.github.io/apollo/#/zh/deployment/quick-start-docker

# 使用pymysql模块和mysql Say Hi
## 安装pymysql模块
```
# pip install pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple/
```


# 使用pandas模块和mysql Say Hi
## 安装sqlalchemy模块和pandas模块
```
# pip install sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple/
# pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

注意：本目录下的conf/config.yaml中的信息需要更新为自己的mysql的真实信息才可以进行测试本目录中的两个py脚本。

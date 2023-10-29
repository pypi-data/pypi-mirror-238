## smb_server 模块是smartnotebook 管理服务模块，前端交互服务模块

### notebook 管理
### ds 数据源配置管理
### user 用户管理



## 打包
python setup.py sdist upload -r  http://127.0.0.1:8080/
## 安裝
pip install snb_server -i http://127.0.0.1:8080/
pip install snb_server -i http://127.0.0.1:8080/ --force
## 卸載
pip uninstall snb_server -y

## 運行
python -m snb_server


## 
apt-get install  libnfs-dev/stable

apt search  libnfs



# Release  2023/10/07 
docker stop snb-server-231007 
docker rm snb-server-231007 
docker rmi snb/server:v1.5
docker build -t snb/server:v1.5 .
docker run -p 9000:9000 -v /data01/snb-server/home:/home --name snb-server-231007 snb/server:v1.5



# Release 打包pip、上传；构建镜像及上传
## 1. jenkins  自动化部分,及编译局/加密
1. 自动编译web 到  /var/lib/jenkins/workspace/snb_web/dist
2. 自动编译/加密(pyarmor-7) server 到 /var/lib/jenkins/workspace/snb_server
3. node 到 /var/lib/jenkins/workspace/snb_node
4. plugin 手工加密(pyarmor-7)执行:/var/lib/jenkins/workspace/sh_release_plugin_armor.sh  ,加密的代码路径: /var/lib/jenkins/workspace/snb_plugin/dist
5. 数据库：mysql -uroot -pSnbMysql_WXY_231008 snb_server_db 增量

## 2. pip 打包/上传pypi
###   1. plugin 打包/上传pip
```shell
source  /root/.bashrc
conda activate python3913
cd /var/lib/jenkins/workspace/snb_plugin/dist
python setup.py sdist
twine upload dist/*
```
###   2. node 打包/上传pip
```shell
source  /root/.bashrc
conda activate python3913
cd /var/lib/jenkins/workspace/snb_node
python setup.py sdist
twine upload dist/*
```

###   3. server 打包/上传pip
```shell
source  /root/.bashrc
conda activate python3913
cd /var/lib/jenkins/workspace/snb_server
python setup.py sdist
twine upload dist/*
```
### 2.1 验证清华源有没有同步
https://pypi.tuna.tsinghua.edu.cn/simple/snb-server/
https://pypi.tuna.tsinghua.edu.cn/simple/snb-node/
https://pypi.tuna.tsinghua.edu.cn/simple/snb-plugin/


## 3. 镜像构建
###   1. node 镜像构建
```shell
export snb_ver=V1.5.1
cd /var/lib/jenkins/workspace/snb_node
docker rmi snb/node:${snb_ver}
docker build -t snb/node:${snb_ver} .  --no-cache
```
###   2. server 镜像构建
```shell
cd /var/lib/jenkins/workspace/snb_server
docker rmi snb/server:${snb_ver}
docker build -t snb/server:${snb_ver} . --no-cache
```

### 3. web 镜像构建
```
cd /var/lib/jenkins/workspace/snb_web
docker rmi snb/web:${snb_ver}
docker build -t snb/web:${snb_ver} . --no-cache
```

## 4. 镜像上传
```
docker login -u smartnotebook --password=dckr_pat_wLYdMhkzlRPweaYRlrQ53P5PctM
docker tag snb/web:${snb_ver} smartnotebook/snb-web:${snb_ver}
docker push smartnotebook/snb-web:${snb_ver}

docker login -u smartnotebook --password=dckr_pat_wLYdMhkzlRPweaYRlrQ53P5PctM
docker tag snb/node:${snb_ver} smartnotebook/snb-node:${snb_ver}
docker push smartnotebook/snb-node:${snb_ver}

docker login -u smartnotebook --password=dckr_pat_wLYdMhkzlRPweaYRlrQ53P5PctM
docker tag snb/server:${snb_ver} smartnotebook/snb-server:${snb_ver}
docker push smartnotebook/snb-server:${snb_ver}
```


# 构建镜像/上传 脚本 

```shell
# 设置ver 编号
export snb_ver=V1.6  # 2023-11-22 发布

#1.node 镜像构建
cd /var/lib/jenkins/workspace/snb_node
docker rmi snb/node:${snb_ver}
docker build -t snb/node:${snb_ver} .  --no-cache

#2.server 镜像构建

cd /var/lib/jenkins/workspace/snb_server
docker rmi snb/server:${snb_ver}
docker build -t snb/server:${snb_ver} . --no-cache

###3. web 镜像构建

cd /var/lib/jenkins/workspace/snb_web
docker rmi snb/web:${snb_ver}
docker build -t snb/web:${snb_ver} . --no-cache

#4. 镜像上传

docker login -u smartnotebook --password=dckr_pat_wLYdMhkzlRPweaYRlrQ53P5PctM
docker tag snb/web:${snb_ver} smartnotebook/snb-web:${snb_ver}
docker push smartnotebook/snb-web:${snb_ver}

docker tag snb/node:${snb_ver} smartnotebook/snb-node:${snb_ver}
docker push smartnotebook/snb-node:${snb_ver}

docker tag snb/server:${snb_ver} smartnotebook/snb-server:${snb_ver}
docker push smartnotebook/snb-server:${snb_ver}

```
FROM docker.io/silverlogic/python3.8

MAINTAINER net-compute

WORKDIR /network-x
COPY ./ /network-x/

# 安装python 和 pip
RUN cd /network-x \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt \
    && pip3 install nebula3-python==3.1.0 -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD python3 /network-x/src/main/run.py
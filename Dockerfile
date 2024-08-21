FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# WORKDIR /home/ubuntu

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install sudo -y

# RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin
# RUN echo 'admin:admin' | chpasswd
# RUN echo 'admin ALL=(ALL) NOPASSWD: ALL' | tee -a /etc/sudoers
# RUN sudo chown -R admin /home/ubuntu
# USER admin
# RUN service ssh start

# install dependencies
RUN apt-get -y install --no-install-recommends \
    build-essential \
    libboost-all-dev \
    libssl-dev \
    libsqlite3-dev \
    pkg-config \
    python3 \
    python3-pip \
    python-is-python3 \
    git \
    ca-certificates \
    libcrypto++-dev \
    libpcap-dev \
    libsystemd-dev \

    openssh-server \
    iproute2 \
    iputils-ping \
    net-tools \
    nano \
    vim \
    tcpdump \

    libboost-system1.74.0 \
    libboost-filesystem1.74.0 \
    libboost-date-time1.74.0 \
    libboost-iostreams1.74.0 \
    libboost-regex1.74.0 \
    libboost-program-options1.74.0 \
    libboost-chrono1.74.0 \
    libboost-random1.74.0 \
    libboost-thread1.74.0 \
    libboost-log1.74.0 \
    libboost-stacktrace1.74.0 \
    libpcap0.8 \
    sqlite3

# ndn-cxx
RUN git clone -b ndn-cxx-0.8.1 \
    https://github.com/named-data/ndn-cxx.git &&\
    cd ndn-cxx &&\
    ./waf configure &&\
    ./waf &&\
    ./waf install &&\
    cd .. && rm -r ndn-cxx &&\
    ldconfig
# NFD
RUN git clone -b NFD-22.12 \
    --depth 1 --recursive https://github.com/named-data/NFD.git &&\
    cd NFD &&\
    ./waf configure &&\
    ./waf &&\
    ./waf install &&\
    cp build/nfd.conf.sample /usr/local/etc/ndn/nfd.conf &&\
    cd .. && rm -r NFD
# NDN tools
RUN git clone -b ndn-tools-22.12 https://github.com/named-data/ndn-tools.git &&\
    cd ndn-tools &&\
    ./waf configure &&\
    ./waf &&\
    ./waf install &&\
    cd .. && rm -r ndn-tools

# NDN-Traffic-Generator
RUN git clone https://github.com/named-data/ndn-traffic-generator.git &&\
    cd ndn-traffic-generator &&\
    git reset --hard 08208497d8cf7843d58e744081e60c84e1e81216 &&\
    ./waf configure &&\
    ./waf &&\
    ./waf install &&\
    cd .. && rm -r ndn-traffic-generator

# NDN-SVS
RUN git clone https://github.com/named-data/ndn-svs.git &&\
    cd ndn-svs &&\
    git reset --hard f6129786571b73e5a73256325d4b1d23af0f5d8e &&\
    ./waf configure &&\
    ./waf &&\
    ./waf install &&\
    cd .. && rm -r ndn-svs


# Python-NDN
RUN pip install python-ndn ndn-storage

# remove build dependencies
# RUN apt-get remove --purge -y \
#     build-essential \
#     libboost-all-dev \
#     libssl-dev \
#     libsqlite3-dev \
#     pkg-config \
#     python3 \
#     python3-pip \
#     python-is-python3 \
#     git \
#     ca-certificates \
#     libcrypto++-dev \
#     libpcap-dev

# RUN apt-get remove -y .*-dev &&\
#     apt-get autoremove -y &&\
#     rm -rf /var/lib/apt/lists /tmp/*

COPY nfd-start /usr/local/bin/
RUN chmod +x /usr/local/bin/nfd-start

# RUN sudo mkdir /var/run/sshd
# RUN sudo chmod 0755 /var/run/sshd

# RUN sudo mkdir /run/nfd
# RUN sudo chmod 0755 /run/nfd
# RUN sudo chown -R admin /run/nfd

COPY repo /root/repo
COPY client /root/client

RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config
EXPOSE 22
# RUN usermod -d /home/ubuntu root

COPY scripts/run_repo.sh /root/run_repo.sh
COPY scripts/insert_file.sh /root/insert_file.sh

# Pathch ndn
RUN sudo sed -i '291 i\    if params is None:\n        return ret' /usr/local/lib/python3.10/dist-packages/ndn/app_support/nfd_mgmt.py
RUN sudo sed -i '422 i\        await aio.sleep(1)' /usr/local/lib/python3.10/dist-packages/ndn/app.py

ENTRYPOINT nfd-start -f

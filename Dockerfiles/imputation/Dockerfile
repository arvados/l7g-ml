FROM arvados/jobs
MAINTAINER Jiayong Li <jiayong@curoverse.com>

USER root

RUN apt-get update -q

RUN apt-get install -qy build-essential wget cmake zlib1g-dev

# Installing java8
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y software-properties-common
RUN apt-get update
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee /etc/apt/sources.list.d/webupd8team-java.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
RUN apt-get update
RUN apt-get install -y oracle-java8-installer
RUN apt-get clean

WORKDIR /

# Getting beagle
RUN wget http://faculty.washington.edu/browning/beagle/beagle.27Jan18.7e1.jar

WORKDIR /

# Installing htslib for tabix/bgzip
RUN wget https://github.com/samtools/htslib/releases/download/1.3.1/htslib-1.3.1.tar.bz2 && \
    tar -xjvf htslib-1.3.1.tar.bz2 && \
    cd htslib-1.3.1 && ./configure && make && make install

WORKDIR /

# Installing bcftools
RUN wget https://github.com/samtools/bcftools/releases/download/1.3.1/bcftools-1.3.1.tar.bz2 && \
    tar -xjvf bcftools-1.3.1.tar.bz2 && \
    cd bcftools-1.3.1 && make && make install

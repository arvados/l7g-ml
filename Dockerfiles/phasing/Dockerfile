FROM arvados/jobs
MAINTAINER Jiayong Li <jiayong@curoverse.com>

USER root

RUN apt-get update -q

RUN apt-get install -qy build-essential wget cmake zlib1g-dev

# Installing eagle v2.4
RUN wget https://data.broadinstitute.org/alkesgroup/Eagle/downloads/Eagle_v2.4.tar.gz && \
    tar -xzvf Eagle_v2.4.tar.gz && cp Eagle_v2.4/eagle /usr/local/bin

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

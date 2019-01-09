FROM ubuntu:latest
MAINTAINER Kevin Fang <kfang@curii.com>
USER root

# install necessary dependencies
RUN apt-get update -y && \
    apt-get install -y wget \ 
        gcc \
        libbz2-dev \
        libperl-dev \
        liblzma-dev \
        dtrx \
        autoconf \
        zlib1g-dev \
        make \
        python \
        python-pip \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
        libmysqlclient-dev \
        git \
        curl \
        g++ \
        libgsl0-dev \
        swig \
        clustalo \
        perl \
        snp-sites \
    && rm -rf /var/lib/apt/lists/*

# install htslib and bcftools
RUN git clone git://github.com/samtools/htslib.git && \
    cd htslib && \
    autoheader && autoconf && ./configure && make && make install && \
    cd .. && \
    git clone git://github.com/samtools/bcftools.git && \
    cd bcftools && \
    autoheader && autoconf && ./configure --enable-libgsl --enable-perl-filters && \
    make && \
    make install
 

# alignment tools + variant decoder
RUN cpan DBI && \
    cpan DBD::mysql && \
    cpan Module::Build && \
    cpan Try::Tiny && \
    cpan JSON 

# Ensembl-VEP installer
RUN git clone https://github.com/Ensembl/ensembl-vep && \
    cd ensembl-vep && \
    perl INSTALL.pl
   
ENV PATH="/ensembl-vep:${PATH}"

RUN pip install biopython \
    pyyaml

RUN pip install description-extractor --process-dependency-links

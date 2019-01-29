FROM ubuntu:latest
MAINTAINER Kevin Fang <kfang@curii.com>
USER root

# install necessary dependencies
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget \ 
	gcc \
        libbz2-dev \
        liblzma-dev \
        dtrx \
	zlib1g-dev \
        make \
        python \
        python-pip \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
        g++

# install python specific packages
RUN pip install --upgrade pip==18.0

RUN pip install scikit-learn==0.19.1 \
        matplotlib \
        pandas \
	dask \
	dask_ml \
        scipy \
        numpy \
	toolz \
        ipython[all]

FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
  r-base \
  r-cran-randomforest \
  python3.8 \
  python3-pip \
  python3-setuptools \
  python3-dev \
  gfortran \
  python3-numpy \
  python3-pandas \
  python3-scipy \
  python3-matplotlib \
  libpng-dev \
  libapt-pkg-dev \
  liblapack-dev \
  libopenblas-dev

RUN apt-get clean

RUN pip3 install sklearn
RUN pip3 install --upgrade scipy
RUN pip3 install notebook

RUN R -e "install.packages('Matrix', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('RcppEigen', repos='http://cran.us.r-project.org')"
RUN R -e "install.packages('glmnet', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('reticulate', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('foreach', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('ggplot2', repos = 'http://cran.us.r-project.org')"

FROM debian:buster

USER root

RUN apt-get update && apt-get install -y --no-install-recommends gnupg
RUN apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN echo "deb http://cloud.r-project.org/bin/linux/debian buster-cran35/" > /etc/apt/sources.list.d/cran.list

RUN apt-get update && \
    apt-get -y install r-cran-rcpp r-cran-data.table libapt-pkg-dev less \
      wget \
      python-pip \
      python-numpy \
      python-scipy \
      python-matplotlib \
      python-pandas && \
    apt-get clean

RUN pip install sklearn
RUN pip install --upgrade scipy
RUN pip install seaborn


RUN R -e "install.packages('Matrix', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('glmnet', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('reticulate', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('foreach', repos = 'http://cran.us.r-project.org')"
RUN R -e "install.packages('selectiveInference', repos = 'http://cran.us.r-project.org')"


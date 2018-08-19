FROM phusion/baseimage:0.9.17

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
RUN apt-get -y update && \
    apt-get install -y curl wget bzip2 nano

RUN curl -L -O http://downloads.sourceforge.net/project/cgatools/1.8.0/cgatools-1.8.0.1-linux_binary-x86_64.tar.gz &&\
   tar -xzf cgatools-1.8.0.1-linux_binary-x86_64.tar.gz &&\
   cp cgatools-1.8.0.1-linux_binary-x86_64/bin/cgatools /usr/local/bin/cgatools

# install CGAtools genome
RUN mkdir -p /usr/local/share/cgatools/genomes &&\
  cd /usr/local/share/cgatools/genomes &&\
  wget ftp://ftp.completegenomics.com/ReferenceFiles/build37.crr

#COPY mkvcf.sh /usr/local/bin/mkvcf.sh
#RUN chmod 755 /usr/local/bin/mkvcf.sh

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN rm -fr /cgatools-1.8.0.1-linux_binary-x86_64*

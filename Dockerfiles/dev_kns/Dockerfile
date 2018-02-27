# The image, and thus container created with this are intended
# to be used by Keldin for day-to-day development work.
# Cleaner, simpler images will be used for pipelines.
FROM arvados/jobs:latest

USER root

# Install some essentials
RUN apt-get update
RUN apt-get install apt-utils -y
RUN apt-get install build-essential -y
RUN apt-get install less -y
RUN apt-get install wget -y
RUN apt-get install vim -y
RUN apt-get clean

# Personalize vim
RUN echo "inoremap jk <Esc>" > ~/.vimrc
RUN echo "inoremap kj <Esc>" >> ~/.vimrc 

# Installing python packages
# scipy fails to install with pip3 but succeeds when we use apt-get.
# For consistency, we therefore use apt-get to install all the
# packages we need.
# Must specify python3, since just python ends up installing for
# python2 only.
# Must use -y option in order to default "Yes" to all requests for consent to
# use disk space.

RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install python3-numpy -y
RUN apt-get install python3-scipy -y
RUN apt-get install python3-matplotlib -y
RUN apt-get install python3-pandas -y
RUN apt-get clean

# Surprisingly, apt-get install python3-sklearn fails because sklearn cannot
# be found. Therefore we break with the consistency of using apt-get so far
# and instead use pip3 to get sklearn (scikit-learn)

RUN pip3 install sklearn

# Install bioinformatics tools
RUN apt-get update
RUN apt-get install vcftools -y
RUN apt-get install zlib1g-dev -y
RUN apt-get install libncurses5-dev -y
RUN apt-get install libbz2-dev -y
RUN apt-get install liblzma-dev -y
RUN apt-get clean

# Get SAMtools
RUN wget https://github.com/samtools/samtools/releases/download/1.5/samtools-1.5.tar.bz2
RUN bzip2 -d samtools-1.5.tar.bz2
RUN tar xf samtools-1.5.tar
RUN cd samtools-1.5 && ./configure && make && make install

# Get BCFtools
RUN wget https://github.com/samtools/bcftools/releases/download/1.5/bcftools-1.5.tar.bz2
RUN bzip2 -d bcftools-1.5.tar.bz2
RUN tar xf bcftools-1.5.tar
RUN cd bcftools-1.5 && ./configure && make && make install

# Get Eagle
RUN wget https://data.broadinstitute.org/alkesgroup/Eagle/downloads/Eagle_v2.3.4.tar.gz
RUN gunzip Eagle_v2.3.4.tar.gz
RUN tar -x -f Eagle_v2.3.4.tar
# Move eagle executable into path
RUN cp Eagle_v2.3.4/eagle /usr/local/bin/

# Get java (in order to run Beagle)
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee /etc/apt/sources.list.d/webupd8team-java.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
RUN apt-get update
RUN apt-get install -y oracle-java8-installer
RUN apt-get clean

# Get Beagle
RUN mkdir /Beagle
RUN cd /Beagle
RUN wget http://faculty.washington.edu/browning/beagle/beagle.08Jun17.d8b.jar
RUN wget http://faculty.washington.edu/browning/beagle/bref.08Jun17.d8b.jar
RUN wget http://faculty.washington.edu/browning/beagle/test.08Jun17.d8b.vcf.gz
RUN wget http://faculty.washington.edu/browning/beagle/run.beagle.08Jun17.d8b.example

# Delete tar archives
RUN cd /
RUN rm samtools-1.5.tar
RUN rm bcftools-1.5.tar
RUN rm Eagle_v2.3.4.tar


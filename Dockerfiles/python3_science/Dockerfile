FROM arvados/jobs:latest

USER root

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

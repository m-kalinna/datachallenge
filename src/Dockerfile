FROM ubuntu:16.04

#JDK
RUN apt-get update && apt-get -y upgrade && apt-get -y install software-properties-common && add-apt-repository ppa:webupd8team/java -y && apt-get update
RUN (echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections) && apt-get install -y oracle-java8-installer oracle-java8-set-default
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
ENV PATH $JAVA_HOME/bin:$PATH

# SPARK
RUN apt-get -y install curl
ARG SPARK_ARCHIVE=http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz
ENV SPARK_HOME /usr/local/spark-2.0.2-bin-hadoop2.7
ENV PATH $PATH:${SPARK_HOME}/bin
ENV PYTHONPATH /usr/local/spark-2.0.2-bin-hadoop2.7/python/
RUN curl -s ${SPARK_ARCHIVE} | tar -xz -C /usr/local/

#PYTHON
RUN apt-get -y install python2.7 python-setuptools
RUN easy_install pip
RUN pip install py4j logging argparse

#UTF-8
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

#YELP
COPY yelp_dataset_challenge_round9.tar /data/
COPY yelp_data_loader.py /yelp/
COPY spark_connector.py /yelp/

#EXECUTION
ENV PYTHONIOENCODING=UTF-8
WORKDIR /yelp
#CMD [ "locale" ]
CMD [ "python", "yelp_data_loader.py", "-f", "/data/yelp_dataset_challenge_round9.tar", "-c", "2" ]

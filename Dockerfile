FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
ARG LANGUAGE=en_US.UTF-8
ARG LANG=en_US.UTF-8
ARG LC_ALL=en_US.UTF-8
ARG locale-gen en_US.UTF-8
WORKDIR /all
RUN apt update && apt upgrade -y && apt install -y coreutils software-properties-common git pip parallel wget make gcc locales
RUN pip install scikit-learn==1.0.1 gdown==5.2.0 pandas==2.0.3
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt install -y gcc-11 g++-11

COPY GP-GOMEA /all/GP-GOMEA
WORKDIR GP-GOMEA
RUN chmod +x deps_ubuntu
RUN ./deps_ubuntu
RUN make

#COPY gp-experiments /all/gp-experiments
#WORKDIR ../gp-experiments
#RUN chmod 777 *.sh
#RUN chmod 777 *.py

#VOLUME /all/gp-experiments
#WORKDIR ../..
#COPY script.sh .
#RUN chmod 777 script.sh
#ENTRYPOINT ["/script.sh"]

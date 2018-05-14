
FROM debian:stable

RUN apt-get update
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev
RUN apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
RUN apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev
RUN cd root; mkdir Downloads; cd Downloads ; wget --quiet https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz; ls -la
RUN cd /root/home/Downloads; tar xvf Python-3.6.3.tgz
RUN cd Python-3.6.3
RUN ./configure --enable-optimizations
RUN make -j8
RUN sudo make install
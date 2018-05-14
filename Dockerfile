
FROM debian:stable

RUN apt-get update
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev
RUN apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
RUN apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev
RUN cd /root; mkdir Downloads; cd Downloads ; wget --quiet https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz; ls -la
RUN ls; cd /root/Downloads; ls; tar xvf Python-3.6.5.tgz; ls
RUN cd /root/Downloads/Python-3.6.5/; ./configure; make -j8; make install
# RUN ./configure --enable-optimizations
RUN /usr/local/bin/pip3 install discord python-dateutil numpy flake8

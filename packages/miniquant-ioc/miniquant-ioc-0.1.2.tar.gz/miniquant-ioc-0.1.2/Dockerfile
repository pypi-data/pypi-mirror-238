FROM python:latest

# Assuming that we have miniquant-ioc sources in '/miniquant_ioc_src'
# Auto-sensing for miniquant sources in '/miniquant_src'

RUN useradd -u 9999 cthulhu 

RUN if [ -d /miniquant_src ]; then pip install /miniquant_src[softioc] ; \
    else pip install miniquant[softioc] ; fi

ENV MINIQUANT_HHLIB=/usr/local/lib/hhlib.so

RUN mkdir -p `dirname $MINIQUANT_HHLIB` && \
    curl -L -o $MINIQUANT_HHLIB \
    https://github.com/PicoQuant/HH400-v3.x-Demos/raw/master/Linux/64bit/library/hhlib.so && \
    chmod a+x $MINIQUANT_HHLIB

RUN apt-get update && apt-get install -y libusb-0.1-4 

RUN pip install /miniquant_ioc_src && \
    mkdir -p /etc/miniquant &&  \
    cp /miniquant_ioc_src/examples/*.yaml /etc/miniquant

USER miniquant

CMD miniquant-ioc -c /etc/miniquant/harp.yaml

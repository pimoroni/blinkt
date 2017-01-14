FROM resin/rpi-raspbian:jessie

RUN apt-get update -qy && apt-get install -qy \
    python \
    python-rpi.gpio
WORKDIR /root/
COPY . .
WORKDIR /root/library
RUN python setup.py install
WORKDIR /root/examples/
ENTRYPOINT []
CMD ["python", "larson.py"]

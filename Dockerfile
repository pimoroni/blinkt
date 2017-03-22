FROM resin/rpi-raspbian:jessie

RUN apt-get update -qy && apt-get install -qy \
    python \
    python-rpi.gpio

# Cancel out any Entrypoint already set in the base image.
ENTRYPOINT []	

WORKDIR /root/

COPY library	library
WORKDIR /root/library
RUN python setup.py install

WORKDIR /root/
COPY examples	examples
WORKDIR /root/examples/

CMD ["python", "larson.py"]

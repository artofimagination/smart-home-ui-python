FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -yqq \
    python3-pip \
    python3-tk \
    python3-pyqt5.qtopengl \
    python3-pyqt5.qtwebengine \
    x11-apps

RUN pip install -U pip
RUN pip install pyqt5 numpy pandas pyqtgraph

FROM python:latest

RUN useradd -u 9999 cthulhu 

RUN if [ -d /kronos_src ]; then pip install /kronos_src; else pip install dg645-ioc; fi

USER cthulhu

CMD dg645-ioc

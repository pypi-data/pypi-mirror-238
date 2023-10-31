FROM python:latest

RUN useradd -u 9999 cthulhu 

RUN if [ -d /fridge_src ]; then pip install /fridge_src; else pip install ls336-ioc; fi

USER cthulhu

CMD ls336-ioc

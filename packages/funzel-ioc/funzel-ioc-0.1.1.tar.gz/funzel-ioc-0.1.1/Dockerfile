FROM python:latest

RUN useradd -u 9999 cthulhu 

RUN if [ -d /funzel_src ]; then pip install /funzel_src; else pip install funzel-ioc; fi

USER cthulhu

CMD funzel-ioc

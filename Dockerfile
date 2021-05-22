FROM debian:sid

COPY geckodriver /usr/local/bin/
COPY get_ps5.py /usr/local/bin/

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install firefox xvfb python3-selenium python3-pyvirtualdisplay python3-requests
RUN chmod 755 /usr/local/bin/get_ps5.py && chmod 755 /usr/local/bin/geckodriver

ENV PYTHONUNBUFFERED=1

CMD /usr/local/bin/get_ps5.py
FROM ubuntu:17.10

ENV USERNAME              user
ENV UID                   1000
ENV GID                   1000

RUN \
  sed -i \
    s/archive\.ubuntu\.com/la-mirrors.evowise.com/g /etc/apt/sources.list && \
  apt-get update && \
  apt-get install --no-install-recommends -y \
    texlive \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-lang-spanish \
    texlive-xetex \
    lmodern \
    ttf-ubuntu-font-family \
    openjdk-8-jre \
    virtualenv python-virtualenv \
    locales \
    curl && \
  rm -rf /var/lib/apt/lists/*

RUN locale-gen es_AR.UTF-8 && update-locale
ENV LC_ALL es_AR.UTF-8

RUN curl -LO \
  https://github.com/jgm/pandoc/releases/download/2.0.6/pandoc-2.0.6-1-amd64.deb && \
  dpkg -i pandoc-2.0.6-1-amd64.deb && \
  rm pandoc-2.0.6-1-amd64.deb

RUN curl -L -o /usr/local/bin/plantuml.jar \
  http://sourceforge.net/projects/plantuml/files/plantuml.jar/download
ADD plantuml /usr/local/bin/

RUN \
  groupadd --gid ${GID} ${USERNAME} && \
  useradd --uid ${UID} --gid ${GID} --create-home ${USERNAME}

ADD entrypoint.sh /
RUN sed -i s/USERNAME/${USERNAME}/g /entrypoint.sh

USER      ${USERNAME}

RUN virtualenv -p python3 /home/${USERNAME}/env

RUN \
  . /home/${USERNAME}/env/bin/activate && \
  curl -L -o /tmp/requirements.txt \
     https://raw.githubusercontent.com/bmc/ebook-template/master/requirements.txt && \
  pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt && \
  pip install WeasyPrint

WORKDIR   /home/${USERNAME}/book
VOLUME    /home/${USERNAME}/book

ENTRYPOINT ["/entrypoint.sh"]
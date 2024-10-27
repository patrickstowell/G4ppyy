FROM johnpatrickstowell/pycrust:jupyter
ENV PYCRUST_PORT=8888
EXPOSE 8888
WORKDIR /data/

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER=${NB_USER}
ENV NB_UID=${NB_UID}
ENV HOME=/home/${NB_USER}
WORKDIR /home/${NB_USER}

WORKDIR /data/


USER root
RUN useradd -ms /bin/bash joyvan
RUN usermod -u 1101 pycrust
RUN usermod -u ${NB_UID} joyvan
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


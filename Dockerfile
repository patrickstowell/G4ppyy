FROM johnpatrickstowell/pycrust:jupyter
ENV PYCRUST_PORT=8888
EXPOSE 8888
WORKDIR /data/

ARG NB_USER=pycrust
ARG NB_UID=1000
ENV USER=${NB_USER}
ENV NB_UID=${NB_UID}
ENV HOME=/home/${NB_USER}

USER root
RUN usermod -u ${NB_UID} pycrust
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}


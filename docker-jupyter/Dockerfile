FROM almalinux:9.3

RUN yum update -y && yum install -y expat-devel libXmu-devel freeglut-devel git gcc g++ cmake nano wget python3 python3-pip git python3-devel 

WORKDIR /app/Geant4-11.2.2-Linux/share/Geant4/data/
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4ABLA3.3/ ./G4ABLA3.3
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4EMLOW8.5/ ./G4EMLOW8.5
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4ENSDFSTATE2.3/ ./G4ENSDFSTATE2.3
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4INCL1.2/ ./G4INCL1.2
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4NDL4.7.1/ ./G4NDL4.7.1
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4PARTICLEXS4.0/ ./G4PARTICLEXS4.0
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4PII1.3/ ./G4PII1.3
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4SAIDDATA2.0/ ./G4SAIDDATA2.0
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/G4TENDL1.4/ ./G4TENDL1.4
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/PhotonEvaporation5.7/ ./PhotonEvaporation5.7
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/share/Geant4/data/RadioactiveDecay5.6/ ./RadioactiveDecay5.6

WORKDIR /app/Geant4-11.2.2-Linux/
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/lib64 ./lib64
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/include ./include
COPY --from=johnpatrickstowell/pycrust:g4base /app/Geant4-11.2.2-Linux/bin ./bin

RUN python3 -m pip install jupyterlab matplotlib numpy pandas plotly

RUN STDCXX=17 MAKE_NPROCS=8 pip install --verbose cppyy 

RUN chmod 777 -R /app/Geant4-11.2.2-Linux/bin/
#RUN chmod 777 -R /root/

RUN yum install -y sudo passwd which; dnf module install -y nodejs:20; pip install k3d numpy matplotlib pandas; jupyter labextension install k3d; jupyter labextension enable k3d; dnf autoremove -y nodejs:20

RUN useradd -ms /bin/bash pycrust; echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers; passwd -d pycrust; usermod -aG wheel pycrust

USER pycrust

WORKDIR /app
WORKDIR /app/pycrust
WORKDIR /data/

ENV PYCRUST_PORT=8168
ENV PYCRUST_HOST=0.0.0.0
EXPOSE 8168

RUN cat <<EOF > /app/Geant4-11.2.2-Linux/bin/pycrust-jupyter
#!/bin/sh
jupyter lab --port \$PYCRUST_PORT --ip \$PYCRUST_HOST
EOF

RUN chmod +x /app/Geant4-11.2.2-Linux/bin/pycrust-jupyter; ln -sf /app/Geant4-11.2.2-Linux/bin/pycrust-jupyter /app/Geant4-11.2.2-Linux/bin/start;
RUN echo 'PS1="\[\033[38;5;208m\][ π - \u : \#:\W ] $ \[\033[0m\]"' >> /home/pycrust/.bashrc

COPY ./ /data/
WORKDIR /data/
RUN sudo chmod 777 /data/* /data/; sudo chmod 777 /data/

ENV PATH=//app/Geant4-11.2.2-Linux/bin/:$PATH
ENV LD_LIBRARY_PATH=/app/Geant4-11.2.2-Linux/lib64/
ENV LD_PRELOAD=/app/Geant4-11.2.2-Linux/lib64/libG4run.so 
ENV PYTHONPATH=/data/
ENV GEANT4_DATA_DIR=/app/Geant4-11.2.2-Linux/share/Geant4/data
ENV PATH=/app/Geant4-11.2.2-Linux/bin:/home/pycrust/.local/bin:/home/pycrust/bin://app/Geant4-11.2.2-Linux/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


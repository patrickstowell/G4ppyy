FROM almalinux:9.3

RUN yum update -y && yum install -y expat-devel libXmu-devel freeglut-devel git gcc g++ cmake nano wget python3 python3-pip git python3-devel 

WORKDIR /app/geant4-v11.2.2/install/share/Geant4/data/

COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4ABLA3.3/ ./G4ABLA3.3
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4EMLOW8.5/ ./G4EMLOW8.5
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4ENSDFSTATE2.3/ ./G4ENSDFSTATE2.3
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4INCL1.2/ ./G4INCL1.2
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4NDL4.7.1/ ./G4NDL4.7.1
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4PARTICLEXS4.0/ ./G4PARTICLEXS4.0
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4PII1.3/ ./G4PII1.3
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4SAIDDATA2.0/ ./G4SAIDDATA2.0
# COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/G4TENDL1.4/ ./G4TENDL1.4
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/PhotonEvaporation5.7/ ./PhotonEvaporation5.7
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/share/Geant4/data/RadioactiveDecay5.6/ ./RadioactiveDecay5.6

RUN wget https://cern.ch/geant4-data/datasets/G4TENDL.1.4.tar.gz; tar -zxvf G4TENDL.1.4.tar.gz; rm G4TENDL.1.4.tar.gz

WORKDIR /app/geant4-v11.2.2/install/
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/lib64 ./lib64
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/include ./include
COPY --from=johnpatrickstowell/pycrust:jupyter /app/geant4-v11.2.2/install/bin ./bin

RUN python3 -m pip install jupyterlab matplotlib numpy pandas plotly

RUN STDCXX=17 MAKE_NPROCS=8 pip install --verbose cppyy 

RUN chmod 777 -R /app/geant4-v11.2.2/install/bin/

RUN yum install -y sudo passwd which; dnf module install -y nodejs:20; pip install k3d numpy matplotlib pandas; jupyter labextension install k3d; jupyter labextension enable k3d; dnf autoremove -y nodejs:20

RUN python3 -m pip install git+https://github.com/patrickstowell/G4ppyy.git@v0.0.1

RUN useradd -ms /bin/bash g4user; echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers; passwd -d g4user; usermod -aG wheel g4user

USER g4user


WORKDIR /app
WORKDIR /data/

ENV G4PPYY_PORT=8168
ENV G4PPYY_HOST=0.0.0.0
EXPOSE 8168

RUN cat <<EOF > /app/geant4-v11.2.2/install/bin/g4ppyy-jupyter
#!/bin/sh
jupyter lab --port \$G4PPYY_PORT --ip \$G4PPYY_HOST
EOF

RUN cat <<EOF > /app/geant4-v11.2.2/install/bin/g4ppyy-update
#!/bin/sh
sudo python3 -m pip uninstall g4ppyy
sudo python3 -m pip install git+https://github.com/patrickstowell/G4ppyy.git@main
EOF

RUN chmod +x /app/geant4-v11.2.2/install/bin/g4ppyy-update; chmod +x /app/geant4-v11.2.2/install/bin/g4ppyy-jupyter; ln -sf /app/geant4-v11.2.2/install/bin/g4ppyy-jupyter /app/geant4-v11.2.2/install/bin/start;
RUN echo 'PS1="\[\033[38;5;208m\][ \u : \#:\W ] $ \[\033[0m\]"' >> /home/g4user/.bashrc

WORKDIR /data/
RUN sudo chmod 777 /data/; sudo chmod 777 /data/

ENV PATH=//app/geant4-v11.2.2/install/bin/:$PATH
ENV LD_LIBRARY_PATH=/app/geant4-v11.2.2/install/lib64/
ENV LD_PRELOAD=/app/geant4-v11.2.2/install/lib64/libG4run.so 
ENV PYTHONPATH=/data/
ENV GEANT4_DATA_DIR=/app/geant4-v11.2.2/install/share/Geant4/data
ENV PATH=/app/geant4-v11.2.2/install/bin:/home/g4user/.local/bin:/home/g4user/bin://app/geant4-v11.2.2/install/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY ./ExampleB1.py	/data/ExampleB1.py
COPY ./SimpleSimulation.ipynb /data/SimpleSimulation.ipynb

RUN echo "sudo python3 -m pip uninstall -y g4ppyy; sudo python3 -m pip install git+https://github.com/patrickstowell/G4ppyy.git@main" > /app/geant4-v11.2.2/install/bin/g4ppyy-update; chmod +x /app/geant4-v11.2.2/install/bin/g4ppyy-update



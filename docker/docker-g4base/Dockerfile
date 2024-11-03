FROM almalinux:9.3

RUN yum update -y && yum install -y expat-devel libXmu-devel freeglut-devel git gcc g++ cmake nano wget python3 python3-pip git python3-devel && pip install "pybind11[global]"

WORKDIR /app
RUN <<EOF
wget https://geant4-data.web.cern.ch/releases/lib4.11.2.p02/Linux-g++11.4.1-Alma9.tar.gz
tar -zxf Linux-g++11.4.1-Alma9.tar.gz 
mkdir /app/Geant4-11.2.2-Linux/share/Geant4/data/
source /app/Geant4-11.2.2-Linux/bin/geant4.sh
EOF

RUN <<EOF
cd /app/Geant4-11.2.2-Linux/share/Geant4/data/
wget https://cern.ch/geant4-data/datasets/G4NDL.4.7.1.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4EMLOW.8.5.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4PhotonEvaporation.5.7.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.6.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4PARTICLEXS.4.0.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4RealSurface.2.2.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4SAIDDATA.2.0.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4ABLA.3.3.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4INCL.1.2.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.3.tar.gz &
wget https://cern.ch/geant4-data/datasets/G4TENDL.1.4.tar.gz & 

while true; do
  wait -n || {
    code="$?"
    ([[ $code = "127" ]] && exit 0 || exit "$code")
    break
  }
done;

for f in ./*.tar.gz;
do 
  tar -zxf $f
done

rm ./*.tar.gz
EOF


WORKDIR /app
ENV LD_LIBRARY_PATH=/app/Geant4-11.2.2-Linux/lib64
ENV GEANT4_DATA_DIR=/app/Geant4-11.2.2-Linux/share/Geant4/data
ENV PATH=/app/Geant4-11.2.2-Linux/bin:/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin




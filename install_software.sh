# mostly taken from S. Rappoccio's fastjet-tutorial
# https://github.com/rappoccio/fastjet-tutorial/blob/master/install_software.sh
# Ubuntu+tools, python, pip, python modules
apt-get update
apt-get install -y emacs nano wget g++ libtool rsync make x11-apps python3-dev python3-numpy python3-pip python3-tk 
rm -rf /var/lib/apt/lists/*
#pip install --no-cache-dir matplotlib scipy numpy scikit-learn keras tensorflow jupyter metakernel zmq notebook==5.* plaidml-keras plaidbench energyflow
pip3 install --no-cache-dir matplotlib scipy numpy scikit-learn keras tensorflow jupyter metakernel zmq notebook==5.* plaidml-keras plaidbench
update-alternatives --install /usr/bin/python python /usr/bin/python3 10
# fastjet
wget http://fastjet.fr/repo/fastjet-3.3.2.tar.gz \
    && tar xzf fastjet-3.3.2.tar.gz && rm fastjet-3.3.2.tar.gz \
    && cd fastjet-3.3.2 \
    && ./configure --prefix=/ --enable-pyext && make && make install \
    && cd .. 
# fastjet-contrib
wget http://fastjet.hepforge.org/contrib/downloads/fjcontrib-1.038.tar.gz \
    && tar xzf fjcontrib-1.038.tar.gz && rm fjcontrib-1.038.tar.gz \
    && cd fjcontrib-1.038 \
    && ./configure --fastjet-config=/bin/fastjet-config && make && make install \
    && cd .. 

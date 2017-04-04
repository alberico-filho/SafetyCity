# SafetyCity

Instalação do Openface

Opcao do userguide
apt-get install git


para instalacao do opencv 2


apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python2.7-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev 

wget https://github.com/Itseez/opencv/archive/2.4.11.zip

unzip 2.4.11.zip

cd opencv-2.4.11

mkdir build

cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ../(local do opencv baixado)

make

make install


Para instalar o dlib

apt-get install libboost-python-dev libopenblas-dev

wget https://github.com/davisking/dlib/releases/download/v18.16/dlib-18.16.tar.bz2

tar xfvj dlib-18.16.tar.bz2

cd dlib-18.16/python_examples

mkdir build

cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ../../tools/python

cmake --build . --config Release

sudo cp dlib.so /usr/local/lib/python2.7/dist-packages


apt-get install python-pip curl libreadline6-dev python-pgmagick libgraphicsmagick1-dev

instalar o torch tirado de http://torch.ch/docs/getting-started.html#_

curl -s https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash

git clone https://github.com/torch/distro.git ~/torch --recursive

cd ~/torch; ./install.sh


source ~/.bashrc

apt-get install 


luarocks install image

luarocks install nn

luarocks install dpnn

luarocks install optim

luarocks install csvigo

luarocks install trepl

luarocks install argcheck

luarocks install torchx

luarocks install graphicsmagick

luarocks install sys

luarocks install optnet


instalado dependencias para openface

apt-get install python-numpy  python-scipy python-pandas python-nose-exclude 

wget https://github.com/scikit-learn/scikit-learn/archive/0.17.X.zip

unzip 0.17.X.zip

cd scikit-learn-0.17.X

make

python2 setup.py install




para operar openface

git clone https://github.com/cmusatyalab/openface.git ~/openface --recursive

cd ~/openface

python setup.py install

verificacao do openface

cd openface

models/get-models.sh

data/download-lfw-subset.sh

run-test.sh


bug se ocorrer essa mensagem:
Failure: ImportError (/usr/local/lib/python2.7/dist-packages/dlib.so: undefined symbol: _gfortran_compare_string) ... ERROR
então e necessario preceder a execução:
 LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libgfortran.so.3.0.0 


<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Extra web 
apt-get install python-tox
git clone https://github.com/crossbario/txaio.git ~/crossbario --recursive
python2 setup.py install
Usar pip para instalar twisted e autobahn ao invés de usar 
pip install autobahn
pip install autobahn[twisted]
pip install autobahn[asyncio]
pip install twisted


<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
outras anotacoes 
Dos requirements do proprio openface para ubuntu

numpy ok -> python-numpy
scipy ok -> python-scipy

apt-get install git
 apt-get install python-numpy python-scipy python-pandas python-pandas-lib python-scikits-learn python-nose2
 apt-get install libcv2.4 libcv-dev python-opencv

do dlib-master.zip
apt-get install cmake cmake-qt-gui
 apt-get install libboost-python-dev libluajit-5.1-dev
 python setup.py install --yes USE_AVX_INSTRUCTIONS

para instalar o th segue os seguintes passos

segue os passos de http://torch.ch/docs/getting-started.html#_
ao inves de usar ./install.sh usa o cmake-gui configura e gera

 
instala com make install

apt-get install libreadline-dev
luarocks install trepl

luarocks install luaffi
luarocks install nn

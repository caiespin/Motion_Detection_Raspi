# OpenCV

sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev


# install opencv using pip (I did it for python3, python2 didnt worked)
https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/
https://stackoverflow.com/questions/31133050/virtualenv-command-not-found
https://stackoverflow.com/questions/60252119/error-environment-users-myuser-virtualenvs-iron-does-not-contain-activation-s
https://raspberrypi.stackexchange.com/questions/108740/error-environment-home-pi-virtualenvs-cv-does-not-contain-an-activate-scrip

sudo pip3 install virtualenv virtualenvwrapper
nano ~/.bashrc

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin

mkvirtualenv cvp3 -p python3

pip install -v opencv-contrib-python==4.1.0.25
pip install imutils
pip install "picamera[array]"
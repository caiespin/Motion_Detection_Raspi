#!/bin/bash -i
# Install OpenCV using pip
echo "Installing dependencies..."
packages=("libhdf5-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 libatlas-base-dev libjasper-dev")
for pkg in ${packages[@]}; do

    is_pkg_installed=$(dpkg-query -W --showformat='${Status}\n' ${pkg} | grep "install ok installed")

    if [ "${is_pkg_installed}" == "install ok installed" ]; then
        echo ${pkg} is installed.
    else
        sudo apt-get install ${pkg}
    fi
done
echo "Installing virtualenv and virtualenvwrapper..."
pip_packages=("virtualenv virtualenvwrapper")
for pkg in ${pip_packages[@]}; do
    if ! [[ -n "$(pip3 list | grep ${pkg})" ]];then
	echo ${pkg} is not installed, installing from pip3...
    	sudo pip3 install ${pkg}
    else
	echo ${pkg} is installed.
    fi
done
#sudo pip3 install virtualenv virtualenvwrapper
echo "Configuring virtual environment..."
echo "Changing to home directory..."
cd ~
if grep -Fxq "# virtualenv and virtualenvwrapper" .bashrc
then
    echo "Found bashrc setup"
else
    echo "Adding bashrc setup"
    echo "" >> .bashrc
    echo "# virtualenv and virtualenvwrapper" >> .bashrc
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> .bashrc
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> .bashrc
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> .bashrc
    echo "export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin" >> .bashrc
fi
echo "Creating virtual environment to install openCV"
source ~/.bashrc
mkvirtualenv cvp3 -p python3
workon cvp3
echo "Installing pip dependencies..."
pip_packages=("imutils "picamera[array]"")
for pkg in ${pip_packages[@]}; do
    if ! [[ -n "$(pip list | grep ${pkg})" ]];then
	echo ${pkg} is not installed, installing from pip...
    	pip install ${pkg}
    else
	echo ${pkg} is installed.
    fi
done
read -p "Do you want to install openCV (This will take a long time)? [Y/n]: " answer
answer=${answer:Y}
[[ $answer =~ [Yy] ]] && pip install -v opencv-contrib-python==4.1.0.25

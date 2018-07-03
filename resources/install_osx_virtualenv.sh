#!/bin/bash

echo Running install_osx_virtalenv.sh

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then

    brew update;

    if [[ "$OSXENV" == "2.7" ]]; then
        brew install python;
        virtualenv venv -p python;
        source venv/bin/activate;
    else
        brew install pyenv;
        brew upgrade pyenv;
        if [[ "$OSXENV" == "3.5" ]]; then
            pyenv install 3.5.0
            pyenv virtualenv 3.5.0 venv
            pyenv activate venv
#            virtualenv venv --python=python3.5;
#            source venv/bin/activate;
        else
            pyenv install 3.6.0
            virtualenv venv --python=python3.6;
            source venv/bin/activate;
        fi
    fi
fi

which python;
pip install lxml;

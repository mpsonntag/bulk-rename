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
        brew install pyenv-virtualenv;
        eval "$(pyenv init -)";
        eval "$(pyenv virtualenv-init -)";
        if [[ "$OSXENV" == "3.5" ]]; then
            pyenv install 3.5.0
            pyenv virtualenv 3.5.0 venv
        else
            pyenv install 3.6.0
            pyenv virtualenv 3.6.0 venv
        fi
        pyenv activate venv
    fi
fi

which python;
python --version;
pip install lxml;

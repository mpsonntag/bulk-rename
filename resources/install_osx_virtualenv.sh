#!/bin/bash

echo Running install_osx_virtalenv.sh

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew update;
    brew install pyenv;
    brew upgrade pyenv;
    brew install pyenv-virtualenv;
    eval "$(pyenv init -)";
    eval "$(pyenv virtualenv-init -)";
    pyenv install $OSXENV;
    pyenv virtualenv $OSXENV venv;
    pyenv activate venv;
    which python;
    python --version;
    which pip
    pip install requests;
    pip install lxml;
fi

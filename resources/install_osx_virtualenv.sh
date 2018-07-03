#!/bin/bash

echo Running install_osx_virtalenv.sh

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then

    brew update;
    brew install pyenv;
    brew upgrade pyenv;
    brew install pyenv-virtualenv;
    eval "$(pyenv init -)";
    eval "$(pyenv virtualenv-init -)";

    if [[ "$OSXENV" == "2.7" ]]; then
        pyenv install 2.7.14
        pyenv virtualenv 2.7.14 venv
    else
        if [[ "$OSXENV" == "3.5" ]]; then
            pyenv install 3.5.0
            pyenv virtualenv 3.5.0 venv
        else
            pyenv install 3.6.0
            pyenv virtualenv 3.6.0 venv
        fi
    fi
    pyenv activate venv

    which python;
    python --version;
    which pip
    pip install requests;
    pip install lxml;
fi

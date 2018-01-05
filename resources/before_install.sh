#!/bin/bash

echo Running before_install.sh

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then brew update; fi
if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    if [[ "$OSXENV" == "2.7" ]]; then
        brew install python;
        virtualenv venv -p python;
        source venv/bin/activate;
    else
        brew install python3;
        virtualenv venv -p python3;
        source venv/bin/activate;
    fi
fi

which python

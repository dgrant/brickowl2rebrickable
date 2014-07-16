#!/bin/sh
nosetests --with-coverage --cover-inclusive --cover-html --exclude='.*integration.*'

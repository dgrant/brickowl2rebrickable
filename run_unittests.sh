#!/bin/sh
nosetests --with-coverage --cover-inclusive --exclude='.*integration.*'

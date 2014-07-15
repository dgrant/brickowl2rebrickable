#!/bin/sh
pep8 --max-line-length=120  *.py
pylint --disable=C0301 --reports=n *.py

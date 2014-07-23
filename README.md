[![Build Status](https://travis-ci.org/dgrant/brickowl2rebrickable.png)](https://travis-ci.org/dgrant/dbrickowl2rebrickable) [![Coverage Status](https://coveralls.io/repos/dgrant/brickowl2rebrickable/badge.png)](https://coveralls.io/r/dgrant/brickowl2rebrickable)

brickowl2rebrickable
====================

Convert BrickOwl.com orders into a Rebrickable CSV file.

    usage: brickowl2rebrickable.py [-h] API_KEY ORDER_NUM [ORDER_NUM ...]

combine_rebrickable_csv
=======================

Combine multiple Rebrickable CSV files into one:

    usage: combine_rebrickable_csv.py file1.csv file2.csv file3.csv
    
Combined file is created as "combined.csv". I can add a command-line option to change this.

Notes
=====

I went a little overboard on testing here as I was using this project as an opportunity to learn how to use the Python mock library.

Contributing
============

Issue reports, feature requests, and patch requests welcome!

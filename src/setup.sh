#!/bin/bash

#This file installs all dependencies automatically
# @Author: Cole Marino (cole1.marino@gmail.com)

python3 -m pip install --upgrade pip
echo "Updated pip!"

pip install pandas
echo "Installed Pandas"

pip install psycopg2-binary
echo "Installed psycopg2-binary"

pip install psycopg2
echo "Installed psycopg2"
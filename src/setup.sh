#!/bin/bash

#This file installs all dependencies automatically
# @Author: Cole Marino (cole1.marino@gmail.com)

py get-pip.py
echo "Installed pip!"

pip install psycopg2-binary
echo "Installed psycopg2-binary"
#!/bin/bash

./main.py $@ > temp.out

for last; do true; done

diff -bB temp.out $last.s
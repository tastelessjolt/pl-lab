#! /bin/bash

rm -rf 150050031-150050069/
cp -R src/ 150050031-150050069/ && 
cd 150050031-150050069/ && 
find . | grep -E "(__pycache__|temp|\.pyc$|/\.)" | xargs rm -rf &&
mv main.py Parser.py && 
cd .. && 
tar -zcvf 150050031-150050069.tar.gz 150050031-150050069/ &&
rm -rf 150050031-150050069/


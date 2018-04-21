
coverage erase

for i in {0..19};
do
echo t$i.c;
coverage run -a main.py temp/t$i.c;
done;

coverage report
coverage html

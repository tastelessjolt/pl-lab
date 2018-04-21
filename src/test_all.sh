for i in {0..19};
do 
echo t$i.c;
z=0;
one=1;
file1=temp/t$i.c.$1;
file2=testcases/asm/t$i.c.$1;
if [ "$2" -eq "$z" ]; then
    diff -bB <( tr -d ' \n\t' <$file1 ) <( tr -d ' \n\t' <$file2 )
else
    if [ "$2" -eq "$one" ]; then
        diff -bB $file1 $file2
    else
        sort $file1 > temp.out1
        sort $file2 > temp.out2
        diff -bBw <( tr -d ' \n\t' <temp.out1 ) <( tr -d ' \n\t' <temp.out2 )
    fi
fi    
read;  
done;

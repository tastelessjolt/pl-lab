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
        tr -d ' \t' <$file1 > temp.out1
        sort temp.out1 > temp.out2
        tr -d ' \t' <$file2 > temp.out3
        sort temp.out3 > temp.out4
        diff -bB <( tr -d ' \n\t' <temp.out2 ) <( tr -d ' \n\t' <temp.out4 )
    fi
fi    
read;  
done;

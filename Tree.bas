///.a
input "size 3-7";s
rem check for overflow
if s<3 goto a
if s>7 goto a
rem build the tree itself
for c=1 to s
    for e=0 to s-c
        print " ";
    next e
    for a=1 to (c-1)*2+1
    rem i write the star on top and the leaves
        if c=1 then print "+";
        if c<>1 then print "*";
    next a
    print " "
    next c
rem here i add the log
for c=1 to s
print " ";
next c
print "#"
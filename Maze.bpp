rem print chr$(205+int(rnd(1)*2));

rem the chance of a wall spawning 1/10
p=9
input "wall rate";p
print chr$(147);
for y=0 to 24
    for x=0 to 39
        a=int((rnd(1)*p))
        b=1
        if a<>0 then b=0
        poke 1024+x+40*y,77+int(rnd(1)*2)
        poke 55296+x+40*y,int(b*int(peek(53281)))
    next x
next y

for a=0 to 3000
next a
///FLAGS:-ur
///,emptychar=32
p%=0
print chr$(147)
///.input
add%=0
in%=peek(56320)


rem input handler
if in%=119 then add%=1:poke 1024+p%,///emptychar///
if in%=123 then add%=-1:poke 1024+p%,///emptychar///
if in%=125 then add%=40:poke 1024+p%,///emptychar///
if in%=126 then add%=-40:poke 1024+p%,///emptychar///

p%=p%+add%

if p%>999 then p%=p%-add%
if p%<0 then p%=p%-add%

rem exiting the program
if in%=111 then goto end
poke 1024+p%,0
goto input

///.end
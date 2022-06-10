///,ball=81
///,null=32
///,lpad=118
///,rpad=117
///,lpadx=2
///,rpadx=37
///,rxbounce=36
///,lxbounce=3
///,scr=1024
///,sy=25
///,winpoints=5

///{cls
print chr$(147)
}///


rem clear the screen
///cls///


rem points
pl%=0
pr%=0

rem l is left r is right
ly%=11
ry%=12

rem ball position
bx%=20
by%=12

rem speed multipliers
xm%=1
ym%=1

rem updating the ball position

///.inputmanager

if peek(56321)=255 then goto p2check
if peek(1026)=///lpad/// then goto p1d
if peek(56321)=254 then ly%=ly%-1:goto p2check
///.p1d
if peek(1986)=///lpad/// then goto p2check
if peek(56321)=253 then ly%=ly%+1

///.p2check
if peek(56320)=127 then goto posupdater
if peek(1061)=///rpad/// then goto p2d
if peek(56320)=126 then ry%=ry%-1:goto posupdater
///.p2d
if peek(2021)=///rpad/// then goto posupdater
if peek(56320)=125 then ry%=ry%+1




///.posupdater
if by%=0 or by%=24 then ym%=-ym%
if peek(///scr///+bx%+xm%+((by%+ym%)*40))<>///null/// then xm%=-xm%

bx%=bx%+xm%
by%=by%+ym%





///.render
poke ///scr///+(bx%-xm%)+((by%-ym%)*40),///null///
poke ///scr///+bx%+(by%*40),///ball///

if bx%=0 then pr%=pr%+1:goto wl
if bx%=39 then pl%=pl%+1:goto wr


rem poking the pads
ls%=///scr///+///lpadx///+(ly%*40)
rs%=///scr///+///rpadx///+(ry%*40)

poke ls%,///lpad///
poke ls%+40,///lpad///
poke ls%+80,///lpad///
poke ls%-40,///lpad///
poke ls%-80,///lpad///

poke rs%,///rpad///
poke rs%+40,///rpad///
poke rs%+80,///rpad///
poke rs%-40,///rpad///
poke rs%-80,///rpad///


rem clearing the sides
poke rs%-120,///null///
poke rs%+120,///null///
poke ls%-120,///null///
poke ls%+120,///null///

poke 1197,48+pl%
poke 1210,48+pr%



goto inputmanager


///.wl
xm%=-1
goto resetball

///.wr
xm%=1
goto resetball

///.resetball
poke ///scr///+bx%+(by%*40),///null///
if pl%=///winpoints/// then goto lwin
if pr%=///winpoints/// then goto rwin

bx%=20
by%=rnd(1)*24
ym%=1


goto inputmanager

///.lwin
///cls///
print "left player wins"
goto end

///.rwin
///cls///
print "right player wins"
goto end

///.end
print " "
print "made by ago061 10/06/2022"
import math,glob,sys,os
from PIL import Image,ImageDraw,ImageFont
from PIL import Image,ImageDraw,ImageFont
W,H,FPS,S=1280,720,20,2
BG=(243,235,224);K=(45,36,32);RED=(205,80,50);NIGHT=(22,28,52)
FA=sorted(glob.glob('/usr/share/fonts/**/NotoSansArabic-Bold.ttf',recursive=True)) or sorted(glob.glob('/usr/share/fonts/**/NotoSansArabic*.ttf',recursive=True))
FC={}
def F(sz):
    if sz not in FC:FC[sz]=ImageFont.truetype(FA[0],sz,layout_engine=ImageFont.Layout.RAQM)
    return FC[sz]
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3
def clamp(x):return max(0,min(1,x))
# drawing helpers (coords logical, scaled by S)
def ln(d,p,q,w=5,c=K):d.line([(p[0]*S,p[1]*S),(q[0]*S,q[1]*S)],fill=c,width=int(w*S))
def circ(d,x,y,r,fill=None,outline=None,w=3):d.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=fill,outline=outline,width=int(w*S))
def rect(d,x0,y0,x1,y1,fill=None,outline=None,w=3,r=0):d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,fill=fill,outline=outline,width=int(w*S))
def seg(p,a,l):return (p[0]+l*math.cos(math.radians(a)),p[1]+l*math.sin(math.radians(a)))
def txt(d,x,y,s,sz,fill=K,anchor='mm'):d.text((x*S,y*S),s,font=F(sz*S),fill=fill,anchor=anchor)
def man(d,x,base,t,walk=0,armL=(100,100),armR=(80,80),tilt=0,lean=0,bob=1,col=K,scarf=True,head=BG):
    b=math.sin(t*2.5)*2*bob
    hip=(x+lean*0.3,base-80+b);neck=(x+lean,base-165+b)
    sw=math.sin(t*7)*28*walk
    for ph in (1,-1):ln(d,hip,(hip[0]+ph*(sw+8),base),5,col)
    ln(d,hip,neck,5,col)
    sh=(neck[0],neck[1]+22);hands=[]
    for ang in (armL,armR):
        e=seg(sh,ang[0],38);h=seg(e,ang[1],36);ln(d,sh,e,5,col);ln(d,e,h,5,col);hands.append(h)
    hx,hy=neck[0]+math.sin(math.radians(tilt))*10,neck[1]-27
    circ(d,hx,hy,27,fill=head,outline=col,w=4)
    ex=hx+9+tilt*0.2;ey=hy+3+tilt*0.15
    circ(d,ex,ey,3,fill=col);circ(d,ex+13,ey,3,fill=col)
    if scarf:d.polygon([((neck[0]-3)*S,(neck[1]+2)*S),((neck[0]+3)*S,(neck[1]+2)*S),((neck[0]+9)*S,(neck[1]+34)*S),((neck[0])*S,(neck[1]+46)*S),((neck[0]-9)*S,(neck[1]+34)*S)],fill=RED)
    return hands,(hx,hy)
def moon(d,x,y,r,a=1.0,bgc=NIGHT,phase=0):
    c=tuple(int(bgc[i]+(240-bgc[i]+ (0 if i<2 else -20))*a) if i<2 else int(bgc[i]+(215-bgc[i])*a) for i in range(3))
    circ(d,x,y,r,fill=c)
    cr=tuple(int(c[i]*0.9) for i in range(3))
    for dx,dy,rr in ((-.3,-.2,.22),(.25,.15,.18),(-.1,.4,.12),(.4,-.35,.1)):circ(d,x+dx*r,y+dy*r,rr*r,fill=cr)
def stars(d,t,n=40,a=1.0,seed=3):
    import random;rnd=random.Random(seed)
    for i in range(n):
        x=rnd.randint(20,1260);y=rnd.randint(20,400);tw_=0.5+0.5*math.sin(t*2+i);k=int(255*a*(0.5+0.5*tw_))
        circ(d,x,y,2,fill=(k,k,min(255,k+10)))
def ground(d,col,y=560):d.rectangle([0,y*S,W*S,H*S],fill=col)
def bubble(d,x,y,s,col,sz=28):
    w=d.textlength(s,font=F(sz*S))/S+30;rect(d,x-w/2,y-24,x+w/2,y+24,fill=col,r=22);txt(d,x,y,s,sz,'white')
def card(d,x,y,w,h,title,sub=None,col=(236,226,212)):
    rect(d,x,y,x+w,y+h,fill=col,outline=(215,203,188),w=2,r=14);txt(d,x+w/2,y+h/2-(10 if sub else 0),title,26)
    if sub:txt(d,x+w/2,y+h/2+22,sub,19,(110,96,85))
def earth(d,x,y,r,tilt=23,spin=0):
    circ(d,x,y,r,fill=(90,150,210),outline=K,w=3)
    for k in range(3):
        a=spin+k*2.1;lx=x+math.cos(a)*r*0.5;ly=y+math.sin(a*1.3)*r*0.4
        circ(d,lx,ly,r*0.22,fill=(110,170,100))
    ln(d,seg((x,y),-90+tilt,r*1.35),seg((x,y),90+tilt,r*1.35),4,RED)
def sun(d,x,y,r):
    for i in range(12):
        a=i*30;ln(d,seg((x,y),a,r+6),seg((x,y),a,r+20),4,(240,170,40))
    circ(d,x,y,r,fill=(250,205,70))

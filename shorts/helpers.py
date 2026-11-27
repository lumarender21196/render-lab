import math
from PIL import Image,ImageDraw,ImageFont
BG=(243,235,224);INK=(45,36,32);RED=(205,80,50)
S=2
K=(45,36,32)
FA=[]
def ease(x):x=max(0,min(1,x));return 1-(1-x)**3
def back(x):
    x=max(0,min(1,x));c=1.70158;return 1+(c+1)*(x-1)**3+c*(x-1)**2
CACHE={}
def tw(name,sz):
    k=(name,sz)
    if k not in CACHE:CACHE[k]=Image.open(f'ic/{name}.png').convert('RGBA').resize((sz,sz))
    return CACHE[k]
def ln(d,p,q,w=5,c=K):d.line([(p[0]*S,p[1]*S),(q[0]*S,q[1]*S)],fill=c,width=int(w*S))
def circ(d,x,y,r,fill=None,outline=None,w=3):d.ellipse([(x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S],fill=fill,outline=outline,width=int(w*S))
def rect(d,x0,y0,x1,y1,fill=None,outline=None,w=3,r=0):
    if r:d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,fill=fill,outline=outline,width=int(w*S))
    else:d.rectangle([x0*S,y0*S,x1*S,y1*S],fill=fill,outline=outline,width=int(w*S))
def seg(p,a,l):return (p[0]+l*math.cos(math.radians(a)),p[1]+l*math.sin(math.radians(a)))
def man(d,x,base,t,walk=0,armL=(100,100),armR=(80,80),tilt=0,lean=0,bob=1):
    """angles in degrees, 0=right, 90=down. arms (upper,fore)"""
    b=math.sin(t*2.5)*2*bob
    hip=(x+lean*0.3,base-80+b);neck=(x+lean,base-165+b)
    d.ellipse([(x-26)*S,(base-2)*S,(x+26)*S,(base+8)*S],fill=(222,208,190))
    sw=math.sin(t*7)*28*walk
    for ph in (1,-1):
        ln(d,hip,(hip[0]+ph*(sw+8),base))
    ln(d,hip,neck)
    sh=(neck[0],neck[1]+22)
    for ang in (armL,armR):
        e=seg(sh,ang[0],38);h=seg(e,ang[1],36);ln(d,sh,e);ln(d,e,h)
        d._h=getattr(d,'_h',{});d._h[id(ang)]=h
    hx,hy=neck[0]+math.sin(math.radians(tilt))*10,neck[1]-27
    circ(d,hx,hy-0,27,fill=BG,outline=K,w=4)
    ex=hx+9+tilt*0.2;ey=hy+3+tilt*0.15
    circ(d,ex,ey,3,fill=K);circ(d,ex+13,ey,3,fill=K)
    d.polygon([((neck[0]-3)*S,(neck[1]+2)*S),((neck[0]+3)*S,(neck[1]+2)*S),((neck[0]+9)*S,(neck[1]+34)*S),((neck[0])*S,(neck[1]+46)*S),((neck[0]-9)*S,(neck[1]+34)*S)],fill=RED)
    return sh,[seg(seg(sh,a[0],38),a[1],36) for a in (armL,armR)]
K=(45,36,32)

def pap(d,x,y,ang,w=60,h=78,col=(252,250,244),star=False):
    ca,sa=math.cos(ang),math.sin(ang);pts=[]
    for dx,dy in((-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)):pts.append(((x+dx*ca-dy*sa)*S,(y+dx*sa+dy*ca)*S))
    d.polygon(pts,fill=col,outline=K)
    for i in(-1,0,1):
        p=(x+(-18)*ca-(i*16)*sa,y+(-18)*sa+(i*16)*ca);q=(x+18*ca-(i*16)*sa,y+18*sa+(i*16)*ca);d.line([(p[0]*S,p[1]*S),(q[0]*S,q[1]*S)],fill=(170,160,150),width=2*S)
    if star:circ(d,x+w/2,y-h/2,16,fill=RED)

import os as _os
_BGC={}
def getbg(scene,col,W_,H_):
    f=_os.environ.get('BG_'+scene,scene+'_xl1')
    p=f'bgs/{f}.jpg'
    if _os.path.exists(p):
        if p not in _BGC:
            b=Image.open(p).convert('RGB');tw_,th_=W_*S,H_*S
            sc=max(tw_/b.width,th_/b.height);b=b.resize((int(b.width*sc)+1,int(b.height*sc)+1),Image.LANCZOS)
            _BGC[p]=b.crop((0,0,tw_,th_))
        return _BGC[p].copy(),True
    return Image.new('RGB',(W_*S,H_*S),col),False

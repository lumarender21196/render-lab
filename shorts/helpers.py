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
SKIN=(247,214,180);SHIRT=(70,120,200);PANTS=(55,60,95);HAIR=(60,40,30);SHOE=(40,34,34)
def ln2(d,p,q,w,c,o=None):
    if o:d.line([(p[0]*S,p[1]*S),(q[0]*S,q[1]*S)],fill=o,width=int((w+3)*S));circ(d,p[0],p[1],(w+3)/2,fill=o);circ(d,q[0],q[1],(w+3)/2,fill=o)
    d.line([(p[0]*S,p[1]*S),(q[0]*S,q[1]*S)],fill=c,width=int(w*S));circ(d,p[0],p[1],w/2,fill=c);circ(d,q[0],q[1],w/2,fill=c)
def man(d,x,base,t,walk=0,armL=(100,100),armR=(80,80),tilt=0,lean=0,bob=1):
    """angles in degrees, 0=right, 90=down. arms (upper,fore). richer: shirt, pants, shoes, hair, face"""
    b=math.sin(t*2.5)*2*bob
    hip=(x+lean*0.3,base-80+b);neck=(x+lean,base-165+b)
    d.ellipse([(x-34)*S,(base-4)*S,(x+34)*S,(base+10)*S],fill=(0,0,0,0) if False else (205,190,172))
    sw=math.sin(t*7)*28*walk
    for ph in (1,-1):
        f=(hip[0]+ph*(sw+8),base-4);kn=((hip[0]+f[0])/2+ph*3,(hip[1]+f[1])/2)
        ln2(d,hip,kn,9,PANTS,K);ln2(d,kn,f,9,PANTS,K)
        d.ellipse([(f[0]-9)*S,(f[1]-3)*S,(f[0]+17)*S,(f[1]+9)*S],fill=SHOE,outline=K,width=2*S)
    sh=(neck[0],neck[1]+22)
    # torso: filled shirt
    tw_=15
    d.polygon([((sh[0]-tw_)*S,(sh[1]-2)*S),((sh[0]+tw_)*S,(sh[1]-2)*S),((hip[0]+11)*S,(hip[1]+6)*S),((hip[0]-11)*S,(hip[1]+6)*S)],fill=SHIRT,outline=K)
    d.line([((hip[0]-11)*S,(hip[1]+4)*S),((hip[0]+11)*S,(hip[1]+4)*S)],fill=(40,40,60),width=3*S)
    for ang in (armL,armR):
        e=seg(sh,ang[0],38);hd=seg(e,ang[1],36)
        ln2(d,(sh[0],sh[1]+2),e,9,SHIRT,K);ln2(d,e,hd,8,SKIN,K);circ(d,hd[0],hd[1],6,fill=SKIN,outline=K,w=2)
    hx,hy=neck[0]+math.sin(math.radians(tilt))*10,neck[1]-27
    ln2(d,neck,(hx,hy+20),9,SKIN,K)
    # hair back, head, hair top
    circ(d,hx,hy,29,fill=SKIN,outline=K,w=3)
    d.pieslice([(hx-29)*S,(hy-29)*S,(hx+29)*S,(hy+29)*S],185,355,fill=HAIR,outline=K,width=2*S)
    d.ellipse([(hx-29)*S,(hy-24)*S,(hx-16)*S,(hy+4)*S],fill=HAIR)
    ex=hx+9+tilt*0.2;ey=hy+3+tilt*0.15
    for k in (0,13):
        circ(d,ex+k,ey,5.5,fill=(255,255,255),outline=K,w=1.5);circ(d,ex+k+1.5,ey+0.5,3,fill=K)
        ln(d,(ex+k-5,ey-9),(ex+k+5,ey-10-(1 if k else 0)),2.5,K)
    circ(d,ex-4,ey+10,4.5,fill=(245,160,150))
    d.arc([(ex-2)*S,(ey+6)*S,(ex+16)*S,(ey+20)*S],20,160,fill=K,width=int(2.5*S))
    d.polygon([((neck[0]-3)*S,(neck[1]+4)*S),((neck[0]+3)*S,(neck[1]+4)*S),((neck[0]+8)*S,(neck[1]+28)*S),((neck[0])*S,(neck[1]+42)*S),((neck[0]-8)*S,(neck[1]+28)*S)],fill=RED,outline=K)
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

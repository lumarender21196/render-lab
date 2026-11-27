import sys,os,math
from helpers import *
from whatif import txt,card,CARD
W,H=450,800;FPS=24;T=20.0;NF=int(T*FPS)
GY=640;MX=150
def Z(t):
    if t<5.0:return 1.0
    if t<6.8:return 1+11*ease((t-5.0)/1.8)
    return 12.0
def blade(d,x,y,h,w,col):
    d.polygon([((x-w)*S,y*S),((x+w)*S,y*S),((x+w*0.3+h*0.08)*S,(y-h)*S)],fill=col,outline=INK)
def ant(d,x,y,s,t,face=-1):
    c=(70,45,40)
    for k in range(3):
        ph=math.sin(t*9+k*2.1)*10*s
        for sd in(-1,1):ln(d,(x+(k-1)*26*s,y-22*s),(x+(k-1)*26*s+sd*14*s+ph*0.4,y+2*s),4*s**0.5,INK)
    for dx,r in((-34,20),(0,16),(32,13)):circ(d,x+dx*s*face*-1*-1,y-34*s,r*s,fill=c,outline=INK,w=3)
    circ(d,x+face*44*s,y-40*s,3*s,fill=(255,255,255))
    ln(d,(x+face*44*s,y-52*s),(x+face*60*s,y-70*s+math.sin(t*12)*4),3,INK)
def foot(d,x,y,s):
    d.polygon([((x-80*s)*S,(y-300*s)*S),((x+40*s)*S,(y-300*s)*S),((x+60*s)*S,(y-60*s)*S),((x+150*s)*S,(y-20*s)*S),((x+160*s)*S,y*S),((x-90*s)*S,y*S)],fill=(70,80,120),outline=INK)
    rect(d,x-90*s,y-14*s,x+160*s,y+8*s,fill=(40,36,40))
def frame(i):
    t=i/FPS;z=Z(t)
    im,HB=getbg('meadow',(160,212,242),W,H);d=ImageDraw.Draw(im)
    wy=lambda y:GY+(y-GY)*z
    wx=lambda x:MX+(x-MX)*z
    # ground
    rect(d,-10,wy(GY)+0,W+10,H+300,fill=(120,170,95));d.line([(0,wy(GY)*S),(W*S,wy(GY)*S)],fill=INK,width=3*S)
    # sun
    if not HB:circ(d,380,110,38,fill=(255,225,110))
    # grass blades scaled by zoom
    for k in range(40):
        gx=(wx(-200+k*34+(k*17)%23)-(max(0,min(t,15)-10)*70 if t>=10 else 0))%(W+260)-60;h=(28+(k*37)%24)*z*0.9
        if -60<gx<W+60:blade(d,gx,wy(GY)+6,h,6*z*0.8,(70+(k*13)%40,150+(k*7)%30,80))
    # flowers early
    if z<3:
        for fx in(300,380):circ(d,wx(fx),wy(GY)-30*z,8*z,fill=(240,120,150),outline=INK,w=2)
    # man
    s=1.0
    if t<5:aL,aR=(100,95),(70,80)
    elif t<6.8:aL,aR=(-60,-40),(-120,-90)
    elif t<10:aL,aR=(160,150),(70,80)
    else:aL,aR=(100,95),(80,80)
    mw=wx(MX)
    wk=0.5 if 10<=t<15 else 0
    xo=0
    # draw man at constant pixel size but base at world ground
    layer=Image.new('RGBA',(W*S,H*S),(0,0,0,0));ld=ImageDraw.Draw(layer)
    msc=1.0 if z<1.5 else 0.5
    man(ld,MX+xo,wy(GY)-4*z*0,t,walk=wk,armL=aL,armR=aR,tilt=0,bob=1)
    if z>=1.5:
        # shrink layer around man base
        sc=max(0.28,1/ (1+ (z-1.5)*0.35))
    else:sc=1.0
    if z>1.0 and z<12:
        sc=1.0/(1+(z-1)*0.18)
    elif z>=12:sc=0.32
    bw,bh=layer.size
    ml=layer.resize((int(bw*sc),int(bh*sc)),Image.LANCZOS)
    px=int((MX+xo)*S-(MX+xo)*S*sc);py=int(wy(GY)*S-wy(GY)*S*sc)
    # ant
    if t>=6.8:
        ax=max(520-(t-6.8)*110,MX+150)
        ant(d,ax,wy(GY)-6,1.5,t)
    im.paste(ml,(px,py),ml)
    # raindrop splash 12-13.2
    if 12.2<=t<13.4:
        u=(t-12.2)/1.2;dx=MX+xo+60;dy=-40+u*(GY-4+40)
        d.ellipse([(dx-14)*S,(dy-22)*S,(dx+14)*S,(dy+10)*S],fill=(100,170,235),outline=INK,width=2*S)
        if u>0.95:circ(d,dx,GY-6,50,fill=(150,200,240),outline=INK,w=2)
    if 13.4<=t<14.6:circ(d,MX+xo+60,GY-6,50*(1+(t-13.4)),fill=(150,200,240),outline=INK,w=2)
    # foot shadow and foot 15-18
    if 15.0<=t<18.0:
        u=(t-15.0)/3.0;sh=Image.new('RGBA',(W*S,H*S),(0,0,0,0));sd=ImageDraw.Draw(sh)
        r=60+u*220;sd.ellipse([(MX+xo+60-r*1.6)*S,(GY-20-r*0.25)*S,(MX+xo+60+r*1.6)*S,(GY+30+r*0.2)*S],fill=(0,0,0,int(40+u*90)));im.paste(sh,(0,0),sh)
        fy=-200+ease(u)*(GY-4+200);foot(d,MX+xo+20,fy,1.5)
    ui=Image.new('RGBA',(W*S,H*S),(0,0,0,0));u2=ImageDraw.Draw(ui)
    if t<3.6:
        card(u2,28,70,422,320);txt(u2,225,118,'WHAT IF YOU',34);txt(u2,225,168,'SHRANK TO',34);txt(u2,225,218,'ANT SIZE?',48,RED)
        if not os.environ.get('NOAR'):txt(u2,225,282,'ماذا لو صغرت لحجم نملة؟',28,INK,True)
    else:
        a=ease((t-3.6)/0.4);y=28+(1-a)*30
        rect(u2,60,y,390,y+48,fill=CARD,outline=INK,w=3,r=20);txt(u2,225,y+24,'WHAT IF: ANT SIZE',17)
    if 5.0<=t<6.6:card(u2,60,420,390,520);txt(u2,225,455,'SHRINK',30);txt(u2,225,498,'RAY!',44,RED)
    if 8.0<=t<10.4:card(u2,40,690,410,770);txt(u2,225,718,"Meet the locals.",24);txt(u2,225,750,"Ant: 'Hi!'",24,RED)
    if 11.0<=t<12.2:card(u2,60,690,390,770);txt(u2,225,730,"Free ride.",30)
    if 12.2<=t<14.4:card(u2,60,690,390,770);txt(u2,225,718,"A raindrop is",24);txt(u2,225,750,"a water balloon.",24,RED)
    if 15.6<=t<18.0:card(u2,60,690,390,770);txt(u2,225,730,"Is that... a shoe?!",26,RED)
    if t>=18.4:card(u2,50,690,400,770);txt(u2,225,718,"Tiny life.",28);txt(u2,225,752,"Big adventure.",26,RED)
    if 5.0<=t<5.2:ui.paste(Image.new('RGBA',(W*S,H*S),(255,255,255,170)),(0,0))
    zc=1.25;cw=W*S/zc;ch=H*S/zc;cx=W*S/2;cy=H*S*0.66
    sk=0
    for ts,amp in((0,8),(5.0,5),(15.8,7)):
        if 0<=t-ts<0.4:sk=amp*(1-(t-ts)/0.4)*math.sin((t-ts)*60)
    bx=max(0,min(W*S-int(cw),int(cx-cw/2+sk*S)));by=max(0,min(H*S-int(ch),int(cy-ch/2)))
    out=im.crop((bx,by,bx+int(cw),by+int(ch))).resize((720,1280),Image.LANCZOS).convert('RGBA')
    out.alpha_composite(ui.resize((720,1280),Image.LANCZOS))
    return out.convert('RGB')
if __name__=='__main__':
    D='ant'+os.environ.get('SUF','');os.makedirs(D,exist_ok=True);a=int(sys.argv[1]);b=int(sys.argv[2])
    for i in range(a,min(b,NF)):
        p=f'{D}/{i:04d}.png'
        if not os.path.exists(p):frame(i).save(p)

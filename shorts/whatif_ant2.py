import sys,os,math,random
from helpers import *
import helpers as HH
from whatif import txt,card,CARD
W,H=450,800;FPS=24;T=20.0;NF=int(T*FPS);GY=640
SPR={}
def spr(name,h):
    """sprite keyed from white bg, scaled to world height h (px, before S)"""
    k=(name,int(h))
    if k in SPR:return SPR[k]
    if name not in SPR:
        if not os.path.exists(f'sp/{name}.jpg'):
            ph=Image.new('RGB',(512,512),(255,255,255));pd=ImageDraw.Draw(ph);pd.polygon([(40,200),(300,200),(470,380),(470,470),(40,470)],fill=(60,90,200),outline=(0,0,0));pd.rectangle([40,430,470,490],fill=(250,250,250),outline=(0,0,0));ph.save(f'sp/{name}.jpg')
        im=Image.open(f'sp/{name}.jpg').convert('RGB')
        m=im.copy()
        for pt in((0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1),(im.width//2,0),(im.width//2,im.height-1)):
            ImageDraw.floodfill(m,pt,(255,0,255),thresh=48)
        a=m.convert('RGB');import numpy as np
        ar=np.array(a);alpha=~((ar[:,:,0]>240)&(ar[:,:,1]<20)&(ar[:,:,2]>240))
        al=Image.fromarray((alpha*255).astype('uint8')).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
        if name.startswith('grass'):
            mn=np.array(im.convert('RGB')).min(axis=2).astype('float32');al=Image.fromarray((np.clip((255-mn-22)/50,0,1)*255).astype('uint8')).filter(ImageFilter.MaxFilter(3))
        if name.startswith('grass'):
            import numpy as np
            w_=al.width;ramp=np.minimum(1,np.minimum(np.arange(w_),w_-1-np.arange(w_))/(w_*0.22))[None,:]
            al=Image.fromarray((np.array(al)*ramp).astype('uint8'))
        r=im.convert('RGBA');r.putalpha(al);bb=al.getbbox();SPR[name]=r.crop(bb)
    b=SPR[name];s=h*S/b.height
    SPR[k]=b.resize((max(1,int(b.width*s)),max(1,int(h*S))),Image.LANCZOS)
    return SPR[k]
from PIL import ImageFilter
def put(im,sp,x,y,flip=False,rot=0,anchor='bm'):
    if flip:sp=sp.transpose(Image.FLIP_LEFT_RIGHT)
    if rot:sp=sp.rotate(rot,expand=True,resample=Image.BICUBIC)
    w,h=sp.size;px=int(x*S-w/2);py=int(y*S-h) if anchor=='bm' else int(y*S-h/2)
    im.paste(sp,(px,py),sp)
_BG=None
def bg(par):
    global _BG
    if _BG is None:
        b=Image.open('bgs/'+os.environ.get('BG_meadow','meadow_xl1')+'.jpg').convert('RGB')
        sc=H*S*1.0/b.height;_BG=b.resize((int(b.width*sc*1.45),int(H*S)),Image.LANCZOS)
    ox=int(max(0,min(_BG.width-W*S,par*S)))
    return _BG.crop((ox,0,ox+W*S,H*S))
def Z(t):
    if t<5.0:return 1.0
    if t<6.8:return 1+11*ease((t-5.0)/1.8)
    return 12.0
def scroll(t):
    if t<11.0:return 0
    return (min(t,17.2)-11.0)*70
def draw_man(im,x,base,sc,t,shadow=True,mood='smile',aL=(100,95),aR=(70,80),walk=0,tilt=0):
    HH.MOOD[0]=mood;HH.SHADOW[0]=shadow
    ly=Image.new('RGBA',(320*S,330*S),(0,0,0,0));ld=ImageDraw.Draw(ly)
    man(ld,160,300,t,walk=walk,armL=aL,armR=aR,tilt=tilt,bob=1)
    ly=ly.resize((int(320*S*sc),int(330*S*sc)),Image.LANCZOS)
    im.paste(ly,(int(x*S-160*S*sc),int(base*S-300*S*sc)),ly)
def ground(im,d,t,sc_):
    rect(d,-10,GY+4,W+10,H+400,fill=(112,168,86))
    r=random.Random(3)
    for k in range(120):
        gx=(r.uniform(0,W+80)-sc_*1.0)%(W+80)-40;gy=GY+10+r.uniform(0,1)**0.8*(H-GY+60)
        c=r.choice([(86,146,70),(132,190,100),(98,158,76)]);l=r.uniform(6,16)*(0.6+(gy-GY)/200)
        d.line([(gx*S,gy*S),((gx+r.uniform(-4,4))*S,(gy-l)*S)],fill=c,width=int(2.2*S))
    d.line([(0,(GY+4)*S),(W*S,(GY+4)*S)],fill=INK,width=3*S)
def frame(i):
    t=i/FPS;z=Z(t);sc_=scroll(t)
    wy=lambda y:GY+(y-GY)*z
    im=bg(sc_*0.12);d=ImageDraw.Draw(im)
    ground(im,d,t,sc_)
    # back grass sprites (scale with z)
    r=random.Random(11)
    gnames=['grass1','grass2','grass3']
    for k in range(9):
        gxw=r.uniform(-60,520);gh=(34+r.uniform(0,24))*z*0.8
        gx=MXW(gxw,z)-sc_*(0.7 if z>5 else 1)
        gx=(gx+300)%(W+700)-300
        if t<5 and gxw%2<1 and False:continue
        put(im,spr(gnames[k%3],gh),gx,wy(GY)+8)
    # actors
    MX=150
    if t<5:
        sc=1.0;mx=MX;mb=GY
    else:
        u=ease((t-5.0)/1.8);sc=1-0.45*u if t<6.8 else 0.55
        mx=MX;mb=GY
    # ant
    antH=120;antx=None
    if t>=6.8:
        if t<8.4:antx=560-(t-6.8)/1.6*(560-270)
        elif t<12.0:antx=270
        elif t<15:antx=270
        elif t<17.2:antx=270+(t-15)/2.2*125
        else:antx=395
        bobv=math.sin(t*16)*2.5 if (t<8.4 or 12<=t<17.2) else math.sin(t*5)*1.2
        walking=(t<8.4) or (12<=t<17.2)
        # ant moves left? faces left toward man
    # man pos/pose by phase
    mood='smile';aL=(100,95);aR=(70,80);walk=0;tilt=0
    if t<3.6:aR=(-70+math.sin(t*8)*18,-40);mood='smile'
    elif t<5:mood='worry'if t>4.4 else 'smile'
    elif t<6.8:mood='shock';aL=(-70,-50);aR=(-110,-80)
    elif t<8.4:mood='shock';aL=(-60,-40);aR=(-120,-90)
    elif t<10.4:mood='laugh';aR=(-60+math.sin(t*10)*15,-30)  # wave
    elif t<12.0:
        mood='laugh';aL=(-100,-80);aR=(-80,-60)
    elif t<15.0:mood='laugh' if t<12.2 or t>14.3 else 'shock';aL=(-80,-60);aR=(-100,-80)
    elif t<17.2:mood='shock';aL=(-70,-30);aR=(-30,-10)
    elif t<17.8:mood='shock';aL=(-100,-60);aR=(-90,-50)
    else:mood='laugh';aL=(-60,-30);aR=(-120,-100)
    # man x,base by phase (riding)
    if t<10.4:man_x=mx;man_b=mb
    elif t<12.0:
        u=ease((t-10.4)/1.0) if t<11.4 else 1.0
        tx=antx-8;ty=GY-antH*0.6
        man_x=mx+(tx-mx)*u;man_b=GY-(GY-ty)*u-math.sin(u*3.14)*90
    elif t<17.2:
        man_x=antx-8;man_b=GY-antH*0.6+bobv
    else:
        u=ease((t-17.2)/0.5);man_x=antx-8-u*100;man_b=GY-antH*0.6+(antH*0.6)*min(1,u*1.0)+0
    if t>=6.8:
        if t<17.2:
            put(im,spr('ant1',antH),antx,GY+4+(bobv if walking else 0))
        else:
            put(im,spr('ant1',antH),antx,GY+4)
    if t>=17.2 and False:pass
    dm=lambda:draw_man(im,man_x,man_b,sc,t,(t<10.8 or t>17.4),mood,aL,aR,walk=0.4 if (t<10.4 and 8.4<t<9) else 0,tilt=tilt)
    if t<17.2:dm()
    # raindrop
    if 12.2<=t<13.4:
        u=(t-12.2)/1.2;dx=antx+95;dy=-60+u*(GY+2+60)
        put(im,spr('drop1',70),dx,dy+35)
    if 13.4<=t<14.4:
        u=(t-13.4)/1.0;rr=40+u*70
        d2=ImageDraw.Draw(im);d2.ellipse([((antx+95-rr)*S),(GY-rr*0.22)*S,(antx+95+rr)*S,(GY+rr*0.18)*S],outline=(120,180,240),width=3*S)
    # shoe
    if 15.0<=t<17.4:
        u=min(1,(t-15.0)/2.2);sx=antx-190 if t<17.2 else antx-190
        fy=-260+ease(u)*(GY+4+260)
        shx=190
        # shadow on ground first
        sh=Image.new('RGBA',(W*S,H*S),(0,0,0,0));sd=ImageDraw.Draw(sh);rr=40+u*230
        sd.ellipse([(shx-rr*1.2)*S,(GY-rr*0.12)*S,(shx+rr*1.2)*S,(GY+rr*0.22)*S],fill=(0,0,0,int(60+u*100)));im.paste(sh,(0,0),sh)
        put(im,spr('shoe2',210),shx,fy,flip=True)
    if 17.2<=t<18.4:
        u=(t-17.2)/1.2;shx=190
        put(im,spr('shoe2',210),shx,GY+4,flip=True)
        dd=ImageDraw.Draw(im)
        for k in range(9):
            a=k*0.7;rr=20+u*110;cx_=shx+math.cos(a)*rr*1.3;cy_=GY-10-abs(math.sin(a))*rr*0.5
            dd.ellipse([(cx_-18*(1-u*0.5))*S,(cy_-14*(1-u*0.5))*S,(cx_+18*(1-u*0.5))*S,(cy_+14*(1-u*0.5))*S],fill=(214,200,170))
    elif t>=18.4:
        put(im,spr('shoe2',210),190,GY+4,flip=True)
    if t>=17.2:dm()
    # front tufts
    r2=random.Random(21)
    for k in range(5):
        fx=(r2.uniform(0,W+300)-sc_*1.7)%(W+500)-200;put(im,spr(gnames[k%3],(150 if z>5 else 46)*(1.0)),fx,GY+70+r2.uniform(0,80))
    ui=Image.new('RGBA',(W*S,H*S),(0,0,0,0));u2=ImageDraw.Draw(ui)
    if t<3.6:
        card(u2,28,70,422,320);txt(u2,225,118,'WHAT IF YOU',34);txt(u2,225,168,'SHRANK TO',34);txt(u2,225,218,'ANT SIZE?',48,RED)
        if not os.environ.get('NOAR'):txt(u2,225,282,'ماذا لو صغرت لحجم نملة؟',28,INK,True)
    else:
        a=ease((t-3.6)/0.4);y=28+(1-a)*30
        rect(u2,60,y,390,y+48,fill=CARD,outline=INK,w=3,r=20);txt(u2,225,y+24,'WHAT IF: ANT SIZE',17)
    if 5.0<=t<6.6:card(u2,60,420,390,520);txt(u2,225,455,'SHRINK',30);txt(u2,225,498,'RAY!',44,RED)
    if 8.0<=t<10.4:card(u2,40,690,410,770);txt(u2,225,718,"Meet the locals.",24);txt(u2,225,750,"Ant: 'Hi!'",24,RED)
    if 10.6<=t<12.2:card(u2,60,690,390,770);txt(u2,225,730,"Free ride.",30)
    if 12.2<=t<14.4:card(u2,60,690,390,770);txt(u2,225,718,"A raindrop is",24);txt(u2,225,750,"a water balloon.",24,RED)
    if 15.4<=t<17.2:card(u2,60,690,390,770);txt(u2,225,730,"Is that... a shoe?!",26,RED)
    if 17.4<=t<18.4:card(u2,60,690,390,770);txt(u2,225,730,"RUN!!",34,RED)
    if t>=18.6:card(u2,40,680,410,780);txt(u2,225,712,"Tiny life. Big adventure.",24);txt(u2,225,750,"Next: What if you grew GIANT?",19,RED)
    if 5.0<=t<5.2:ui.paste(Image.new('RGBA',(W*S,H*S),(255,255,255,170)),(0,0))
    # camera
    fx_=(man_x+(antx if antx else man_x))/2 if t>=6.8 else MX+60
    if t<5:zc=1.25;cx=W*S/2;cy=H*S*0.66
    else:
        k=ease(min(1,(t-5)/2.0));zc=1.25+0.65*k;fxs=man_x*0.5+(antx if antx else man_x)*0.5 if t>=6.8 else 225
        cx=(225+(fxs-225)*0.8*k)*S;cy=(H*0.66+(0.705-0.66)*H*k)*S
        if t>=17.4:zc=1.7
    sk=0
    for ts,amp in((0,8),(5.0,5),(17.2,16)):
        if 0<=t-ts<0.5:sk=amp*(1-(t-ts)/0.5)*math.sin((t-ts)*60)
    cw=W*S/zc;ch=H*S/zc
    bx=max(0,min(W*S-int(cw),int(cx-cw/2+sk*S)));by=max(0,min(H*S-int(ch),int(cy-ch/2+sk*0.4*S)))
    out=im.crop((bx,by,bx+int(cw),by+int(ch))).resize((720,1280),Image.LANCZOS).convert('RGBA')
    out.alpha_composite(ui.resize((720,1280),Image.LANCZOS))
    return out.convert('RGB')
def MXW(x,z):return 150+(x-150)*z
if __name__=='__main__':
    D='ant2'+os.environ.get('SUF','');os.makedirs(D,exist_ok=True);a=int(sys.argv[1]);b=int(sys.argv[2])
    for i in range(a,min(b,NF)):
        p=f'{D}/{i:04d}.png'
        if not os.path.exists(p):frame(i).save(p)

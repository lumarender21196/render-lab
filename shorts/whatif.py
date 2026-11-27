import sys,os,math,glob,random,subprocess
from helpers import *
import helpers as Hh
W,H=450,800;FPS=24;T=20.0;NF=int(T*FPS)
CARD=(236,226,212);BLUE=(110,170,230)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FA=sorted(glob.glob('/usr/share/fonts/**/NotoSansArabic-Bold.ttf',recursive=True)) or sorted(glob.glob('/usr/share/fonts/**/NotoSansArabic*.ttf',recursive=True))
def fnt(sz,ar=False):
    return ImageFont.truetype(FA[0],int(sz*S),layout_engine=ImageFont.Layout.RAQM) if ar else ImageFont.truetype(FB,int(sz*S))
def txt(d,x,y,s,sz,col=INK,ar=False,anchor='mm'):
    d.text((x*S,y*S),s,font=fnt(sz,ar),fill=col,anchor=anchor,**({'direction':'rtl'} if ar else {}))
def card(d,x0,y0,x1,y1):
    rect(d,x0+4,y0+5,x1+4,y1+5,fill=(214,202,186),r=22);rect(d,x0,y0,x1,y1,fill=CARD,outline=INK,w=3,r=22)
GY=640
def mp(t):  # man world state: returns base y (feet), x, flail
    # phases
    if t<6: return GY,225,0
    if t<16.2:
        u=t-6;rise=45*u+6*u*u   # accelerating rise
        return GY-rise-0,225+math.sin(u*1.3)*40,1
    if t<18.2:
        u=t-16.2;top=GY-(45*10.2+6*10.2*10.2)
        v=u/2.0;return top+(GY-top)*(v*v),225+math.sin(10)*40*(1-v),2
    return GY,225,3
def frame(i):
    t=i/FPS
    mb,mx,mode=mp(t)
    man_c=mb-90
    cy=min(400,man_c-40) if mode in(1,2) else 400
    oy=400-cy
    im=Image.new('RGB',(W*S,H*S),BG);d=ImageDraw.Draw(im)
    # clouds / depth lines (world)
    for k in range(14):
        cx=(k*97)%520-40;cyw=GY-300-k*130
        yy=cyw+oy
        if -60<yy<H+60:
            for dx,dr in((0,26),(26,20),(-24,18),(12,16)):circ(d,cx+dx,yy-dr*0.3,dr,fill=(250,246,238))
    # ground
    gy=GY+oy
    if gy<H+20:
        rect(d,-10,gy+8,W+10,H+300,fill=(226,214,196));d.line([(0,(gy+8)*S),(W*S,(gy+8)*S)],fill=INK,width=3*S)
        # tree
        rect(d,60,gy-150,76,gy+8,fill=(140,100,70));circ(d,68,gy-170,48,fill=(120,170,110),outline=INK,w=3)
    # objects
    def ball(x,y):circ(d,x,y+oy,16,fill=RED,outline=INK,w=3)
    # ball
    if t<6: ball(340,GY-16)
    else:
        u=t-6;by=GY-16-(40*u+30*u*u);bx=340+u*14
        if t>=16.2:
            v=min(1,(t-16.2)/2.0);            by=-400+(GY-16+400)*(v*v)*1.0;bx=340+10.2*14
            by=by if v<1 else GY-16
        ball(bx,by) if by<GY+40 else None
    # book rotates
    if t<6: pap(d,110,GY-8+oy,0,w=46,h=34)
    else:
        u=t-6;ty=GY-8-(18*u+14*u*u)
        if t>=16.2:
            v=min(1,(t-16.2)/2.0);ty=-300+(GY-8+300)*(v*v)
        pap(d,110+u*8,ty+oy,u*1.6 if t<16.2 else 0,w=46,h=34)
    # man
    flail=math.sin(t*9)*40
    if mode==0: aL,aR=(110,95),(30,-20) if t<6 else (70,60)
    elif mode==1: aL,aR=(200+flail,170-flail),(-20-flail,10+flail)
    elif mode==2: aL,aR=(250,230),(-70,-90)
    else:
        sq=(t-18.2);aL,aR=(120,100),(60,100)
    walk=1 if mode==1 else 0
    tl=0
    if mode==3: tl=-20*max(0,1-(t-18.2)*1.5)
    if mode in(1,2):
        lay=Image.new('RGBA',(220*S,320*S),(0,0,0,0));ld=ImageDraw.Draw(lay)
        man(ld,110,250,t*(2 if mode==1 else 1),walk=walk,armL=aL,armR=aR,tilt=0,lean=0)
        if mode==1:
            u=t-6;ang=35*math.sin(u*1.1)+u*28
        else:
            v=(t-16.2)/2.0;ang0=35*math.sin(10.2*1.1)+10.2*28;ang=(ang0%360)*(1-ease(v*1.25)) if v<0.8 else 0
            if ang>180:ang-=360
        rl=lay.rotate(-ang,center=(110*S,160*S),resample=Image.BICUBIC)
        im.paste(rl,(int((mx-110)*S),int((mb+oy-250)*S)),rl)
        hands=[(mx,mb-90),(mx,mb-90)];d=ImageDraw.Draw(im)
    else:
        sh,hands=man(d,mx,mb+oy,t,walk=0,armL=aL,armR=aR,tilt=tl,lean=0)
    # cup
    if t<6:
        h=hands[1];rect(d,h[0]-9,h[1]-20,h[0]+9,h[1]+2,fill=(250,246,238),outline=INK,w=2,r=3)
    elif t<16.2:
        u=t-6;cxp=mx+30+u*9;cyp=mb-150-u*28;rect(d,cxp-9,cyp-20+oy,cxp+9,cyp+2+oy,fill=(250,246,238),outline=INK,w=2,r=3)
        for k in range(7):
            circ(d,cxp+math.sin(k*2+u)*22+k*3,cyp-10+oy-k*14-u*10%30,5,fill=BLUE)
    else:
        v=(t-16.2)/2.0
        if t<18.9:
            cyp=-300+(GY-170+300)*min(1,max(0,(t-16.2)/2.7))**2;rect(d,mx-9,cyp-20+oy,mx+9,cyp+2+oy,fill=(250,246,238),outline=INK,w=2,r=3)
        else: rect(d,mx-9,GY-212+oy+(t-18.9)*40*0,mx+9,GY-190+oy,fill=(250,246,238),outline=INK,w=2,r=3)
    # speed lines when falling/rising
    if mode in(1,2):
        for k in range(10):
            x=(k*53+i*7)%W;y=(k*131+i*40)%H;ln(d,(x,y),(x,y+40*(1 if mode==2 else 0.5)),2,(205,192,172))
    # dust and stars on impact
    if t>=18.2:
        u=t-18.2
        for k in range(8):
            a=k*0.785;r=20+u*90;circ(d,mx+math.cos(a)*r,GY-6+oy+math.sin(a)*r*0.3,max(1,8-u*6),fill=(205,192,172))
        if u>0.7:
            for k in range(3):
                a=k*2.1+t*5;circ(d,mx+math.cos(a)*34,GY-245+oy+math.sin(a)*8,6,fill=(240,190,50),outline=INK,w=2)
    ui=Image.new('RGBA',(W*S,H*S),(0,0,0,0));u=ImageDraw.Draw(ui)
    # UI text
    # hook title card 0-3.4
    if t<3.6:
        pop=back(t/0.35);yoff=0
        card(u,28,70+yoff,422,(250 if os.environ.get('NOAR') else 320)+yoff)
        txt(u,225,118+yoff,'WHAT IF THERE',34);txt(u,225,168+yoff,'WAS NO',34)
        txt(u,225,218+yoff,'GRAVITY?',50,RED)
        (txt(u,225,282+yoff,'ماذا لو اختفت الجاذبية؟',30,INK,True) if not os.environ.get('NOAR') else None)
    else:
        a=ease((t-3.6)/0.4);y=28+ (1-a)*30
        rect(u,92,y,358,y+48,fill=CARD,outline=INK,w=3,r=20);txt(u,225,y+24,'WHAT IF: NO GRAVITY',19)
    if 5.0<=t<6.4:
        s=back((t-5.0)/0.3);card(u,60,150,390,260);txt(u,225,190,'GRAVITY',36,INK);txt(u,225,235,'OFF!',44,RED)
    if 8.5<=t<11.5:
        card(u,40,690,410,770);txt(u,225,716,"You can't walk.",24);txt(u,225,748,"You can't stop.",24,RED)
    if 12.0<=t<15.8:
        card(u,30,670,420,772);txt(u,225,700,'Everything not nailed',24);txt(u,225,740,'down floats away',24,RED)
    if 16.2<=t<17.9:
        s=back((t-16.2)/0.3);card(u,55,670,395,760);txt(u,225,715,'GRAVITY BACK!',34,RED)
    if t>=18.9:
        card(u,130,150,320,210);txt(u,225,180,'Ouch.',30)
    # camera: zoom + shake
    z=1.3+0.12*ease((t-6)/4)*(1 if t<16.2 else max(0,1-(t-16.2)))+ (0.14*ease((t-18.2)/0.2) if t>=18.2 else 0)
    if t<0.6:z+=0.04*(1-t/0.6)
    sk=0
    for ts,amp in((0.0,9),(5.0,6),(18.2,12)):
        if 0<=t-ts<0.5:sk=amp*(1-(t-ts)/0.5)*math.sin((t-ts)*60)
    cw=W*S/z;ch=H*S/z;cxm=W*S/2+sk*S;cym=H*S/2+(sk*0.6)*S
    cym=H*S*(0.66-0.11*ease((t-5.5)/1.0)+0.11*ease((t-17.5)/0.7))
    box=(int(cxm-cw/2),int(cym-ch/2),int(cxm+cw/2),int(cym+ch/2))
    box=(max(0,min(W*S-int(cw),box[0])),max(0,min(H*S-int(ch),box[1])),0,0)
    box=(box[0],box[1],box[0]+int(cw),box[1]+int(ch))
    out=im.crop(box).resize((720,1280),Image.LANCZOS).convert('RGBA')
    out.alpha_composite(ui.resize((720,1280),Image.LANCZOS))
    return out.convert('RGB')
if __name__=='__main__':
    os.makedirs('wf'+os.environ.get('SUF',''),exist_ok=True);a=int(sys.argv[1]);b=int(sys.argv[2])
    for i in range(a,min(b,NF)):
        p=f'wf'+os.environ.get('SUF','')+f'/{i:04d}.png'
        if not os.path.exists(p):frame(i).save(p)

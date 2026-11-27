import sys,os,math,random
from helpers import *
from whatif import txt,card,CARD
W,H=450,800;FPS=24;T=20.0;NF=int(T*FPS);GY=640;MX=225
def final(im,ui,t,shakes):
    zc=1.25;cw=W*S/zc;ch=H*S/zc;cx=W*S/2;cy=H*S*0.66;sk=0
    for ts,amp in shakes:
        if 0<=t-ts<0.4:sk=amp*(1-(t-ts)/0.4)*math.sin((t-ts)*60)
    bx=max(0,min(W*S-int(cw),int(cx-cw/2+sk*S)));by=max(0,min(H*S-int(ch),int(cy-ch/2)))
    out=im.crop((bx,by,bx+int(cw),by+int(ch))).resize((720,1280),Image.LANCZOS).convert('RGBA')
    out.alpha_composite(ui.resize((720,1280),Image.LANCZOS));return out.convert('RGB')
def title(u,t,l1,l2,l3,ar,tag):
    if t<3.6:
        card(u,28,70,422,320);txt(u,225,118,l1,34);txt(u,225,168,l2,34);txt(u,225,218,l3,48,RED)
        if not os.environ.get('NOAR'):txt(u,225,282,ar,28,INK,True)
    else:
        a=ease((t-3.6)/0.4);y=28+(1-a)*30;rect(u,60,y,390,y+48,fill=CARD,outline=INK,w=3,r=20);txt(u,225,y+24,tag,17)
def cap(u,t,items):
    for a,b,l1,l2 in items:
        if a<=t<b:
            card(u,40,690,410,770)
            if l2:txt(u,225,718,l1,24);txt(u,225,750,l2,24,RED)
            else:txt(u,225,730,l1,28,RED)
COL=[(235,80,110),(250,170,50),(120,200,90),(90,150,235),(180,100,220),(250,230,80)]
def candy(d,x,y,r,k,rot=0):
    c=COL[k%6]
    if k%3==0:
        circ(d,x,y,r,fill=c,outline=INK,w=2);d.arc([(x-r*0.6)*S,(y-r*0.6)*S,(x+r*0.6)*S,(y+r*0.6)*S],0,200,fill=(255,255,255),width=2*S)
    elif k%3==1:
        d.polygon([((x-r*1.6)*S,(y-r*0.6)*S),((x-r*0.6)*S,y*S),((x-r*1.6)*S,(y+r*0.6)*S)],fill=c,outline=INK);d.polygon([((x+r*1.6)*S,(y-r*0.6)*S),((x+r*0.6)*S,y*S),((x+r*1.6)*S,(y+r*0.6)*S)],fill=c,outline=INK)
        rect(d,x-r*0.9,y-r*0.6,x+r*0.9,y+r*0.6,fill=c,outline=INK,w=2,r=6)
    else:
        ln(d,(x,y),(x,y+r*2.4),3,INK);circ(d,x,y,r,fill=c,outline=INK,w=2);circ(d,x,y,r*0.5,fill=(255,255,255),outline=None)
def candyrain(i):
    t=i/FPS;im,HB=getbg('candy',(190,225,245),W,H);d=ImageDraw.Draw(im)
    rect(d,-10,GY+8,W+10,H+300,fill=(150,205,130));d.line([(0,(GY+8)*S),(W*S,(GY+8)*S)],fill=INK,width=3*S)
    for cx_,cy_ in(() if HB else((80,120),(300,90),(380,200))):
        for dx,dr in((0,28),(28,22),(-26,20)):circ(d,cx_+dx,cy_,dr,fill=(255,255,255))
    rnd=random.Random(5);items=[(rnd.uniform(10,440),rnd.uniform(0,1),rnd.uniform(1.3,2.4),rnd.randint(0,5),rnd.uniform(7,13)) for _ in range(150)]
    start=5.0;pile=0
    if t>start:pile=min(150,(t-start)*(8 if t<15 else 14))*0.5
    # pile
    pr=random.Random(9)
    for k in range(int(pile)):
        px=pr.uniform(0,450);py=GY+4-pr.uniform(0,1)**1.5*(pile*0.9)
        candy(d,px,py,pr.uniform(7,11),k)
    my=GY-pile*0.0
    # man
    if t<5:aL,aR=(100,95),(70,80)
    elif t<6.5:aL,aR=(-90,-70),(-80,-60)
    elif 8<=t<13:aL,aR=(-60,-30),(-70,-40)
    elif t<16:aL,aR=(100,95),(70,80)
    else:aL,aR=(-90,-60),(-90,-60)
    mb=GY-min(pile*0.35,40)
    sh,hands=man(d,MX,mb,t,walk=0,armL=aL,armR=aR,tilt=(15 if 8<=t<13 else 0),bob=1.5)
    if 8<=t<13:
        hx,hy=MX,mb-165-27;d.polygon([((hx-5)*S,(hy+6)*S),((hx+30)*S,(hy+14)*S),((hx+5)*S,(hy+22)*S)],fill=(120,40,50))
    # falling candies
    if t>start:
        for x,off,sp,k,r in items:
            ty=(t-start-off*6)*sp*260
            if ty>0 and ty<GY+30 and not(t>16 and x%2<1):
                if (t-start)<10 or True:candy(d,x,-30+ty,r,k)
    if 14<=t<16:
        u=(t-14)/2.0;gy=-80+ease(u)*(mb-205+80)
        circ(d,MX+8,gy,34,fill=(235,80,110),outline=INK,w=3)
    if 16<=t<16.6:
        for k in range(5):txt(d,MX-40+k*22,mb-250-k*3,'*',30,(250,200,40))
    ui=Image.new('RGBA',(W*S,H*S),(0,0,0,0));u=ImageDraw.Draw(ui)
    title(u,t,'WHAT IF IT','RAINED','CANDY?','ماذا لو أمطرت السماء حلوى؟','WHAT IF: CANDY RAIN')
    cap(u,t,[(5.0,6.6,'Wait...','is that candy?'),(8.0,12.5,'Free snacks.','Forever.'),(12.8,14.2,'Pile: 2 meters.','Sticky.'),(15.0,16.4,'Ouch!',None),(17.4,19.9,'Dentist: "Oh no."','You: "Worth it."')])
    if 5.0<=t<5.2:ui.paste(Image.new('RGBA',(W*S,H*S),(255,255,255,150)),(0,0))
    return final(im,ui,t,((5.0,4),(14.9,8)))
def nosleep(i):
    t=i/FPS;day=(t*0.5)%1 if t>5 else 0.25
    sky=(int(150+60*math.sin(day*6.28)),int(190+40*math.sin(day*6.28)),int(235+15*math.sin(day*6.28)))
    if t>5:
        night=int((t-5)/2.5)%2==1
    else:night=False
    im,HB=getbg('night' if night else 'meadow',(30,35,70) if night else (170,215,245),W,H);d=ImageDraw.Draw(im)
    if night and not HB:
        for k in range(30):circ(d,(k*97)%450,(k*53)%380,2,fill=(255,255,220))
        circ(d,340,120,34,fill=(245,240,200));circ(d,352,112,30,fill=(30,35,70))
    elif not HB:circ(d,340+0,120,36,fill=(255,225,110))
    rect(d,-10,GY+8,W+10,H+300,fill=(60,90,70) if night else (150,205,130));d.line([(0,(GY+8)*S),(W*S,(GY+8)*S)],fill=INK,width=3*S)
    # house
    rect(d,50,GY-110,170,GY+8,fill=(220,200,180),outline=INK,w=3);d.polygon([(40*S,(GY-110)*S),(110*S,(GY-160)*S),(180*S,(GY-110)*S)],fill=RED,outline=INK)
    rect(d,95,GY-70,125,GY-30,fill=(255,240,150) if night else (160,200,230),outline=INK,w=2)
    bed=t<5
    if t<5:aL,aR=(100,95),(70,80)
    elif t<9:aL,aR=(-70,-40),(-90,-70)
    elif t<13:aL,aR=(160,140),(10,30)
    elif t<16:aL,aR=(100,95),(70,80)
    else:aL,aR=(120,110),(60,70)
    wk=0.5 if 9<=t<13 else 0
    mx=MX+(math.sin(t*1.5)*60 if 9<=t<13 else 0)
    sh,hands=man(d,mx,GY,t,walk=wk,armL=aL,armR=aR,tilt=(10 if t>14 else 0),bob=1)
    # eye bags grow
    if t>10:
        a=min(1,(t-10)/5);hx,hy=mx+9,GY-165-27+3
        d.ellipse([(hx-6)*S,(hy+4)*S,(hx+6)*S,(hy+12)*S],fill=(120,90,130));d.ellipse([(hx+7)*S,(hy+4)*S,(hx+19)*S,(hy+12)*S],fill=(120,90,130))
    # coffee
    if 7<=t<9.5:
        hh=hands[0];rect(d,hh[0]-8,hh[1]-14,hh[0]+8,hh[1]+4,fill=(240,240,240),outline=INK,w=2);
    if 13<=t<16:
        for k in range(3):circ(d,mx+30+k*25,GY-250-k*30,8+k*3,fill=(255,255,255),outline=INK,w=2)
    ui=Image.new('RGBA',(W*S,H*S),(0,0,0,0));u=ImageDraw.Draw(ui)
    title(u,t,'WHAT IF YOU','NEVER NEEDED','SLEEP?','ماذا لو ما احتجت تنام؟','WHAT IF: NO SLEEP')
    if t>=5.0:
        dd=int((t-5)/2.5)+1;rect(u,300,90,430,150,fill=CARD,outline=INK,w=3,r=14);txt(u,365,120,f'DAY {dd}',22)
    cap(u,t,[(5.0,7.0,'24 hours awake.','Nice!'),(7.2,9.5,'More time.','More coffee.'),(9.6,13.0,'All night:','free time!'),(13.2,15.8,'Day 4...','Brain: "...?"'),(16.4,19.9,'Sleep is not','a waste.')])
    if 5.0<=t<5.2:ui.paste(Image.new('RGBA',(W*S,H*S),(255,255,255,150)),(0,0))
    return final(im,ui,t,((5.0,4),))
if __name__=='__main__':
    nm=sys.argv[1];fn={'candy':candyrain,'sleep':nosleep}[nm];D=nm+os.environ.get('SUF','');os.makedirs(D,exist_ok=True)
    for i in range(int(sys.argv[2]),min(int(sys.argv[3]),NF)):
        p=f'{D}/{i:04d}.png'
        if not os.path.exists(p):fn(i).save(p)

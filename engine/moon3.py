import sys,os,math,random
from moon import *
import moon as M
DUR=[9,9,10,10,9,9,9,8];ST=[sum(DUR[:i]) for i in range(len(DUR))];TT=sum(DUR)
LAB={0:"",1:"",2:"تخيّل: مش علم",3:"تخيّل: مش علم",4:"علم: المد يضعف",5:"علم: الحيوانات بتتلخبط",6:"علم: ميل الأرض يتأرجح",7:""}
DK=(8,10,20)
def runner(d,x,base,t,ph,col=(235,230,215),dirn=1,arms=(-110,-70)):
    man(d,x,base,t+ph,walk=1.6,armL=(arms[0],arms[1]),armR=(arms[1]-10,arms[0]+10),tilt=12*dirn,col=col,scarf=False,head=DK,bob=2)
def sc0(d,t,lt,du,im):
    gone=lt>5.0
    bg=DK if gone else NIGHT
    d.rectangle([0,0,W*S,H*S],fill=bg);stars(d,t,40,1.0 if not gone else 0.0,3);ground(d,(30,38,40) if not gone else (12,14,16))
    if lt<5: moon(d,860,200,90,1,NIGHT)
    elif lt<5.8:
        r=90*(1-ease((lt-5)/0.8));moon(d,860,200,max(1,r),1-ease((lt-5)/0.8),NIGHT)
    if 5.0<lt<5.12:d.rectangle([0,0,W*S,H*S],fill=(255,255,255))
    for i,x in enumerate((250,360,470,580,690)):
        up=lt<5.0
        if up: man(d,x,560,t+i,armL=(100,100),armR=(-60,-30),tilt=-14,col=(235,230,215),scarf=False,head=NIGHT)
        else:
            sh=3*math.sin(t*14+i)
            man(d,x+sh,560,t+i,armL=(-120,-60),armR=(-60,-120),tilt=0,bob=3,col=(235,230,215),scarf=False,head=DK)
            if lt>6.2:txt(d,x,300+math.sin(t*9+i)*4,"!!" if i%2 else "آاااه",40,(255,120,90))
    if gone:
        # eyes only glow
        pass
def sc1(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=(5,6,12));stars(d,t,25,0.5,5);ground(d,(10,12,14))
    # buildings silhouettes with a few lit windows flickering
    random.seed(4)
    for i in range(7):
        bx=40+i*180;bh=180+(i*37)%120;rect(d,bx,560-bh,bx+130,560,fill=(14,16,24))
        for r_ in range(4):
            for c_ in range(3):
                if (r_*3+c_+i)%3==0 and int(t*3+i+r_)%7:rect(d,bx+14+c_*38,560-bh+20+r_*38,bx+40+c_*38,560-bh+44+r_*38,fill=(250,220,120))
    for i in range(10):
        dirn=1 if i%2 else -1
        x=((lt*(160+i*18)*dirn)+i*170)%1500-110
        if dirn<0:x=1280-x
        runner(d,x,600+(i%3)*14,t,i,dirn=dirn)
        if i%3==0:txt(d,x,430+(i%3)*14,"!",34,(255,120,90))
    for i in range(3):txt(d,200+i*400+math.sin(t*5+i)*8,330+math.sin(t*7+i)*6,("آاااه","إيييه","الحقوني")[i],38,(255,255,255))
def sc2(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=(30,26,30));ground(d,(60,44,36),540)
    # TV
    rect(d,380,50,900,350,fill=(20,20,24),outline=(90,90,100),w=8,r=16)
    rect(d,396,66,884,334,fill=(40,60,110),r=8)
    # president at podium, talking
    rect(d,560,260,720,334,fill=(130,90,60));man(d,640,454,t,armL=(100,100),armR=(70+20*math.sin(t*6),50),scarf=False,col=(235,230,215),head=(40,60,110),bob=0.3) if False else None
    px=640;circ(d,px,150,24,fill=(40,60,110),outline=(235,230,215),w=4);ln(d,(px,174),(px,260),5,(235,230,215))
    ln(d,(px,190),(px-40,240+10*math.sin(t*6)),5,(235,230,215));ln(d,(px,190),(px+40,230-10*math.sin(t*6+1)),5,(235,230,215))
    rect(d,px-28,262,px+28,270,fill=(235,230,215)) if False else None
    ln(d,(px-24,116),(px+24,116),6,RED)  # tie-like band = president mark
    circ(d,px+8,150,3,fill=(235,230,215));circ(d,px+20,150,3,fill=(235,230,215))
    # mouth flap
    ln(d,(px+2,162),(px+18,162+4*abs(math.sin(t*9))),3,(235,230,215))
    rect(d,420,80,550,110,fill=RED,r=6);txt(d,485,95,"عاجل",22,'white')
    # audience: 3 stick men on couch reacting
    rect(d,260,520,1020,570,fill=(90,60,50),r=18)
    for i,x in enumerate((420,540,660,780,900)):
        if lt<4:man(d,x,540,t+i,armL=(100,100),armR=(80,80),scarf=False,col=(235,230,215),head=(30,26,30),bob=1)
        else:man(d,x,540,t+i,armL=(-120,-60),armR=(-60,-120),scarf=False,col=(235,230,215),head=(30,26,30),bob=3)
    if lt>4:
        for i in range(3):txt(d,420+i*240,380+math.sin(t*6+i)*5,("؟","!","؟")[i],44,(255,200,120))
def rocket(d,x,y,t,fire=True):
    d.polygon([((x-14)*S,(y+60)*S),((x+14)*S,(y+60)*S),((x+14)*S,(y)*S),((x)*S,(y-30)*S),((x-14)*S,(y)*S)],fill=(235,235,240),outline=K)
    circ(d,x,y+15,6,fill=(90,150,210))
    d.polygon([((x-14)*S,(y+60)*S),((x-26)*S,(y+78)*S),((x-14)*S,(y+40)*S)],fill=RED);d.polygon([((x+14)*S,(y+60)*S),((x+26)*S,(y+78)*S),((x+14)*S,(y+40)*S)],fill=RED)
    if fire:
        f=30+12*math.sin(t*30);d.polygon([((x-10)*S,(y+60)*S),((x+10)*S,(y+60)*S),((x)*S,(y+60+f)*S)],fill=(250,170,40))
def sc3(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=DK);stars(d,t,15,0.0,6);ground(d,(14,16,18),560)
    stars(d,t,0)
    # control tower + stick-man engineer
    rect(d,160,420,300,560,fill=(40,44,52));man(d,230,560,t,armL=(-110,-70),armR=(-60,-100),scarf=False,col=(235,230,215),head=(40,44,52),bob=2)
    # rockets launch one by one, each reaches a small lamp and it fades
    for k,(rx,t0) in enumerate(((560,0.5),(760,3.2),(960,5.8))):
        q=lt-t0
        if q<0:rocket(d,rx,500,t,False)
        elif q<2.2:rocket(d,rx,500-q*210,t,True)
        else:
            # lamp satellite in orbit glow, small
            a=clamp(1-(q-2.2)/2.2)*1
            circ(d,rx,60+k*10,10+14*a,fill=(int(255*(0.3+0.7*a)),int(230*(0.3+0.7*a)),int(130*a+40)))
            if q>3.5:txt(d,rx,115+k*10,"ضعيف",24,(160,160,170))
    if lt>7:txt(d,640,650,"المحاولة فشلت: ضوء ضعيف جداً",30,(255,255,255))
def sc4(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=(205,230,245));d.rectangle([0,430*S,W*S,H*S],fill=(235,215,170))
    q=ease((lt-du*0.3)/(du*0.35));amp=44*(1-0.67*q);lvl=330+q*70
    poly=[(x*S,(lvl+amp*math.sin(x/90+t*1.6*(1-0.5*q))+(x/W)*40)*S) for x in range(0,W+20,20)]
    d.polygon(poly+[(W*S,H*S),(0,H*S)],fill=(70,140,200))
    circ(d,1100,130,40,fill=(250,205,70));moon(d,200,110,40,1-q,(205,230,245))
    d.polygon([(100*S,560*S),(180*S,500*S),(300*S,560*S)],fill=(120,110,100))
    for cx in (230,520,860):
        cy=545;circ(d,cx,cy,16,fill=RED);ln(d,(cx-16,cy),(cx-32,cy-14),4,RED);ln(d,(cx+16,cy),(cx+32,cy-14),4,RED)
        if q>0.5:txt(d,cx,cy-45,"؟",34)
    by=470+q*40;d.polygon([(960*S,by*S),(1160*S,by*S),(1130*S,(by+40)*S),(990*S,(by+40)*S)],fill=(150,100,60))
    ln(d,(1060,by),(1060,by-90),4,K);d.polygon([(1060*S,(by-90)*S),(1060*S,(by-30)*S),(1120*S,(by-30)*S)],fill=(250,245,235),outline=K)
    man(d,600,600,t,armL=(80,60),armR=(-60,-100) if q>0.5 else (80,80),col=K,head=(235,215,170),bob=1)
def sc5(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=DK);stars(d,t,20,0.4,3);ground(d,(12,14,16))
    # owl confused, beetle circles, sea turtle going the wrong way
    ln(d,(100,260),(500,250),8,(80,60,45));ox=300;circ(d,ox,228,34,fill=(150,115,80))
    for k in(-12,12):circ(d,ox+k,220,10,fill=(255,230,120));circ(d,ox+k+8*math.sin(t*4),220,4,fill=K)
    txt(d,ox,170,"؟",40,(255,255,255))
    bx=700+math.cos(t*2.4)*70;by=548+math.sin(t*2.4)*10;circ(d,bx,by,16,fill=(120,85,50));circ(d,bx-28,by+8,9,fill=(80,60,40));txt(d,bx,500,"؟",30,(255,255,255))
    tx=1000+math.sin(t*1.1)*110;ty=520
    circ(d,tx,ty,34,fill=(90,150,100));circ(d,tx+(40 if math.cos(t*1.1)>0 else -40),ty,11,fill=(90,150,100))
    for dx in (-22,22):circ(d,tx+dx,ty+26,8,fill=(90,150,100))
    txt(d,tx,ty-60,"؟",34,(255,255,255))
def sc6(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=NIGHT);stars(d,t,40,0.8,5);p=lt/du
    wob=clamp((p-0.3)/0.3);sh=6*math.sin(t*9)*wob
    earth(d,640+sh,360,150,23+sh*1.2+10*wob*math.sin(t*1.5),spin=t*0.4)
    hot=(math.sin(t*1.5)>0) if wob>0 else True
    sun(d,160,200,40) if hot else None
    man(d,160,600,t,armL=(100,100),armR=(-100,-60),scarf=False,col=(235,230,215),head=NIGHT)
    if wob>0:
        txt(d,160,300,"حر؟" if hot else "برد؟",34,(255,200,120))
        man(d,1120,600,t,armL=(90,90),armR=(-100,-100),scarf=False,col=(235,230,215),head=NIGHT)
        txt(d,1120,300,"برد؟" if hot else "حر؟",34,(150,200,255))
def sc7(d,t,lt,du,im):
    back=lt>3.0
    d.rectangle([0,0,W*S,H*S],fill=DK if not back else (40,48,86));stars(d,t,50,0.9 if back else 0.2,13);ground(d,(25,28,34))
    s=ease((lt-3.0)/1.5)
    if back:moon(d,960,230-(1-s)*150,100,s,(40,48,86))
    for i,x in enumerate((300,400,500,600,700)):
        if not back:man(d,x,560,t+i,armL=(100,100),armR=(80,80),scarf=False,col=(235,230,215),head=DK,tilt=6*math.sin(t+i))
        else:man(d,x,560-abs(math.sin(t*5+i))*30,t+i,armL=(-110,-70),armR=(-70,-110),scarf=False,col=(235,230,215),head=(40,48,86),bob=3)
    if back and lt>4.5:
        for i in range(8):a=t*2+i;circ(d,960+math.cos(a)*150,230+math.sin(a)*130,5,fill=(255,230,120))
        bubble(d,500,330,"وحشتني",RED,34)
M.SCF3=[sc0,sc1,sc2,sc3,sc4,sc5,sc6,sc7]
def frame(t):
    idx=max(i for i in range(len(ST)) if t>=ST[i]);lt=t-ST[idx];du=DUR[idx]
    im=Image.new('RGB',(W*S,H*S),BG);d=ImageDraw.Draw(im)
    M.SCF3[idx](d,t,lt,du,im)
    if lt<0.5 and idx>0:d.rectangle([0,0,W*S,H*S],fill=(0,0,0)) if False else None
    im=im.resize((W,H),Image.LANCZOS);d=ImageDraw.Draw(im)
    if LAB[idx]:
        w=d.textlength(LAB[idx],font=F(28),direction='rtl');d.rounded_rectangle([W-30-w-24,14,W-30,60],12,fill=(30,26,24))
        d.text((W-42,37),LAB[idx],font=F(28),fill=(255,230,120),anchor='rm',direction='rtl')
    return im
if __name__=='__main__':
    a=int(sys.argv[1]);b=int(sys.argv[2]);os.makedirs('g',exist_ok=True)
    if a<0:
        for i in range(len(DUR)):frame(ST[i]+DUR[i]*0.7).save(f'q{i}.png')
        sys.exit()
    for n in range(a,min(b,int(TT*FPS))):
        p=f'g/{n:05d}.png'
        if not os.path.exists(p):frame(n/FPS).save(p)

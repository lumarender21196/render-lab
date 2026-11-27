import sys,os,math,random
from moon3 import *
import moon as M
import moon3 as M3
DUR4=[14,14,16,22,28,28,14,30,24,28,26,22,14];ST4=[sum(DUR4[:i]) for i in range(len(DUR4))];TT4=sum(DUR4)
LAB4=["","تخيّل","تخيّل: مش علم","علم: الحيوانات","تمثيلية: مش حدث علمي","علم: المد يضعف","تخيّل","علم: ميل الأرض","علم: طول اليوم","علم: الكسوف","علم: التقويم","",""]
CAP={0:[(1,5,"ليلة عادية... والقمر الكامل فوق الكل",""),(6,14,"فجأة اختفى. مفيش صوت، السما بس ضلمت","")],
1:[(0,7,"أول رد فعل: هلع!",""),(7,14,"بس الحقيقة أهدى وأغرب من كده","")],
2:[(0,8,"عاجل: القمر اختفى!",""),(8,16,"مفيش نهاية عالم النهارده... التغيير بيجي ببطء","")],
3:[(0,7,"الليل بقى أضلم: البدر بيدّي نور ضعيف","حوالي ربع لوكس تقدير"),(7,15,"خنافس الروث بتمشي بنمط ضوء القمر المستقطب",""),(15,22,"من غير القمر بوصلتها بتروح وبتلف في دايرة","")],
4:[(0,9,"تمثيلية: ستيك مان في طريق ريفي من غير قمر",""),(9,19,"الكشاف بس... كل خطوة أبطأ وكل ضل مخيف",""),(19,28,"في المدن الأنوار الصناعية بتخلّي الليلة عادية تقريباً","")],
5:[(0,9,"المد والجزر سببه الأساسي جاذبية القمر",""),(9,19,"مد الشمس تقريباً نص مد القمر حسب هيئة المحيطات الأمريكية","1 : 2"),(19,28,"من غير القمر: المد حوالي ثلث الحالي تقدير باحث","حوالي ثلث المد")],
6:[(0,6,"نعوّض القمر بأقمار صناعية؟",""),(6,14,"المحاولة فشلت: ضوءها ضعيف جداً","")],
7:[(0,9,"الأرض مايلة حوالي 23 درجة: ده سبب الفصول","23 درجة"),(9,19,"القمر بيثبّت الميل بين 22.1 و24.5 درجة",""),(19,30,"من غير القمر الميل هيتذبذب أكتر على مئات آلاف السنين، والعلماء لسه مختلفين","")],
8:[(0,8,"القمر بيبعد عننا كل سنة","3.8 سم في السنة"),(8,16,"واليوم بيطول ميلي ثانية أو اتنين كل قرن","1 إلى 2.3 ميلي ثانية في القرن"),(16,24,"لو اختفى: اليوم هيفضل قريب من 24 ساعة","")],
9:[(0,9,"النهارده القمر بيغطي الشمس بالظبط: كسوف كلي",""),(9,19,"لما القمر يبعد كفاية، قرصه هيصغر",""),(19,28,"الكلي هيبقى كسوف حلقي حسب ناسا... بعد زمن بعيد جداً","")],
10:[(0,9,"التقويم الهجري بالشهور القمرية","354 أو 355 يوم"),(9,18,"بداية رمضان والعيد بتعتمد على رؤية الهلال",""),(18,26,"من غير قمر: مفيش هلال ولا شهر قمري","")],
11:[(0,22,"الخلاصة: مش هنموت في يوم... بس العالم هيتغير ببطء","")],
12:[(3,14,"وفجأة... القمر رجع!","")]}
def pose(t,i):  # variety of arm poses
    k=int(t*0.7+i)%4
    return [((100,100),(80,80)),((-110,-70),(-60,-110)),((100,100),(-70,-30)),((80,60),(-100,-80))][k]
def sc_dark(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=(10,12,22));stars(d,t,30,0.15,8);ground(d,(14,16,18),560)
    ln(d,(0,600),(1280,600),60,(24,26,28))
    # trees and owl
    for tx in (120,1100):ln(d,(tx,560),(tx,330),12,(30,24,22));circ(d,tx,310,60,fill=(16,28,24))
    ox=1100;circ(d,ox,420,22,fill=(120,90,60));[circ(d,ox+k,414,7,fill=(255,230,120)) for k in(-8,8)]
    p=lt/du;x=100+p*900
    stumble=0.30<p<0.42;fall=0.42<=p<0.55;sh=0.55<=p<0.62
    xx=x if not fall else 100+0.42*900
    if fall:
        ln(d,(xx-60,590),(xx+60,590),5);circ(d,xx+66,590,24,fill=BG,outline=K,w=4);txt(d,xx,520,"آاخ!",36,(255,200,120))
        for i in range(3):txt(d,xx+80+i*30,500-i*22,("★","★","★")[i],26,(255,230,120))
    else:
        tilt=22*math.sin(lt*14) if stumble else 0
        a=(-100,-60) if stumble else ((60,40) if sh else (80,80))
        hands,hd=man(d,xx,590,t,walk=0 if sh else 1.2,armL=(70,40),armR=a,tilt=tilt,scarf=False,col=(235,230,215),head=(10,12,22),bob=1.5)
        hx,hy=hands[0]
        # flashlight cone (weakens over time)
        k=max(0.25,1-p*0.9);cone=[(hx*S,hy*S),((hx+260*k)*S,(hy-60)*S),((hx+260*k)*S,(hy+90)*S)]
        d.polygon(cone,fill=(int(70*k)+25,int(66*k)+25,int(40*k)+20))
        if sh:txt(d,xx,420,"؟!",30,(255,255,255))
        elif stumble:txt(d,xx,430,"!",44,(255,120,90))
    if 0.62<=p<0.75:
        x2=100+p*900;[txt(d,x2+i*60,430,"ههه",30,(255,230,120)) for i in range(1)]
    if p>0.7:
        for i in range(5):
            xs=150+i*200;rect(d,xs,500,xs+60,560,fill=(40,36,30),r=4);rect(d,xs+16,512,xs+44,534,fill=(250,220,120))
def sun2(d,x,y,r,col=(250,205,70)):
    for k in range(16):
        a=k*math.pi/8;ln(d,(x+math.cos(a)*r*1.15,y+math.sin(a)*r*1.15),(x+math.cos(a)*r*1.5,y+math.sin(a)*r*1.5),5,col)
    circ(d,x,y,r,fill=col)
def sc_day(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=NIGHT);stars(d,t,40,0.9,6);p=lt/du
    ex=420;circ(d,ex,330,110,fill=(60,120,190));circ(d,ex-30,300,40,fill=(80,160,100));circ(d,ex+40,360,34,fill=(80,160,100))
    mx=640+ease(p)*300;moon(d,mx,330,34,1,NIGHT)
    ln(d,(520,470),(560+min(p,1)*300+60,470),3,(255,255,255))
    txt(d,820,500,"المسافة بتزيد... سنتيمترات بس",26,(255,230,120))
    # clock
    cx,cy=1100,150;circ(d,cx,cy,70,fill=(240,235,225),outline=K,w=5)
    [ln(d,(cx+math.cos(k*math.pi/6)*58,cy+math.sin(k*math.pi/6)*58),(cx+math.cos(k*math.pi/6)*66,cy+math.sin(k*math.pi/6)*66),3) for k in range(12)]
    a=t*0.8;ln(d,(cx,cy),(cx+math.cos(a)*50,cy+math.sin(a)*50),5);ln(d,(cx,cy),(cx+math.cos(a/12)*34,cy+math.sin(a/12)*34),7,RED)
    # stick-man with ruler
    hands,_=man(d,160,600,t,armL=pose(t,0)[0],armR=(-20+15*math.sin(t*2),-10),scarf=False,col=(235,230,215),head=NIGHT)
    if p>0.65:txt(d,640,640,"24 ساعة تقريباً",40,(255,255,255))
def sc_ecl(d,t,lt,du,im):
    p=lt/du;sky=(40,60,110) if p<0.35 else (90,150,210)
    d.rectangle([0,0,W*S,H*S],fill=sky);ground(d,(50,70,50),600)
    sx,sy=640,230
    sun2(d,sx,sy,60)
    if p<0.35:
        rr=60;mx=sx+(0.35-p)*0*0;mrx=sx-max(0,(0.12-p))*400;circ(d,mrx,sy,rr,fill=(16,16,24))
        if p>0.15:
            for k in range(24):a=k*math.pi/12;ln(d,(sx+math.cos(a)*68,sy+math.sin(a)*68),(sx+math.cos(a)*(90+10*math.sin(t*5+k)),sy+math.sin(a)*(90+10*math.sin(t*5+k))),3,(255,255,255))
    else:
        q=ease((p-0.35)/0.45);rr=60-q*20;mrx=sx+q*330*0;rry=sy-q*0;circ(d,sx,sy,rr,fill=(16,16,24))
        circ(d,sx,sy,60,outline=(250,205,70),w=5)
        if rr<56:circ(d,sx,sy,rr,fill=(16,16,24));circ(d,sx,sy,60,outline=(255,235,150),w=4)
    for i,x in enumerate((300,420,860,980)):
        man(d,x,600,t+i,armL=(-100,-70) if i%2 else (100,100),armR=(-80,-100),scarf=False,col=K,head=sky,tilt=-10)
        txt(d,x,400,"واو" if p<0.35 else "؟",32,K if p>0.35 else (255,255,255))
    if p>0.75:txt(d,640,420,"كسوف حلقي: حلقة نار",36,(255,235,150))
def sc_cres(d,t,lt,du,im):
    p=lt/du
    d.rectangle([0,0,W*S,H*S],fill=(22,26,60));stars(d,t,40,0.7,9);ground(d,(26,24,30),580)
    # search sweep
    sx=300+math.sin(t*0.9)*380
    circ(d,sx,150,46,outline=(255,255,255),w=3);ln(d,(sx,196),(sx,260),3,(255,255,255)) if False else None
    if p<0.6:
        hands,hd=man(d,640,600,t,armL=(-100,-50),armR=(-120,-70),scarf=False,col=(235,230,215),head=(22,26,60),tilt=12*math.sin(t*0.9))
        txt(d,hd[0]+60,hd[1]-60,"فين الهلال؟",34,(255,230,120))
        ln(d,hands[1],(hands[1][0]+30*math.cos(math.radians(-35)),hands[1][1]+30*math.sin(math.radians(-35))),9,(150,150,160))
    else:
        man(d,640,600,t,armL=(60,30),armR=(40,60),scarf=False,col=(235,230,215),head=(22,26,60))
        txt(d,640,430,"مفيش شهر قمري",36,(255,200,120))
    # lantern + calendar
    lx=1090;ln(d,(lx,60),(lx,100),4,(255,255,255));rect(d,lx-26,100,lx+26,180,fill=RED,r=10);circ(d,lx,140,12,fill=(255,230,120))
    rect(d,90,80,260,230,fill=(245,240,230),r=8);rect(d,90,80,260,115,fill=RED,r=8)
    for r_ in range(3):
        for c in range(5):
            on=(int(t*2)%15==r_*5+c);rect(d,100+c*32,128+r_*32,124+c*32,152+r_*32,fill=(255,200,100) if on else (210,205,195),r=4)
def sc_sum(d,t,lt,du,im):
    d.rectangle([0,0,W*S,H*S],fill=(30,26,30));stars(d,t,30,0.5,4);ground(d,(24,22,26),580)
    cards=[("ليل أضلم",(60,60,100)),("مد أضعف",(50,110,160)),("مناخ أقل استقراراً",(150,100,70)),("تقويم يتغير",(120,70,120))]
    for i,(s,c) in enumerate(cards):
        q=ease((lt-1.0-i*3.2)/0.5)
        if q<=0:continue
        x=210+i*290;y=330+(1-q)*200
        rect(d,x-120,y-110,x+120,y+110,fill=c,outline=(255,255,255),w=4,r=18);txt(d,x,y-30,s,34 if len(s)<12 else 27,(255,255,255))
        ic=y+50
        if i==0:moon(d,x,ic,30,0.4,c)
        if i==1:
            poly=[((x-80+k*10)*S,(ic+12*math.sin(k*0.9+t*2))*S) for k in range(17)];d.polygon(poly+[((x+80)*S,(ic+50)*S),((x-80)*S,(ic+50)*S)],fill=(200,230,255))
        if i==2:earth(d,x,ic,30,23+8*math.sin(t*2),spin=t*0.5)
        if i==3:circ(d,x,ic,24,outline=(255,255,255),w=4);ln(d,(x,ic),(x+16,ic-10),4,(255,255,255))
    man(d,640,600,t,armL=pose(t,2)[0],armR=pose(t,2)[1],scarf=False,col=(235,230,215),head=(30,26,30))
SC4=[sc0,sc1,sc2,sc5,sc_dark,sc4,sc3,sc6,sc_day,sc_ecl,sc_cres,sc_sum,sc7]
def pill(d,x,y,s,sz,fill,col):
    w=d.textlength(s,font=F(sz),direction='rtl');d.rounded_rectangle([x-w/2-22,y-sz*0.85,x+w/2+22,y+sz*0.85],18,fill=fill)
    d.text((x,y),s,font=F(sz),fill=col,anchor='mm',direction='rtl')
def frame4(t):
    idx=max(i for i in range(len(ST4)) if t>=ST4[i]);lt=t-ST4[idx];du=DUR4[idx]
    im=Image.new('RGB',(W*S,H*S),BG);d=ImageDraw.Draw(im)
    SC4[idx](d,t,lt,du,im)
    im=im.resize((W,H),Image.LANCZOS);d=ImageDraw.Draw(im)
    if LAB4[idx]:
        w=d.textlength(LAB4[idx],font=F(28),direction='rtl');d.rounded_rectangle([W-30-w-24,14,W-30,60],12,fill=(30,26,24))
        d.text((W-42,37),LAB4[idx],font=F(28),fill=(255,230,120),anchor='rm',direction='rtl')
    for a,b,s,chip in CAP.get(idx,[]):
        if a<=lt<b:
            q=ease((lt-a)/0.3);y=668+(1-q)*40
            if chip:pill(d,W//2,y-62,chip,34,(255,230,120),(30,26,24))
            pill(d,W//2,y,s,30 if len(s)<48 else 26,(20,18,22),(255,255,255))
    return im
if __name__=='__main__':
    a=int(sys.argv[1]);b=int(sys.argv[2]);os.makedirs('g4',exist_ok=True)
    if a<0:
        for i in range(len(DUR4)):frame4(ST4[i]+DUR4[i]*0.6).save(f'v{i}.png')
        sys.exit()
    for n in range(a,min(b,int(TT4*FPS))):
        p=f'g4/{n:05d}.png'
        if not os.path.exists(p):frame4(n/FPS).save(p)

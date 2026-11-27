"""Render frames [a,b) of a scene module into out/NNNNN.png. Usage: python render_chunk.py moon4 frame4 0 700"""
import sys,os,importlib
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'engine'))
mod,func,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
m=importlib.import_module(mod);f=getattr(m,func);fps=m.FPS
os.makedirs('out',exist_ok=True)
for n in range(a,b):
    p=f'out/{n:05d}.png'
    if not os.path.exists(p):
        tmp=p+'.tmp';f(n/fps).save(tmp,format='PNG');os.replace(tmp,p)
print('done',a,b)

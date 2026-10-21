import json,collections
def load(fn):
    d=json.load(open(fn)); return d
def cubes(d): return {(x,y-200,z):b for x,y,z,b in d['edits']['cubes']}
def analyze(d):
    G=cubes(d)
    ring=[(x,z) for (x,y,z),b in G.items() if y==10 and b!=0]
    xs=[a for a,b in ring]; zs=[b for a,b in ring]
    x0,x1,z0,z1=min(xs),max(xs),min(zs),max(zs)
    A=(x1-x0+1)*(z1-z0+1)
    cnt=collections.Counter(); 
    ext={}
    for (x,y,z),b in G.items():
        if b==0: continue
        if x0<=x<=x1 and z0<=z<=z1: cnt[y]+=1
        e=ext.setdefault(y,[x,x,z,z]); e[0]=min(e[0],x);e[1]=max(e[1],x);e[2]=min(e[2],z);e[3]=max(e[3],z)
    roof=None
    for y in range(8,max(ext)+1):
        if y in ext and (ext[y][0]<x0 or ext[y][1]>x1 or ext[y][2]<z0 or ext[y][3]>z1) and y>=12:
            roof=y;break
    slabs=[]
    ys=[y for y in range(2,(roof or 40)) if cnt[y]>=0.5*A]
    # group consecutive
    grp=[]
    for y in ys:
        if grp and y==grp[-1][-1]+1: grp[-1].append(y)
        else: grp.append([y])
    slabs=[g[-1] for g in grp]
    return dict(G=G,x0=x0,x1=x1,z0=z0,z1=z1,roof=roof,slabs=slabs,A=A,cnt=cnt)
if __name__=='__main__':
    import glob,sys
    for fn in sorted(glob.glob('/home/claude/FT/catalogo/estructuras/*.json')):
        if 'ejemplo' in fn: continue
        d=load(fn); a=analyze(d)
        print(fn.split('/')[-1],(a['x0'],a['x1'],a['z0'],a['z1']),'roof',a['roof'],'slabs',a['slabs'])

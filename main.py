import json,os,random,sys,urllib.request
V=[0,100,320,330,500,900,0]
N=[-33,-31,-18,-14,14,18,31,33]
K=[-17,-16,-15,-1,1,15,16,17]
B=[-17,-15,15,17]
R=[-16,-1,1,16]
Q=B+R
_r=random.Random(7)
Z=[_r.getrandbits(64) for _ in range(1700)]
TT={}
KL=[[0,0] for _ in range(128)]
BD=30000
MT=100000
ND=0
PH=[]
ST=[]
b=[0]*128
s=1
c=0
e=-1
w=0
h=0
WK=4
BK=116
NP=0
PW=0
def pi(p):
 return (abs(p)-1)*2+(p<0)
def P(fen):
 global b,s,c,e,w,h,WK,BK,NP,PW
 q=fen.split();b=[0]*128
 M={'P':1,'N':2,'B':3,'R':4,'Q':5,'K':6,'p':-1,'n':-2,'b':-3,'r':-4,'q':-5,'k':-6}
 for r,row in enumerate(q[0].split('/')):
  x=(7-r)*16
  for ch in row:
   if ch.isdigit(): x+=int(ch)
   else: b[x]=M[ch];x+=1
 s=1 if q[1]=='w' else -1
 c=0
 for ch in q[2]:
  if ch=='K': c|=1
  elif ch=='Q': c|=2
  elif ch=='k': c|=4
  elif ch=='q': c|=8
 e=-1
 if q[3]!='-': e=ord(q[3][0])-97+(int(q[3][1])-1)*16
 w=int(q[4]) if len(q)>4 else 0
 h=0;WK=4;BK=116;NP=0;PW=0
 for x in range(128):
  if x&136: continue
  p=b[x]
  if not p: continue
  h^=Z[pi(p)*128+x]
  t=abs(p)
  if t==6:
   if p>0: WK=x
   else: BK=x
  elif t==1: PW+=1
  else: NP+=V[t]
 if s<0: h^=Z[1560]
 h^=Z[1536+c]
 if e>=0: h^=Z[1552+(e&7)]
def A(x,by):
 for d in ((-15,-17) if by>0 else (15,17)):
  t=x+d
  if not t&136 and b[t]==by: return 1
 for d in N:
  t=x+d
  if not t&136 and b[t]==2*by: return 1
 for d in K:
  t=x+d
  if not t&136 and b[t]==6*by: return 1
 for d in B:
  t=x+d
  while not t&136:
   p=b[t]
   if p:
    if p==3*by or p==5*by: return 1
    break
   t+=d
 for d in R:
  t=x+d
  while not t&136:
   p=b[t]
   if p:
    if p==4*by or p==5*by: return 1
    break
   t+=d
 return 0
def G(cp):
 ms=[]
 for x in range(128):
  if x&136: continue
  p=b[x]
  if not p or (p>0)!=(s>0): continue
  t=abs(p)
  if t==1:
   d=16 if s>0 else -16
   y=x+d
   if not y&136 and not b[y]:
    pm(x,y,0,cp,ms)
    y2=x+2*d
    if ((x>>4)==1 and s>0 or (x>>4)==6 and s<0) and not b[y2]: ms.append(x|(y2<<7))
   for dd in (d-1,d+1):
    y=x+dd
    if y&136: continue
    if b[y] and (b[y]>0)!=(s>0): pm(x,y,1,cp,ms)
    elif y==e and not b[y]: ms.append(x|(y<<7))
  elif t==2 or t==6:
   for d in (N if t==2 else K):
    y=x+d
    if y&136: continue
    if not b[y]:
     if not cp: ms.append(x|(y<<7))
    elif (b[y]>0)!=(s>0): ms.append(x|(y<<7))
   if t==6 and not cp: cast(x,ms)
  else:
   for d in (B if t==3 else R if t==4 else Q):
    y=x+d
    while not y&136:
     if b[y]:
      if (b[y]>0)!=(s>0): ms.append(x|(y<<7))
      break
     if not cp: ms.append(x|(y<<7))
     y+=d
 return ms
def pm(x,y,cap,cp,ms):
 if (y>>4)==(7 if s>0 else 0):
  if cap or not cp:
   for pr in (5,4,3,2): ms.append(x|(y<<7)|(pr<<14))
 elif cap or not cp: ms.append(x|(y<<7))
def cast(x,ms):
 if s>0:
  if c&1 and not b[5] and not b[6] and b[7]==4 and not A(4,-1) and not A(5,-1) and not A(6,-1): ms.append(4|(6<<7))
  if c&2 and not b[1] and not b[2] and not b[3] and b[0]==4 and not A(4,-1) and not A(3,-1) and not A(2,-1): ms.append(4|(2<<7))
 else:
  if c&4 and not b[117] and not b[118] and b[119]==-4 and not A(116,1) and not A(117,1) and not A(118,1): ms.append(116|(118<<7))
  if c&8 and not b[113] and not b[114] and not b[115] and b[112]==-4 and not A(116,1) and not A(115,1) and not A(114,1): ms.append(116|(114<<7))
def M(m):
 global s,c,e,w,h,WK,BK,NP,PW
 x=m&127;y=(m>>7)&127;pr=(m>>14)&7
 p=b[x];cap=b[y];epc=-1
 if abs(p)==1 and y==e and not cap:
  epc=y-(16 if s>0 else -16);cap=b[epc]
 ST.append((m,cap,epc,c,e,h,WK,BK,NP,PW,w))
 h^=Z[pi(p)*128+x]
 if cap: h^=Z[pi(cap)*128+(epc if epc>=0 else y)]
 nc=c
 if abs(p)==6: nc&=~(3 if s>0 else 12)
 if x==0 or y==0: nc&=~2
 if x==7 or y==7: nc&=~1
 if x==112 or y==112: nc&=~8
 if x==119 or y==119: nc&=~4
 if nc!=c: h^=Z[1536+c]^Z[1536+nc];c=nc
 if e>=0: h^=Z[1552+(e&7)]
 e=-1
 if abs(p)==1 and abs(y-x)==32: e=(x+y)//2;h^=Z[1552+(e&7)]
 b[x]=0
 np2=pr if pr else abs(p)
 b[y]=np2 if s>0 else -np2
 h^=Z[pi(b[y])*128+y]
 if epc>=0: b[epc]=0
 if abs(p)==6 and abs(y-x)==2:
  if y==6: b[7]=0;b[5]=4;h^=Z[pi(4)*128+7]^Z[pi(4)*128+5]
  elif y==2: b[0]=0;b[3]=4;h^=Z[pi(4)*128+0]^Z[pi(4)*128+3]
  elif y==118: b[119]=0;b[117]=-4;h^=Z[pi(-4)*128+119]^Z[pi(-4)*128+117]
  elif y==114: b[112]=0;b[115]=-4;h^=Z[pi(-4)*128+112]^Z[pi(-4)*128+115]
 if abs(p)==6:
  if s>0: WK=y
  else: BK=y
 if cap:
  if abs(cap)==1: PW-=1
  else: NP-=V[abs(cap)]
 if pr: PW-=1;NP+=V[pr]
 w=0 if abs(p)==1 or cap else w+1
 h^=Z[1560];s=-s
def U():
 global s,c,e,w,h,WK,BK,NP,PW
 m,cap,epc,oc,oe,oh,owk,obk,onp,opw,ow=ST.pop()
 x=m&127;y=(m>>7)&127;pr=(m>>14)&7
 s=-s
 p=(1 if s>0 else -1) if pr else b[y]
 b[x]=p
 b[y]=cap if epc<0 else 0
 if epc>=0: b[epc]=cap
 if abs(p)==6 and abs(y-x)==2:
  if y==6: b[7]=4;b[5]=0
  elif y==2: b[0]=4;b[3]=0
  elif y==118: b[119]=-4;b[117]=0
  elif y==114: b[112]=-4;b[115]=0
 c,e,h,WK,BK,NP,PW,w=oc,oe,oh,owk,obk,onp,opw,ow
def E():
 sc=0;kw=0;kb=0;wb=0;bb=0
 for x in range(128):
  if x&136: continue
  p=b[x]
  if not p: continue
  t=abs(p);f=x&7;r=x>>4
  if p>0: rr=r
  else: rr=7-r
  cc=min(f,7-f)+min(rr,7-rr)
  if t==6:
   if p>0: kw=rr*8+f
   else: kb=rr*8+f
   continue
  v=V[t]
  if t==1: v+=[0,0,4,9,16,26,44,0][rr]+([0,0,0,8,12,10,6,0][rr] if f in (3,4) else 0)
  elif t==2: v+=6*cc-20
  elif t==3:
   v+=4*cc-10
   if p>0: wb+=1
   else: bb+=1
  elif t==4: v+=18 if rr==6 else 0
  elif t==5: v+=2*cc-8
  sc+=v if p>0 else -v
 if wb>=2: sc+=30
 if bb>=2: sc-=30
 ph=min(NP,6400)
 sc+=kg(kw,ph)-kg(kb,ph)
 return sc*s
def kg(rel,ph):
 f=rel&7;r=rel>>4;cc=min(f,7-f)+min(r,7-r)
 o=[18,24,8,0,0,8,24,18][f] if r==0 else max(-40,-12*r)
 return (o*ph+(8*cc-24)*(6400-ph))//6400
class AB(Exception): pass
def OS(m,tt,ply):
 if m==tt: return 1000000
 y=(m>>7)&127;cap=b[y];v=0
 if cap: v=100000+10*V[abs(cap)]-V[abs(b[m&127])]//10
 if (m>>14)&7: v+=90000+V[(m>>14)&7]
 if m==KL[ply][0]: v+=50000
 elif m==KL[ply][1]: v+=40000
 return v
def QS(a,be,ply):
 global ND
 ND+=1
 if ND>BD: raise AB
 if w>=100: return 0
 if PW==0 and NP<=330: return 0
 en=TT.get(h)
 if en:
  sc=en[1]
  if sc>99000: sc-=ply
  elif sc<-99000: sc+=ply
  if en[2]==1: return sc
  if en[2]==2 and sc>=be: return be
  if en[2]==3 and sc<=a: return a
 ao=a
 st=E()
 if st>=be:
  TT[h]=(0,st,2,0)
  return be
 if st>a: a=st
 mv=s
 ck=A(WK if s>0 else BK,-s)
 ms=G(ck==0)
 ms.sort(key=lambda m:-OS(m,0,ply))
 lg=0
 for m in ms:
  if not ck:
   y=(m>>7)&127;cap=b[y]
   if not cap: cap=1
   gn=V[abs(cap)]+ (V[(m>>14)&7]-100 if (m>>14)&7 else 0)
   if st+gn+200<a: continue
  M(m)
  if A(WK if mv>0 else BK,s):
   U();continue
  lg=1
  if h in PH: v=0
  else:
   PH.append(h);v=-QS(-be,-a,ply+1);PH.pop()
  U()
  if v>=be:
   sc=v
   if sc>99000: sc+=ply
   elif sc<-99000: sc-=ply
   TT[h]=(0,sc,2,0)
   return be
  if v>a: a=v
 if ck and not lg: return -MT+ply
 sc=a
 if sc>99000: sc+=ply
 elif sc<-99000: sc-=ply
 TT[h]=(0,sc,1 if a>ao else 3,0)
 return a
def SR(a,be,d,ply):
 global ND
 ND+=1
 if ND>BD: raise AB
 if w>=100: return 0
 if PW==0 and NP<=330: return 0
 if d<=0: return QS(a,be,ply)
 en=TT.get(h);tm=0
 if en and en[0]>=d:
  sc=en[1]
  if sc>99000: sc-=ply
  elif sc<-99000: sc+=ply
  if en[2]==1: return sc
  if en[2]==2 and sc>=be: return be
  if en[2]==3 and sc<=a: return a
  tm=en[3]
 ck=A(WK if s>0 else BK,-s)
 ms=G(False)
 ms.sort(key=lambda m:-OS(m,tm,ply))
 ao=a;best=-MT*2;bm=0;fl=3;mv=s;lg=0;fi=1
 for m in ms:
  M(m)
  if A(WK if mv>0 else BK,s):
   U();continue
  lg=1
  if h in PH: v=0
  else:
   PH.append(h)
   if fi: v=-SR(-be,-a,d-1,ply+1)
   else:
    v=-SR(-a-1,-a,d-1,ply+1)
    if a<v<be: v=-SR(-be,-a,d-1,ply+1)
   PH.pop()
  fi=0
  U()
  if v>best: best=v;bm=m
  if v>a: a=v
  if a>=be:
   fl=2
   if not b[(m>>7)&127] and not (m>>14)&7:
    KL[ply][1]=KL[ply][0];KL[ply][0]=m
   break
 if not lg: return -MT+ply if ck else 0
 if fl==3 and best>ao: fl=1
 sc=best
 if sc>99000: sc+=ply
 elif sc<-99000: sc-=ply
 TT[h]=(d,sc,fl,bm)
 return best
def u2m(u):
 x=ord(u[0])-97+(int(u[1])-1)*16
 y=ord(u[2])-97+(int(u[3])-1)*16
 pr=0
 if len(u)==5: pr={'q':5,'r':4,'b':3,'n':2}[u[4]]
 return x|(y<<7)|(pr<<14)
def T(legal):
 global ND,PH
 if len(legal)==1: return legal[0]
 ms=[u2m(u) for u in legal]
 sc={};best=ms[0];ND=0;PH=[h]
 for d in range(1,11):
  try:
   bv=-MT*2;cb=best
   for i,m in enumerate(ms):
    M(m)
    if h in PH: v=0
    else:
     PH.append(h)
     if i==0: v=-SR(-MT,MT,d-1,1)
     else:
      v=-SR(-bv-1,-bv,d-1,1)
      if v>bv: v=-SR(-MT,MT,d-1,1)
     PH.pop()
    U()
    sc[m]=v
    if v>bv: bv=v;cb=m
   best=cb
   ms.sort(key=lambda m:-sc.get(m,0))
  except AB:
   break
 return mu(best)
def mu(m):
 x=m&127;y=(m>>7)&127;pr=(m>>14)&7
 u='abcdefgh'[x&7]+str((x>>4)+1)+'abcdefgh'[y&7]+str((y>>4)+1)
 if pr: u+='nbrq'[pr-2]
 return u
def F(p,bo):
 req=urllib.request.Request(URL+p,data=json.dumps(bo).encode(),headers={'content-type':'application/json'})
 try:
  with urllib.request.urlopen(req) as r: return json.load(r)
 except urllib.error.HTTPError as ex:
  sys.exit(f"{p}: HTTP {ex.code}")
if __name__=='__main__':
 URL=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
 while True:
  g=F('/game',{})
  if g['status']=='done': break
  while g['status']=='your_move':
   P(g['fen'])
   mv=T(g['legal_moves'])
   if mv not in g['legal_moves']: mv=g['legal_moves'][0]
   g=F('/move',{'game':g['game'],'move':mv})
  print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
 print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)

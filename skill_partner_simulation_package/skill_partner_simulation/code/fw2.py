import numpy as np, networkx as nx, pandas as pd
from scipy import stats
from final_matrix import M as M0, FINAL, DOMAIN
K=20; IDX={s:i for i,s in enumerate(FINAL)}
DOMS=['SW','HW','DES','BIZ','NET','MISC']
DIDX={d:[IDX[s] for s in FINAL if DOMAIN[s]==d] for d in DOMS}
ARCH=['CS','EEE','Design','Business','NetSec']
def _w(spec):
    w=np.full(K,0.5); w[IDX['Cooking']]=0.3
    for names,val in spec:
        for s in names: w[IDX[s]]=val
    return w
SW=[s for s in FINAL if DOMAIN[s]=='SW']; HW=[s for s in FINAL if DOMAIN[s]=='HW']; DES=[s for s in FINAL if DOMAIN[s]=='DES']
ARCH_W=np.vstack([
 _w([(SW,6),(["Network Engineering","Cybersecurity"],2),(["UI/UX"],2),(["Project management","Research and development"],1.5)]),
 _w([(HW,6),(["Network Engineering","Cybersecurity"],2),(["Python"],2),(["Research and development"],2)]),
 _w([(DES,6),(["Website development"],2),(["Digital Marketing"],2),(["Creative Writing"],1.5)]),
 _w([(["Project management","Digital Marketing"],6),(["Creative Writing"],3),(["UI/UX","Data Analysis"],1.5)]),
 _w([(["Network Engineering","Cybersecurity"],6),(["Python"],3),(["Website development"],2),(["Embedded Systems"],1.5)])])
ARCH_P=np.array([.30,.25,.20,.15,.10])
DOM_OF=np.array([DOMAIN[s] for s in FINAL])
def gen_structured(n,rng):
    P=np.zeros((n,K)); arch=rng.choice(5,n,p=ARCH_P)
    for i in range(n):
        m=rng.integers(3,7); w=ARCH_W[arch[i]]; idx=rng.choice(K,m,replace=False,p=w/w.sum())
        for k in idx:
            lv=rng.choice([2,3,4,5],p=[.15,.30,.35,.20]) if w[k]>=3 else rng.choice([1,2,3,4],p=[.35,.35,.20,.10])
            P[i,k]=lv/5
    return P,arch
def gen_uniform(n,rng):
    P=np.zeros((n,K))
    for i in range(n):
        m=rng.integers(3,7); idx=rng.choice(K,m,replace=False); P[i,idx]=rng.integers(1,6,m)/5
    dom=np.array([ARCH_ASSIGN[DOM_OF[int(np.argmax(P[i]))]] for i in range(n)]); return P,dom
ARCH_ASSIGN={'SW':0,'HW':1,'DES':2,'BIZ':3,'NET':4,'MISC':3}
# ---- scores
def _z(S): S=S.copy(); np.fill_diagonal(S,0); return S
def sim_ruzicka(P):
    mn=np.minimum(P[:,None,:],P[None,:,:]).sum(2); mx=np.maximum(P[:,None,:],P[None,:,:]).sum(2); return _z(mn/np.maximum(mx,1e-12))
def sim_cosine(P):
    nr=np.linalg.norm(P,axis=1,keepdims=True); return _z((P@P.T)/np.maximum(nr*nr.T,1e-12))
def syn_raw(P,M=M0): return _z(P@M@P.T)
def gap_dir(P,M=M0):
    s=np.max(P[:,:,None]*M[None,:,:],axis=1)      # s_il = max_k p_ik M_kl
    return (s*(1-P))@P.T                           # g[i,j]=sum_l p_jl (1-p_il) s_il
def syn_gap(P,M=M0): g=gap_dir(P,M); return _z((g+g.T)/2)
def csls(S,kappa=5):
    S2=S.copy(); np.fill_diagonal(S2,-np.inf); r=np.sort(S2,axis=1)[:,-kappa:].mean(1)
    out=2*S-r[:,None]-r[None,:]; np.fill_diagonal(out,-np.inf); return out
def rownorm(S):
    S=S.copy(); np.fill_diagonal(S,np.nan); mn=np.nanmin(S,1,keepdims=True); mx=np.nanmax(S,1,keepdims=True)
    return np.nan_to_num((S-mn)/np.maximum(mx-mn,1e-12),nan=-1)
def hybrid(P,lam,M=M0):
    return lam*rownorm(sim_ruzicka(P))+(1-lam)*rownorm(csls(syn_gap(P,M)))
def all_scores(P,rng,M=M0):
    Sr=sim_ruzicka(P); G=syn_gap(P,M)
    return {'Random':rng.random(Sr.shape),'Similarity (weighted Jaccard)':Sr,'Cosine similarity':sim_cosine(P),
     'FSNP original (binary synergy)':syn_raw((P>0).astype(float),M),'Synergy, proficiency-weighted':syn_raw(P,M),
     'Gap-synergy':G,'Gap-synergy + hubness corr.':csls(G),'Hybrid (λ=0.5)':hybrid(P,0.5,M)}
# ---- tasks / eval
def gen_task(i,P,rng,regime):
    own=np.where(P[i]>0)[0]; lead=int(rng.choice(own)); m=rng.integers(3,7); req={lead:rng.choice([3,4,5])/5}
    ld=DIDX[DOM_OF[lead]] if DOM_OF[lead]!='MISC' else list(range(K))
    while len(req)<m:
        k=int(rng.choice(ld)) if (regime=='coherent' and rng.random()<0.6) else int(rng.integers(K))
        if k not in req: req[k]=rng.choice([3,4,5])/5
    r=np.zeros(K)
    for k,v in req.items(): r[k]=v
    return r
def cov(r,best): return float((r*np.minimum(1,best/np.maximum(r,1e-12))*(r>0)).sum()/r.sum())
def oracle(P,i,r,k):
    team=[i];cur=P[i].copy();out=[];rr=np.maximum(r,1e-12)
    for _ in range(k):
        c=(r*np.minimum(1,np.maximum(cur,P)/rr)).sum(1)/r.sum(); c[team]=-1; j=int(np.argmax(c)); out.append(j);team.append(j);cur=np.maximum(cur,P[j])
    return out
def topk(S,i,k):
    s=S[i].copy(); s[i]=-np.inf; return np.argsort(-s)[:k]
def gini(x):
    x=np.sort(np.asarray(x,float)); n=len(x)
    return 0.0 if x.sum()==0 else float((2*np.sum(np.arange(1,n+1)*x)/(n*x.sum()))-(n+1)/n)
def evaluate(P,arch,scores,rng,regime,Q=3,oracle_on=True):
    n=len(P); tasks=[(i,gen_task(i,P,rng,regime)) for i in range(n) for _ in range(Q)]; rows=[]
    items=list(scores.items())+([('Task-aware oracle (upper bound)',None)] if oracle_on else [])
    for name,S in items:
        g1=[];c3=[];red=[];cr=[];ex=np.zeros(n)
        for i,r in tasks:
            rec=oracle(P,i,r,3) if S is None else [int(x) for x in topk(S,i,3)]
            b=cov(r,P[i]); g1.append(cov(r,np.maximum(P[i],P[rec[0]]))-b); c3.append(cov(r,np.max(P[[i]+rec],0)))
            j=rec[0]; red.append(np.minimum(P[i],P[j]).sum()/max(np.maximum(P[i],P[j]).sum(),1e-12))
            cr.append(np.mean([arch[x]!=arch[i] for x in rec]))
            for x in rec: ex[x]+=1
        rows.append(dict(method=name,Gain1=np.mean(g1),Cov3=np.mean(c3),Red=np.mean(red),Cross=np.mean(cr),CatCov=np.mean(ex>0),Gini=gini(ex)))
    return rows
def run(N,regime,R,gen=gen_structured,M=M0,seed0=0,oracle_on=True,Q=3):
    out=[]
    for r in range(R):
        rng=np.random.default_rng(seed0+r); P,arch=gen(N,rng); sc=all_scores(P,rng,M)
        for row in evaluate(P,arch,sc,rng,regime,Q,oracle_on): row['rep']=r; out.append(row)
    return pd.DataFrame(out)
def ci(x):
    x=np.asarray(x,float); return stats.t.ppf(.975,len(x)-1)*x.std(ddof=1)/np.sqrt(len(x))
def summarize(df,ref='Similarity (weighted Jaccard)'):
    base=df[df.method==ref].sort_values('rep')['Gain1'].values; rows=[]
    for m,g in df.groupby('method',sort=False):
        d={'method':m}
        for c in ['Gain1','Cov3','Red','Cross','CatCov','Gini']: d[c]=g[c].mean(); d[c+'_ci']=ci(g[c])
        a=g.sort_values('rep')['Gain1'].values
        d['p_vs_sim']=np.nan if m==ref else stats.ttest_rel(a,base).pvalue
        rows.append(d)
    return pd.DataFrame(rows)
# ---- graphs
def knn_graph(S,k,cost_scores=None):
    C=S if cost_scores is None else cost_scores
    n=len(S); G=nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for j in topk(S,i,k): G.add_edge(i,int(j),score=float(max(C[i,j],C[j,i])))
    mx=max([d['score'] for _,_,d in G.edges(data=True)]+[1e-12])
    for u,v,d in G.edges(data=True): d['cost']=1/(d['score']/mx+0.05)   # scale-free cost; eps=0.05
    return G
def graph_metrics(G,arch):
    n=G.number_of_nodes(); comps=list(nx.connected_components(G)); gc=max(comps,key=len); H=G.subgraph(gc)
    deg=np.array([d for _,d in G.degree()]); bet=nx.betweenness_centrality(G,weight='cost'); b=np.array([bet[i] for i in range(n)])
    T=nx.minimum_spanning_tree(H,weight='cost')
    return {'Edges':G.number_of_edges(),'Components':len(comps),'Giant %':100*len(gc)/n,'Avg path (hops)':nx.average_shortest_path_length(H),
            'Clustering':nx.average_clustering(G),'Hubs':int((b>=b.mean()+b.std()).sum()),'Cross-archetype edges %':100*np.mean([arch[u]!=arch[v] for u,v in G.edges]),
            'MST cross-archetype %':100*np.mean([arch[u]!=arch[v] for u,v in T.edges]),'Degree Gini':gini(deg),'MST weight':sum(d['cost'] for *_,d in T.edges(data=True))}

import sys,time,json; sys.path.insert(0,'.')
from fw2 import *
t0=time.time(); T=lambda s:print(f'[{time.time()-t0:6.1f}s] {s}',flush=True)
# 1. main comparison
main={}
for popname,gen in (('structured',gen_structured),('uniform',gen_uniform)):
    for reg in ('random','coherent'):
        df=run(50,reg,100,gen); df['pop']=popname; df['regime']=reg; main[(popname,reg)]=df; df.to_csv(f'out/main_{popname}_{reg}.csv',index=False)
        T(f'main {popname}/{reg}')
pd.concat(main.values()).to_csv('out/main_all.csv',index=False)
# 2. N sweep
rows=[]
for N,R in ((50,100),(100,50),(200,30),(500,8)):
    for reg in ('random','coherent'):
        df=run(N,reg,R,gen_structured,oracle_on=True); s=summarize(df); s['N']=N; s['regime']=reg; rows.append(s); T(f'N={N} {reg}')
pd.concat(rows).to_csv('out/nsweep.csv',index=False)
# 3. M stress tests (structured population, both regimes)
def noisy(M,sig,rng):
    A=np.clip(M+rng.normal(0,sig,M.shape),0.0,1.0); A=(A+A.T)/2; np.fill_diagonal(A,0); return A
def permuted(M,rng):
    iu=np.triu_indices(20,1); v=M[iu].copy(); rng.shuffle(v); A=np.zeros_like(M); A[iu]=v; return A+A.T
def uniformM(): A=np.full((20,20),0.5); np.fill_diagonal(A,0); return A
stress=[]
for reg in ('random','coherent'):
    for label,mk in (('Expert M (σ=0)',lambda r:M0),('Noisy M σ=0.10',lambda r:noisy(M0,0.10,r)),('Noisy M σ=0.20',lambda r:noisy(M0,0.20,r)),('Noisy M σ=0.30',lambda r:noisy(M0,0.30,r)),
                     ('Shuffled M (same values)',lambda r:permuted(M0,r)),('Uniform M (0.5)',lambda r:uniformM())):
        for rep in range(60):
            rng=np.random.default_rng(1000+rep); P,arch=gen_structured(50,rng); Mx=mk(rng)
            sc=all_scores(P,rng,Mx)
            for row in evaluate(P,arch,{k:v for k,v in sc.items() if k in ('Similarity (weighted Jaccard)','FSNP original (binary synergy)','Synergy, proficiency-weighted','Gap-synergy','Gap-synergy + hubness corr.','Random')},rng,reg,3,oracle_on=False):
                row.update(rep=rep,Mlabel=label,regime=reg); stress.append(row)
    T(f'stress {reg}')
pd.DataFrame(stress).to_csv('out/stress.csv',index=False)
# 4. lambda sweep
lam=[]
for reg in ('random','coherent'):
    for l in np.round(np.arange(0,1.01,0.1),1):
        for rep in range(40):
            rng=np.random.default_rng(2000+rep); P,arch=gen_structured(50,rng); S={'h':hybrid(P,l)}
            row=evaluate(P,arch,S,rng,reg,3,oracle_on=False)[0]; row.update(lam=l,rep=rep,regime=reg); lam.append(row)
    T(f'lambda {reg}')
pd.DataFrame(lam).to_csv('out/lambda.csv',index=False)
# 5. graph metrics (k=5, and k sweep)
gm=[]; hubskill=[]
for popname,gen in (('structured',gen_structured),('uniform',gen_uniform)):
    for rep in range(100):
        rng=np.random.default_rng(3000+rep); P,arch=gen(50,rng); sc=all_scores(P,rng)
        for k in (3,5,8):
            for name in ('Similarity (weighted Jaccard)','FSNP original (binary synergy)','Gap-synergy','Gap-synergy + hubness corr.'):
                G=knn_graph(sc[name],k); m=graph_metrics(G,arch); m.update(method=name,k=k,pop=popname,rep=rep); gm.append(m)
        if popname=='structured':
            for name in ('Similarity (weighted Jaccard)','Gap-synergy'):
                G=knn_graph(sc[name],5); bet=nx.betweenness_centrality(G,weight='cost'); b=np.array([bet[i] for i in range(50)]); hub=b>=b.mean()+b.std()
                for i in range(50): hubskill.append(dict(method=name,rep=rep,hub=bool(hub[i]),**{FINAL[k]:float(P[i,k]>0) for k in range(K)}))
pd.DataFrame(gm).to_csv('out/graph.csv',index=False); T('graph')
hs=pd.DataFrame(hubskill); hs.to_csv('out/hubskills.csv',index=False)
T('done')

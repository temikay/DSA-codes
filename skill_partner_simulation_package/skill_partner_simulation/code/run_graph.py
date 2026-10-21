import sys; sys.path.insert(0,'.')
from fw2 import *
import time; t0=time.time()
gm=[]; hubskill=[]
for popname,gen in (('structured',gen_structured),('uniform',gen_uniform)):
    for rep in range(60):
        rng=np.random.default_rng(3000+rep); P,arch=gen(50,rng); sc=all_scores(P,rng)
        for k in (3,5,8):
            for name in ('Similarity (weighted Jaccard)','FSNP original (binary synergy)','Gap-synergy','Gap-synergy + hubness corr.'):
                G=knn_graph(sc[name],k,sc['Gap-synergy'] if 'hubness' in name else None); m=graph_metrics(G,arch); m.update(method=name,k=k,pop=popname,rep=rep); gm.append(m)
        if popname=='structured':
            for name in ('Similarity (weighted Jaccard)','Gap-synergy'):
                G=knn_graph(sc[name],5); bet=nx.betweenness_centrality(G,weight='cost'); b=np.array([bet[i] for i in range(50)]); hub=b>=b.mean()+b.std()
                for i in range(50): hubskill.append(dict(method=name,rep=rep,hub=bool(hub[i]),**{FINAL[k]:float(P[i,k]>0) for k in range(K)}))
    print(popname,time.time()-t0,flush=True)
pd.DataFrame(gm).to_csv('out/graph.csv',index=False); pd.DataFrame(hubskill).to_csv('out/hubskills.csv',index=False); print('done')

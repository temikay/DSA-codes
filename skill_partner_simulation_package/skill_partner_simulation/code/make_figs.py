import sys; sys.path.insert(0,'.')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patches as mp
from fw2 import *
plt.rcParams.update({'font.family':'serif','font.serif':['Liberation Serif','Times New Roman','DejaVu Serif'],'font.size':8,'axes.linewidth':0.6,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':300})
SHORT={'Random':'Random','Similarity (weighted Jaccard)':'Jaccard','Cosine similarity':'Cosine','FSNP original (binary synergy)':'FSNP-orig.','Synergy, proficiency-weighted':'Synergy-prof.','Gap-synergy':'Gap-synergy','Gap-synergy + hubness corr.':'Gap-syn.+HC','Hybrid (λ=0.5)':'Hybrid','Task-aware oracle (upper bound)':'Oracle'}
ORDER=list(SHORT)
GREY='#9a9a9a'; BLUE='#1f4e79'; ORG='#c55a11'; GRN='#548235'
def col(m): return {'Random':GREY,'Similarity (weighted Jaccard)':'#c9c9c9','Cosine similarity':'#c9c9c9','FSNP original (binary synergy)':'#9dc3e6','Synergy, proficiency-weighted':'#9dc3e6','Gap-synergy':BLUE,'Gap-synergy + hubness corr.':'#2e75b6','Hybrid (λ=0.5)':'#f4b183','Task-aware oracle (upper bound)':'#ffffff'}[m]
main=pd.read_csv('out/main_all.csv'); s=main[main['pop']=='structured']
S={reg:summarize(s[s.regime==reg]).set_index('method') for reg in ('coherent','random')}

# ---------- Fig 1 framework overview
fig,ax=plt.subplots(figsize=(6.5,2.3)); ax.axis('off'); ax.set_xlim(0,100); ax.set_ylim(0,34)
def box(x,y,w,h,t,fc='#eaf1f8',ec=BLUE,fs=7):
    ax.add_patch(mp.FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.3,rounding_size=1.2',fc=fc,ec=ec,lw=0.8)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,linespacing=1.25)
def arr(x1,y1,x2,y2): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',lw=0.8,color='#333'))
box(1,20,19,11,'Student profiles\n$p_i\\in[0,1]^{K}$\n(proficiency 1–5 → ℓ/5)'); box(1,3,19,11,'Skill-synergy matrix\n$M\\in[0,1]^{K\\times K}$\n(symmetric, $M_{kk}=0$)')
box(27,20,21,11,'Similarity score\n$\\sigma_{ij}$ (weighted Jaccard)\ngives homophily graph $G_S$',fc='#f2f2f2',ec='#666'); box(27,3,21,11,'Gap-synergy score\n$\\gamma_{ij}$ (+ hubness correction)\ngives complementarity graph $G_C$')
box(55,11.5,19,11,'Graph algorithms\nDijkstra · Kruskal MST\nbetweenness hubs'); box(81,11.5,18,11,'Recommendations\ntop-$k$ partners · paths\nteam assembly',fc='#e2efd9',ec=GRN)
arr(20,25.5,27,25.5);arr(20,8.5,27,8.5);arr(20,22,27,10);arr(48,25.5,55,19);arr(48,8.5,55,15);arr(74,17,81,17)
ax.text(50,0.3,'k-NN construction (k=5) gives both graphs equal density; edge cost $c_{ij}=1/(\\tilde{s}_{ij}+\\varepsilon)$',ha='center',fontsize=6.5,style='italic')
fig.savefig('figs/fig1_framework.png',bbox_inches='tight'); plt.close()

# ---------- Fig 2 heatmap (domain-sorted)
order=[i for d in ['SW','HW','DES','BIZ','NET','MISC'] for i in range(K) if DOM_OF[i]==d]
bounds=np.cumsum([sum(DOM_OF[i]==d for i in range(K)) for d in ['SW','HW','DES','BIZ','NET','MISC']])
fig,ax=plt.subplots(figsize=(4.6,4.2)); Ms=M0[np.ix_(order,order)]
im=ax.imshow(Ms,cmap='Blues',vmin=0,vmax=1)
ax.set_xticks(range(K)); ax.set_yticks(range(K)); lab=[f'S{i} {FINAL[i]}' for i in order]
ax.set_xticklabels(lab,rotation=90,fontsize=5.2); ax.set_yticklabels(lab,fontsize=5.2)
for b in bounds[:-1]: ax.axhline(b-.5,color='k',lw=.6); ax.axvline(b-.5,color='k',lw=.6)
for spine in ax.spines.values(): spine.set_visible(True)
cb=fig.colorbar(im,ax=ax,fraction=0.046,pad=0.03); cb.ax.tick_params(labelsize=6); cb.set_label('synergy $M_{kl}$',fontsize=7)
fig.savefig('figs/fig2_matrix.png',bbox_inches='tight'); plt.close()

# ---------- Fig 3 main results (3 panels)
meths=[m for m in ORDER if m!='Task-aware oracle (upper bound)']
fig,axs=plt.subplots(1,3,figsize=(6.5,2.7)); y=np.arange(len(meths))
for k,(ax,metric,title) in enumerate(zip(axs,['Gain1','Red','CatCov'],['(a) Coverage gain @1 ↑','(b) Redundancy @1 ↓','(c) Students ever recommended ↑'])):
    h=0.38
    if metric=='Gain1':
        for off,reg,hatch in ((-h/2,'coherent',None),(h/2,'random','///')):
            v=[S[reg].loc[m,metric] for m in meths]; e=[S[reg].loc[m,metric+'_ci'] for m in meths]
            ax.barh(y+off,v,h,xerr=e,color=[col(m) for m in meths],edgecolor='k',lw=0.4,hatch=hatch,error_kw=dict(lw=0.6))
        ax.axvline(S['coherent'].loc['Task-aware oracle (upper bound)','Gain1'],color='k',ls='--',lw=0.6); ax.text(0.40,7.6,'oracle 0.41',fontsize=6,ha='right',va='center')
    else:
        v=[S['coherent'].loc[m,metric] for m in meths]; e=[S['coherent'].loc[m,metric+'_ci'] for m in meths]
        ax.barh(y,v,0.6,xerr=e,color=[col(m) for m in meths],edgecolor='k',lw=0.4,error_kw=dict(lw=0.6))
    ax.set_yticks(y); ax.set_yticklabels([SHORT[m] for m in meths] if k==0 else []); ax.invert_yaxis(); ax.set_title(title,fontsize=7.5,loc='left'); ax.tick_params(labelsize=6.5)
axs[0].legend(handles=[mp.Patch(fc='w',ec='k',lw=.4,label='Domain-coherent tasks'),mp.Patch(fc='w',ec='k',lw=.4,hatch='///',label='Random tasks')],fontsize=6,frameon=False,loc='center right',bbox_to_anchor=(1.0,0.35))
fig.tight_layout(); fig.savefig('figs/fig3_main.png',bbox_inches='tight'); plt.close()

# ---------- Fig 4 networks (one replicate)
rng=np.random.default_rng(3000); P,arch=gen_structured(50,rng); sc=all_scores(P,rng)
GG=[('(a) Homophily graph $G_S$ (weighted Jaccard)',knn_graph(sc['Similarity (weighted Jaccard)'],5)),
    ('(b) Complementarity graph $G_C$ (gap-synergy)',knn_graph(sc['Gap-synergy'],5)),
    ('(c) $G_C$ with hubness correction',knn_graph(sc['Gap-synergy + hubness corr.'],5,sc['Gap-synergy']))]
colors=['#1f77b4','#d95f02','#1b9e77','#7570b3','#e6ab02']; marks=['o','s','^','D','v']
pos=nx.spring_layout(GG[0][1],seed=4,k=0.35,weight=None)
fig,axs=plt.subplots(1,3,figsize=(6.5,2.5))
for ax,(t,G) in zip(axs,GG):
    pos=nx.spring_layout(G,seed=7,k=0.5)
    nx.draw_networkx_edges(G,pos,ax=ax,width=0.4,edge_color='#999',alpha=.7)
    for a in range(5):
        nodes=[i for i in range(50) if arch[i]==a]; nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_color=colors[a],node_shape=marks[a],node_size=26,ax=ax,linewidths=0.3,edgecolors='k')
    m=graph_metrics(G,arch); ax.set_title(t,fontsize=6.8); ax.text(0.5,-0.08,f"{m['Cross-archetype edges %']:.0f}% cross-archetype edges · avg path {m['Avg path (hops)']:.2f} · {m['Hubs']} hubs",transform=ax.transAxes,ha='center',fontsize=6)
    ax.axis('off')
fig.legend(handles=[plt.Line2D([],[],marker=marks[a],color='w',markerfacecolor=colors[a],markeredgecolor='k',markersize=5,label=ARCH[a]) for a in range(5)],loc='lower center',ncol=5,fontsize=6.5,frameon=False,bbox_to_anchor=(0.5,-0.05))
fig.savefig('figs/fig4_networks.png',bbox_inches='tight'); plt.close()

# ---------- Fig 5 sensitivity
st=pd.read_csv('out/stress.csv'); lam=pd.read_csv('out/lambda.csv'); ns=pd.read_csv('out/nsweep.csv')
fig,axs=plt.subplots(1,3,figsize=(6.5,2.5))
ax=axs[0]; labs=['Expert M','σ=0.1','σ=0.2','σ=0.3','Shuffled','Uniform']; keys=['Expert M (σ=0)','Noisy M σ=0.10','Noisy M σ=0.20','Noisy M σ=0.30','Shuffled M (same values)','Uniform M (0.5)']
for off,reg,hatch in ((-0.2,'coherent',None),(0.2,'random','///')):
    d=st[(st.regime==reg)&(st.method=='Gap-synergy')].groupby('Mlabel')['Gain1']; v=[d.mean()[k] for k in keys]; e=[ci(st[(st.regime==reg)&(st.method=='Gap-synergy')&(st.Mlabel==k)].Gain1) for k in keys]
    ax.bar(np.arange(6)+off,v,0.38,yerr=e,color=BLUE,hatch=hatch,edgecolor='k',lw=.4,error_kw=dict(lw=.6))
for reg,ls in (('coherent','-'),):
    ax.axhline(st[(st.regime==reg)&(st.method=='Similarity (weighted Jaccard)')].Gain1.mean(),color='#555',ls='--',lw=.7); ax.axhline(st[(st.regime==reg)&(st.method=='Random')].Gain1.mean(),color=GREY,ls=':',lw=.8)
ax.set_xticks(range(6)); ax.set_xticklabels(labs,rotation=40,ha='right',fontsize=6); ax.set_ylabel('Coverage gain @1'); ax.set_title('(a) Perturbing $M$',fontsize=7.5,loc='left')
ax.legend(handles=[mp.Patch(fc=BLUE,ec='k',lw=.4,label='Coherent tasks'),mp.Patch(fc=BLUE,ec='k',lw=.4,hatch='///',label='Random tasks')],fontsize=5.5,frameon=False,loc='upper right',bbox_to_anchor=(1,1.02))
ax.set_ylim(0,0.23)
ax=axs[1]; L=lam[lam.regime=='coherent'].groupby('lam')[['Gain1','Red']].mean()
ax.plot(L.index,L.Gain1,'o-',color=BLUE,ms=3,lw=1,label='Coverage gain @1'); ax.set_xlabel('λ (weight on similarity)'); ax.set_ylabel('Coverage gain @1',color=BLUE)
ax2=ax.twinx(); ax2.spines['right'].set_visible(True); ax2.plot(L.index,L.Red,'s--',color=ORG,ms=3,lw=1); ax2.set_ylabel('Redundancy @1',color=ORG); ax.set_title('(b) Hybrid trade-off',fontsize=7.5,loc='left')
ax=axs[2]; nsc=ns[ns.regime=='coherent']
for m,st_,c in (('Similarity (weighted Jaccard)','o-','#888'),('FSNP original (binary synergy)','s-','#9dc3e6'),('Gap-synergy','^-',BLUE),('Gap-synergy + hubness corr.','v-','#2e75b6'),('Random','x:',GREY)):
    d=nsc[nsc.method==m].sort_values('N'); ax.plot(d.N,d.Gain1,st_,color=c,ms=3.5,lw=1,label=SHORT[m])
ax.set_xscale('log'); ax.set_xticks([50,100,200,500]); ax.set_xticklabels([50,100,200,500]); ax.set_xlabel('Number of students $N$'); ax.set_ylabel('Coverage gain @1'); ax.set_title('(c) Scalability',fontsize=7.5,loc='left'); ax.set_ylim(0.035,0.245); ax.legend(fontsize=5.2,frameon=False,loc='upper center',ncol=3,columnspacing=0.8,handlelength=1.4)
for a in axs: a.tick_params(labelsize=6.5)
fig.tight_layout(); fig.savefig('figs/fig5_sensitivity.png',bbox_inches='tight'); plt.close()
print('figs done')

import numpy as np
from math import log, sqrt

def DecoyComparison(a,b,detla,Detla):

    return

def DirectComparison(a,b,detla,epsilon):
    p_ab=0
    n=0
    I_ab=1
    while not (I_ab<epsilon or p_ab/(n+1e-6)+I_ab<0.5 or p_ab/(n+1e-6)-I_ab>0.5):
        p_ab+=np.random.binomial(n=1, p=pref_mat[a][b], size=1) # p is the potential probability of a beats b
        n+=1
        I_ab=min(sqrt(log(N*K**2/detla)/(2*n)),1)

    return 0 if I_ab<epsilon else 1 if p_ab/n-I_ab>0.5 else -1

def USBRoutine(S_t,epsilon_t,detla_t,dueling):
    idx = np.random.randint(len(S_t))
    P_hat = [S_t[idx]]
    S_t = list(S_t)
    S_t.pop(idx)
    # S_t=np.array(S_t)
    print('------------------')
    for c in S_t:
        ori_incom=len(S_t)
        ori_domina = len(S_t)
        epsilon_indis=[]
        for c_ in P_hat:
            print('dueling on:','(',c,c_,')')
            v=dueling(c,c_,detla_t/len(S_t)**2,epsilon_t)
            # v=0,incomparability; v=1,c domainanted c_ ;v=-1,c_ domainanted c
            epsilon_indis.append(v)
        if sum(epsilon_indis)==len(P_hat):
            idx=np.random.randint(len(S_t))
            P_hat=[S_t[idx]]
            S_t.pop(idx)
        elif len(np.where(np.array(epsilon_indis)==0)[0])==len(P_hat):
            P_hat.append(c)
            S_t.pop(np.where(np.array(S_t)==c)[0][0])
            ori_incom-=1
        elif len(np.where(np.array(epsilon_indis)==-1)[0])==len(P_hat):
            ori_domina-=1

    return [P_hat,True] if ori_incom==0 or ori_domina==0 else [P_hat,False]

# dataset = "./datasets/5_real"
# dataset = "./datasets/10_real"
dataset = "./datasets/10_art"
with open(dataset+".npy", 'rb') as f:
    pref_mat = np.load(f)

K=len(pref_mat)
for i in range(K):
    print(i,' ',np.mean(pref_mat[i]))

N=28
Delta=0.001
Epsilon=0.05
S={}
S[0]=np.arange(K)
for t in range(N):
    canad_pareto=USBRoutine(S[t],Epsilon/(t+1),Delta/N,DirectComparison)
    S[t + 1]=canad_pareto[0]
    if len(S[t+1]) < 2 or canad_pareto[1]:
        pareto_front=S[t+1]
        break
print('the pareto front set is :', pareto_front)


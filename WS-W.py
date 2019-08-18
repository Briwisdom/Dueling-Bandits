import numpy as np
import random
class WS_W():
    def __init__(self):
        self.K=len(pref_mat)
        self.Ct=np.zeros((T,self.K))
        self.Ipre=None
        self.Jpre=None
        self.winner=None
        self.loser=None
        # self.Utility=np.zeros(self.K,self.K)
        # for arm in range(self.K):
        #     self.Utility[arm, arm] = 0.5

    def find_IJ(self,t):
        if t==0:
            It = np.random.randint(self.K)
            Jt=It
            while Jt==It:
                Jt = np.random.randint(self.K)
            self.Ipre,self.Jpre=It,Jt
            return It,Jt
        maxValue=max(self.Ct[t-1])
        maxArr=np.where(self.Ct[t-1]==maxValue)[0]
        if self.Ipre in maxArr:
            It=self.Ipre
        elif self.Jpre in maxArr:
            It=self.Jpre
        else:
            It=random.choice(maxArr)
        # choose Jt
        CCt=list(self.Ct[t-1])
        CCt[It]=-t-1
        maxValue1 = max(CCt)
        maxArr1 = np.where(CCt == maxValue1)[0]
        if self.Jpre in maxArr1:
            Jt = self.Jpre
        elif self.Ipre in maxArr1:
            Jt = self.Ipre
        else:
            Jt = random.choice(maxArr1)

        self.Ipre,self.Jpre=It,Jt
        return It,Jt

    def pull(self, It, Jt):
        res = np.random.binomial(n=1, p=pref_mat[int(It)][int(Jt)], size=1)
        if res == 1:
            self.winner, self.loser = It, Jt
        else:
            self.winner, self.loser = Jt, It
        return
    def update_Ct(self):
        if t==0:
            self.Ct[t, self.winner] = 1
            self.Ct[t, self.loser] = -1
        else:
            for i in range(self.K):
                if i==self.winner:
                    self.Ct[t,self.winner] = self.Ct[t - 1, self.winner] + 1
                elif i == self.loser:
                    self.Ct[t, self.loser] = self.Ct[t - 1, self.loser] - 1
                else:
                    self.Ct[t, i] = self.Ct[t - 1, i]
        return

    def compute_regret(self,option):
        if option=="weak":
            return pref_mat[best_arm][It]-max(self.Utility[It][Jt],self.Utility[Jt][It])
        else:
            return pref_mat[best_arm][It]-(self.Utility[It][Jt]+self.Utility[Jt][It])/2


# dataset = "./datasets/10_real"
# best_arm = 7

dataset = "./datasets/5_real"
best_arm = 0
with open(dataset+".npy", 'rb') as f:
    pref_mat = np.load(f)

T=1000
ws=WS_W()
last_winner=[]
for t in range(T):
    It,Jt=ws.find_IJ(t)
    ws.pull(It,Jt)
    ws.update_Ct()
    last_winner.append(ws.winner)
print(last_winner[-1])



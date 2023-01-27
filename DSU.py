class DSU:
    def __init__(self,val):
        self.val = val
        self.parent = [i for i in range(val)]
        self.rank = [0]*val


    def union(self,a,b):
        a = self.fparent(a)
        b = self.fparent(b)
        if a==b:
            return
        if self.rank[a]<self.rank[b]:
            self.parent[b] = a
            self.rank[a]+=1
        else:
            self.parent[a] = b
            self.rank[b]+=1
    
    def fparent(self,a):
        while self.parent[a]!=a:
            a = self.parent[a]
        return a

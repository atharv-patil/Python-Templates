par = {}
rank = {}

def ins(n1):
    if n1 not in par:
        par[n1] = n1
        rank[n1] = 1

def find(n1):
    while n1 != par[n1]:
        par[n1] = par[par[n1]]
        n1 = par[n1]
    return n1

def union(n1, n2):
    p1, p2 = find(n1), find(n2)
    if p1 == p2:
        return 0
    if rank[p1] < rank[p2]:
        p1, p2 = p2, p1
    par[p2] = p1
    rank[p1] += rank[p2]
    return 1

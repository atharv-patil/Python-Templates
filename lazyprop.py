class Solution:
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        from sortedcontainers import SortedList
        
        class SEG:
            def __init__(self, n):
                self.n = n
                self.tree = [0] * 2 * self.n

            def query(self, l, r): ## interval [l,r)
                l += self.n
                r += self.n
                ans = 0
                while l < r:
                    if l & 1:
                        ans = max(ans, self.tree[l])
                        l += 1
                    if r & 1:
                        r -= 1
                        ans = max(ans, self.tree[r])
                    l >>= 1
                    r >>= 1
                return ans

            def update(self, i, val):
                i += self.n
                self.tree[i] = val
                while i > 1:
                    i >>= 1
                    self.tree[i] = max(self.tree[i * 2], self.tree[i * 2 + 1])
                    
        max_value = max([x[1] for x in queries])
        
        seg_tree = SEG(max_value + 1)
        
        
        
        sorted_list = SortedList()
        sorted_list.add(0)
        
        seg_tree.update(0,math.inf)
        
        def insert_val(x):
            sorted_list.add(x)
            index = sorted_list.bisect_left(x)
            if index-1 >= 0:
                curr = sorted_list[index-1]
                seg_tree.update(curr,x-curr)
            if index+1 < len(sorted_list):
                next_val = sorted_list[index+1]
                seg_tree.update(x,next_val-x)
            else:
                seg_tree.update(x,math.inf)
            #sorted_list.add(x)
        
        ans = []
        
        for zeb in queries:
            if zeb[0] == 1:
                insert_val(zeb[1])
            else:
                x = zeb[1]
                size = zeb[2]
                if size > x:
                    ans.append(False)
                    continue
                #print(0,x-size+1,seg_tree.query(0,x-size+1))
                max_value = seg_tree.query(0,x-size+1)
                if max_value >= size:
                    ans.append(True)
                else:
                    ans.append(False)
        # for x in range(10):
        #     print(x,seg_tree.query(x,x+1))
        # print(seg_tree.query(0,1))
        # print(seg_tree.query(1,2))
        # print(seg_tree.query(0,2))
        return ans
        

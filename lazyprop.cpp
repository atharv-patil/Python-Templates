typedef long long ll;

struct seg_tree{
    int NEUTRAL_ELEMENT;
    int NEUTRAL_UPDATE;
    ll size;
    int N;
    vector<int> lazy;
    vector<int> st;

    void init(int n){
        size = 1;
        N = n;
        while(size < n) size <<= 1;

        NEUTRAL_UPDATE = -1;
        NEUTRAL_ELEMENT = -1;
        lazy.assign(2 * size, NEUTRAL_UPDATE);
        st.assign(2 * size, 0);
    }

    int combine(int x, int y){
        int res = max(x, y);
        return res;
    }

    int apply(int curr, int upd, int lx, int rx){
        if(upd == NEUTRAL_UPDATE)   return curr;
        int res = upd; 
        return res;
    }

    int combineUpdate(int new_upd, int old_upd){
        int res =(new_upd == NEUTRAL_UPDATE)?old_upd:new_upd;
        return res;
    }

    void build(int node, int lx, int rx){
        if(rx - lx == 1){
            if(lx < N)
                st[node] = 0;
            return;
        }
        int tm = (lx + rx) >> 1;
        build(2*node + 1, lx, tm);
        build(2*node + 2, tm, rx);
        st[node] = combine(st[2*node + 1], st[2*node + 2]);
    }

    void propagate(ll node, ll lx, ll rx){
        if(rx - lx > 1){
            // Non leaf node
            int tm = (lx + rx) >> 1;
            lazy[2*node + 1] = combineUpdate(lazy[node], lazy[2*node + 1]);
            lazy[2*node + 2] = combineUpdate(lazy[node], lazy[2*node + 2]);
            st[2*node + 1] = apply(st[2*node + 1], lazy[node], lx, tm);
            st[2*node + 2] = apply(st[2*node + 2], lazy[node], tm, rx);
            lazy[node] = NEUTRAL_UPDATE;
        }
    }

    void update(int l, int r, int node, int val, int lx, int rx){
        if(lx >= r || rx <= l){
            return;
        }
        if(lx >= l && rx <= r){
            lazy[node] = combineUpdate(val, lazy[node]);
            st[node] = apply(st[node], val, lx, rx);
            return;
        }

        propagate(node, lx, rx);
        int m = (lx + rx) >> 1;
        update(l, r, 2 * node + 1, val, lx, m);
        update(l, r, 2 * node + 2, val, m, rx);
        st[node] = combine(st[2 * node + 1], st[2 * node + 2]);
    }

    void update(int l, int r, int val){
        update(l, r, 0, val, 0, size);
    }

    int query(int l, int r, int node, int lx, int rx){
        if(rx <= l || lx >= r)  return NEUTRAL_ELEMENT;
        if(lx >= l && rx <= r){
            return st[node];
        }
        propagate(node, lx, rx);
        int m = (lx + rx) >> 1;
        int res = combine(query(l, r, 2 * node + 1, lx, m), query(l, r, 2 * node + 2, m, rx));
        st[node] = combine(st[2 * node + 1], st[2 * node + 2]);
        return res;
    }

    int query(int l, int r){
        return query(l, r, 0, 0, size);
    }

    void build(){
        build(0, 0, size);
    }
} st;


class Solution {
public:
    vector<bool> getResults(vector<vector<int>>& quer) {
        vector<bool> ans;
        int n = quer.size();
        set<int> pts;
        
        seg_tree st;
        st.init(3 * n + 2);
        pts.insert(0);
        
        
        for(auto q:quer){
            int type = q[0];
            int x = q[1];
            if(type == 1){
                auto ub = pts.upper_bound(x);
                auto lb = prev(ub);
                
                st.update(x, x + 1, x - *lb);
                if(ub != pts.end()) st.update(*ub, *ub + 1, *ub - x);
                // cout << st.query(x, x + 1) << endl;
                pts.insert(x);
            }
            else{
                int sz = q[2];
                int mx = st.query(1, x + 1);
                // cout << mx << " ";
                auto ub = pts.upper_bound(x);
                ub = prev(ub);
                mx = max(mx, x - *ub);
                // cout << *ub << endl;
                ans.push_back(mx >= sz);
            }
        }
        
        return ans;
    }
};

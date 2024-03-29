class SortedList():
    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def __init__(self, buckets):
        buckets = list(buckets)
        buckets = sorted(buckets)
        self._build(buckets)

    def __iter__(self):
        for i in self.buckets:
            for j in i:
                yield j

    def __reversed__(self):
        for i in reversed(self.buckets):
            for j in reversed(i):
                yield j

    def __len__(self):
        return self.size

    def __contains__(self, x):
        if self.size == 0:
            return False
        bucket = self._find_bucket(x)
        i = bisect.bisect_left(bucket, x)
        return i != len(bucket) and bucket[i] == x

    def __getitem__(self, x):
        if x < 0:
            x += self.size
        if x < 0:
            raise IndexError
        for i in self.buckets:
            if x < len(i):
                return i[x]
            x -= len(i)
        raise IndexError

    def _build(self, buckets=None):
        if buckets is None:
            buckets = list(self)
        self.size = len(buckets)
        bucket_size = int(
            math.ceil(math.sqrt(self.size/self.BUCKET_RATIO)))
        tmp = []
        for i in range(bucket_size):
            t = buckets[(self.size*i) //
                        bucket_size:(self.size*(i+1))//bucket_size]
            tmp.append(t)
        self.buckets = tmp

    def _find_bucket(self, x):
        for i in self.buckets:
            if x <= i[-1]:
                return i
        return i

    def add(self, x):
        # O(√N)
        if self.size == 0:
            self.buckets = [[x]]
            self.size = 1
            return True

        bucket = self._find_bucket(x)
        bisect.insort(bucket, x)
        self.size += 1
        if len(bucket) > len(self.buckets) * self.REBUILD_RATIO:
            self._build()
        return True

    def remove(self, x):
        # O(√N)
        if self.size == 0:
            return False
        bucket = self._find_bucket(x)
        i = bisect.bisect_left(bucket, x)
        if i == len(bucket) or bucket[i] != x:
            return False
        bucket.pop(i)
        self.size -= 1
        if len(bucket) == 0:
            self._build()
        return True

    def lt(self, x):
        # less than < x
        for i in reversed(self.buckets):
            if i[0] < x:
                return i[bisect.bisect_left(i, x) - 1]

    def le(self, x):
        # less than or equal to <= x
        for i in reversed(self.buckets):
            if i[0] <= x:
                return i[bisect.bisect_right(i, x) - 1]

    def gt(self, x):
        # greater than > x
        for i in self.buckets:
            if i[-1] > x:
                return i[bisect.bisect_right(i, x)]

    def ge(self, x):
        # greater than or equal to >= x
        for i in self.buckets:
            if i[-1] >= x:
                return i[bisect.bisect_left(i, x)]

    def index(self, x):
        # the number of elements < x
        ans = 0
        for i in self.buckets:
            if i[-1] >= x:
                return ans + bisect.bisect_left(i, x)
            ans += len(i)
        return ans

    def index_right(self, x):
        # the number of elements < x
        ans = 0
        for i in self.buckets:
            if i[-1] > x:
                return ans + bisect.bisect_right(i, x)
            ans += len(i)
        return ans

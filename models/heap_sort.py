class HeapSort:
    def __init__(self, data):
        self.data = data.copy()
        self.comparison_count = 0
        self.swap_count = 0
        self.n = len(self.data)

    def _heapify(self, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n:
            self.comparison_count += 1
            yield self.data.copy(), self.comparison_count, self.swap_count, [i, l]
            if self.data[l] > self.data[largest]:
                largest = l

        if r < n:
            self.comparison_count += 1
            yield self.data.copy(), self.comparison_count, self.swap_count, [largest, r]
            if self.data[r] > self.data[largest]:
                largest = r

        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.swap_count += 1
            yield self.data.copy(), self.comparison_count, self.swap_count, [i, largest]
            for state in self._heapify(n, largest):
                yield state

    def sort(self):
        for i in range(self.n // 2 - 1, -1, -1):
            for state in self._heapify(self.n, i):
                yield state

        for i in range(self.n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            self.swap_count += 1
            yield self.data.copy(), self.comparison_count, self.swap_count, [0, i]
            for state in self._heapify(i, 0):
                yield state
        yield self.data.copy(), self.comparison_count, self.swap_count, []

    def sort(self):
        """堆排序生成器"""
        # 构建最大堆
        for i in range(self.n // 2 - 1, -1, -1):
            for state in self._heapify(self.n, i):
                yield state

        # 逐个提取元素
        for i in range(self.n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            self.swap_count += 1
            # 修复：添加current_indices参数
            yield self.data.copy(), self.comparison_count, self.swap_count, [0, i]
            # 调用堆化函数处理剩余元素
            for state in self._heapify(i, 0):
                yield state
        # 修复：最后返回时添加空列表作为第四个值
        yield self.data.copy(), self.comparison_count, self.swap_count, []
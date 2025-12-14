class QuickSort:
    def __init__(self, data):
        self.data = data.copy()
        self.comparison_count = 0
        self.swap_count = 0

    def _partition(self, low, high):
        """分区函数（生成器），返回pivot的最终索引"""
        pivot = self.data[high]
        i = low - 1
        for j in range(low, high):
            self.comparison_count += 1
            if self.data[j] <= pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.swap_count += 1
                yield self.data.copy(), self.comparison_count, self.swap_count, [i, j]
            else:
                yield self.data.copy(), self.comparison_count, self.swap_count, [j, high]
        # 交换pivot到正确位置
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        self.swap_count += 1
        yield self.data.copy(), self.comparison_count, self.swap_count, [i + 1, high]
        # 返回pivot的最终索引（关键）
        return i + 1

    def _quick_sort_recursive(self, low, high):
        """递归快速排序（生成器）"""
        if low < high:
            # 创建分区生成器
            partition_gen = self._partition(low, high)
            pi = None
            # 遍历分区生成器的每一步状态
            try:
                while True:
                    state = next(partition_gen)
                    yield state
            except StopIteration as e:
                # 捕获_partition的return值（pivot索引）
                pi = e.value
            # 递归排序左、右分区
            yield from self._quick_sort_recursive(low, pi - 1)
            yield from self._quick_sort_recursive(pi + 1, high)

    def sort(self):
        """对外暴露的排序生成器（类方法，缩进必须正确）"""
        # 递归排序整个数组
        yield from self._quick_sort_recursive(0, len(self.data) - 1)
        # 最后返回最终状态（4个值，与主程序匹配）
        yield self.data.copy(), self.comparison_count, self.swap_count, []
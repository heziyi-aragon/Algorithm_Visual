class BubbleSort:
    def __init__(self, data):
        self.data = data.copy()
        self.comparison_count = 0  # 比较次数
        self.swap_count = 0        # 交换次数

    def sort(self):
        n = len(self.data)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.comparison_count += 1
                current_indices = [j, j+1]  # 当前比较的两个元素索引
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.swap_count += 1
                    swapped = True
                # 生成当前状态 + 当前操作的索引
                yield self.data.copy(), self.comparison_count, self.swap_count, current_indices
            if not swapped:
                break
        # 最后返回最终状态，所有元素标绿
        yield self.data.copy(), self.comparison_count, self.swap_count, []
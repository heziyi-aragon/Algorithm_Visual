class MergeSort:
    def __init__(self, data):
        self.data = data.copy()
        self.comparison_count = 0
        self.swap_count = 0  

    def _merge(self, left, mid, right):
        """合并函数（生成器）"""
        n1 = mid - left + 1
        n2 = right - mid

        # 创建临时数组
        L = self.data[left:left + n1]
        R = self.data[mid + 1:mid + 1 + n2]

        i = j = 0
        k = left

        # 合并临时数组到原数组
        while i < n1 and j < n2:
            self.comparison_count += 1
            if L[i] <= R[j]:
                self.data[k] = L[i]
                i += 1
            else:
                self.data[k] = R[j]
                j += 1
            self.swap_count += 1
            # 增加当前合并的索引
            yield self.data.copy(), self.comparison_count, self.swap_count, [k]
            k += 1

        # 复制剩余的L元素
        while i < n1:
            self.data[k] = L[i]
            self.swap_count += 1
            yield self.data.copy(), self.comparison_count, self.swap_count, [k]
            i += 1
            k += 1

        # 复制剩余的R元素
        while j < n2:
            self.data[k] = R[j]
            self.swap_count += 1
            yield self.data.copy(), self.comparison_count, self.swap_count, [k]
            j += 1
            k += 1

    def _merge_sort_recursive(self, left, right):
        """递归归并排序（生成器）"""
        if left < right:
            mid = (left + right) // 2
            # 递归排序左、右部分
            for state in self._merge_sort_recursive(left, mid):
                yield state
            for state in self._merge_sort_recursive(mid + 1, right):
                yield state
            # 合并
            for state in self._merge(left, mid, right):
                yield state

    def sort(self):
        """对外暴露的排序生成器"""
        yield from self._merge_sort_recursive(0, len(self.data) - 1)
        # 最后返回最终状态
        yield self.data.copy(), self.comparison_count, self.swap_count
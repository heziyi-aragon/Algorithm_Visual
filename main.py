import tkinter as tk
from tkinter import ttk, messagebox
import random
from models import BubbleSort, QuickSort, HeapSort, MergeSort

class SortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("排序算法可视化")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # 初始化参数
        self.data = []  # 待排序数据
        self.data_size = 15  # 数据数量
        self.max_value = 400  # 数据最大值（对应画布高度）
        self.speed = 50  # 可视化速度（ms）
        self.is_sorting = False  # 是否正在排序
        self.sort_generator = None  # 排序生成器

        # 创建UI组件
        self._create_widgets()
        # 生成初始数据
        self._generate_data()

    def _create_widgets(self):
        """创建界面组件"""
        # 顶部控制面板
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        # 算法选择
        ttk.Label(control_frame, text="排序算法：").grid(row=0, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar(value="冒泡排序")
        algorithm_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.algorithm_var,
            values=["冒泡排序", "快速排序", "堆排序", "归并排序"],
            state="readonly"
        )
        algorithm_combobox.grid(row=0, column=1, padx=5, pady=5)

        # 速度控制
        ttk.Label(control_frame, text="速度：").grid(row=0, column=2, padx=5, pady=5)
        self.speed_scale = ttk.Scale(
            control_frame,
            from_=10,
            to=200,
            orient=tk.HORIZONTAL,
            command=lambda v: setattr(self, "speed", int(float(v)))
        )
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=0, column=3, padx=5, pady=5)

        # 功能按钮
        ttk.Button(control_frame, text="生成新数据", command=self._generate_data).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(control_frame, text="开始排序", command=self._start_sort).grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(control_frame, text="停止排序", command=self._stop_sort).grid(row=0, column=6, padx=5, pady=5)

        # 统计信息面板
        stats_frame = ttk.Frame(self.root, padding="10")
        stats_frame.pack(fill=tk.X)
        ttk.Label(stats_frame, text="比较次数：").grid(row=0, column=0, padx=5, pady=5)
        self.comparison_label = ttk.Label(stats_frame, text="0")
        self.comparison_label.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(stats_frame, text="交换/移动次数：").grid(row=0, column=2, padx=5, pady=5)
        self.swap_label = ttk.Label(stats_frame, text="0")
        self.swap_label.grid(row=0, column=3, padx=5, pady=5)

        # 可视化画布
        self.canvas = tk.Canvas(self.root, width=880, height=400, bg="white")
        self.canvas.pack(pady=10)

    def _generate_data(self):
        """生成随机数据"""
        if not self.is_sorting:
            self.data = [random.randint(1, self.max_value) for _ in range(self.data_size)]
            self._draw_data()
            # 重置统计信息
            self.comparison_label.config(text="0")
            self.swap_label.config(text="0")

    def _draw_data(self, current_indices=None):
        self.canvas.delete("all")
        canvas_width = 880
        canvas_height = 400
        bar_width = canvas_width / self.data_size
        current_indices = current_indices or []
        
        # 通用已排序元素数量计算（适用于所有算法）
        sorted_count = 0
        if self.is_sorting:
            n = self.data_size
            comparison_count = int(self.comparison_label["text"])
            # 估算已排序元素：通过比较次数和总数据量的比例
            # 当比较次数接近n*log2(n)时，认为大部分元素已排序
            max_est_comparisons = n * (n.bit_length())  # 近似n*log2(n)
            sorted_count = min(int(comparison_count / max_est_comparisons * n), n)

        for i, value in enumerate(self.data):
            x0 = i * bar_width
            y0 = canvas_height - value
            x1 = (i + 1) * bar_width
            y1 = canvas_height

            # 颜色逻辑：
            if i in current_indices:
                color = "#e74c3c"  # 当前操作元素 → 红色
            elif i >= len(self.data) - sorted_count:
                color = "#2ecc71"  # 已排序元素 → 绿色
            else:
                color = "#3498db"  # 未处理元素 → 浅蓝色

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=1)
            if bar_width > 10:  # 显示数值（宽度足够时）
                self.canvas.create_text(
                    (x0 + x1) / 2, 
                    y0 - 10, 
                    text=str(value), 
                    fill="#2c3e50",
                    font=("Arial", 8)
                )
        self.root.update_idletasks()

    def _get_sort_round(self):
        """辅助函数：获取冒泡排序当前轮次（用于标记已排序元素）"""
        # 从比较次数反推轮次（仅冒泡排序适用，简化实现）
        comparison_count = int(self.comparison_label["text"])
        n = self.data_size
        round_num = 0
        total = 0
        while total + (n - round_num - 1) <= comparison_count:
            total += (n - round_num - 1)
            round_num += 1
        return round_num

    def _get_sort_algorithm(self):
        """根据选择的算法返回对应的排序实例"""
        algorithm = self.algorithm_var.get()
        if algorithm == "冒泡排序":
            return BubbleSort(self.data)
        elif algorithm == "快速排序":
            return QuickSort(self.data)
        elif algorithm == "堆排序":
            return HeapSort(self.data)
        elif algorithm == "归并排序":
            return MergeSort(self.data)
        else:
            raise ValueError("不支持的排序算法")

    def _start_sort(self):
        """开始排序"""
        if self.is_sorting:
            return
        if not self.data:
            return

        # 重置统计信息
        self.comparison_label.config(text="0")
        self.swap_label.config(text="0")

        # 获取排序算法实例
        sort_algorithm = self._get_sort_algorithm()
        self.sort_generator = sort_algorithm.sort()
        self.is_sorting = True
        self._next_step()

    def _next_step(self):
        if not self.is_sorting or self.sort_generator is None:
            return
        try:
            # 新增：接收 current_indices
            current_data, comparison_count, swap_count, current_indices = next(self.sort_generator)
            self.data = current_data
            self.comparison_label.config(text=str(comparison_count))
            self.swap_label.config(text=str(swap_count))
            # 传递 current_indices 给绘图方法
            self._draw_data(current_indices=current_indices)
            self.root.after(self.speed, self._next_step)
        except StopIteration:
            self.is_sorting = False
            # 排序完成后，所有元素标绿
            self._draw_data(current_indices=[])
            messagebox.showinfo("完成", "排序已完成！")
    def _stop_sort(self):
        """停止排序"""
        self.is_sorting = False
        self.sort_generator = None

if __name__ == "__main__":
    root = tk.Tk()
    app = SortVisualizer(root)
    root.mainloop()
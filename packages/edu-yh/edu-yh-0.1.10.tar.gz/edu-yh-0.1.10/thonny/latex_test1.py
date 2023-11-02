import tkinter as tk
from PIL import ImageTk, Image
from pdf2image import convert_from_path


class PDFViewer:
    def __init__(self, master, pdf_path):
        # 创建主窗口
        self.master = master
        self.master.title("PDF Viewer")

        # 转换PDF文件为图像
        self.pages = convert_from_path(pdf_path, dpi=300)

        # 设置容器和画布
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 显示第一页PDF图像
        self.current_page_number = 0
        self.current_page_image = ImageTk.PhotoImage(self.pages[self.current_page_number])
        self.image_label = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_page_image)

        # 创建“上一个”按钮
        self.prev_page_button = tk.Button(self.master, text="<<", command=self.prev_page)
        self.prev_page_button.pack(side=tk.LEFT)

        # 创建“下一个”按钮
        self.next_page_button = tk.Button(self.master, text=">>", command=self.next_page)
        self.next_page_button.pack(side=tk.RIGHT)

        # 创建滚动条
        self.scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self._scroll_canvas)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 配置滚动条与画布的关联
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self._resize_canvas)

        # 绑定鼠标滚轮事件
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _resize_canvas(self, event):
        # 调整画布大小以适应容器
        self.canvas.itemconfig(self.image_label, image=self.current_page_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def prev_page(self):
        # 显示上一页PDF图像
        if self.current_page_number > 0:
            self.current_page_number -= 1
            self.current_page_image = ImageTk.PhotoImage(self.pages[self.current_page_number])
            self.canvas.itemconfig(self.image_label, image=self.current_page_image)

    def next_page(self):
        # 显示下一页PDF图像
        if self.current_page_number < len(self.pages) - 1:
            self.current_page_number += 1
            self.current_page_image = ImageTk.PhotoImage(self.pages[self.current_page_number])
            self.canvas.itemconfig(self.image_label, image=self.current_page_image)

    def _scroll_canvas(self, *args):
        # 处理滚动条事件，更新当前页面和图像
        scroll_fraction = self.scrollbar.get()[0]
        self.current_page_number = int(scroll_fraction * len(self.pages))
        self.current_page_image = ImageTk.PhotoImage(self.pages[self.current_page_number])
        self.canvas.itemconfig(self.image_label, image=self.current_page_image)

    def _on_mousewheel(self, event):
        # 处理鼠标滚轮事件，根据滚动方向向上或向下滚动页面
        if event.num == 4 or event.delta == 120:
            self.prev_page()
        elif event.num == 5 or event.delta == -120:
            self.next_page()


# 示例代码
root = tk.Tk()
pdf_viewer = PDFViewer(root, "C:\\Users\\adt\\Desktop\\snow.pdf")
root.mainloop()


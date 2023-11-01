from thonny import get_workbench, tktextext, ui_utils
from thonny.ui_utils import scrollbar_style
import subprocess
import shutil
import uuid
from tkinter import filedialog
from thonny.misc_utils import running_on_mac_os, running_on_linux
import tkinter as tk
from pdf2image import convert_from_path
from thonny.languages import tr
from PIL import ImageTk, Image
from tkinter import messagebox
import os


class LatextView(tktextext.TextFrame):
    def __init__(self, master):
        tktextext.TextFrame.__init__(
            self,
            master,
            vertical_scrollbar_style=scrollbar_style("Vertical"),
            horizontal_scrollbar_style=scrollbar_style("Horizontal"),
            horizontal_scrollbar_class=ui_utils.AutoScrollbar,
            read_only=True,
            font="TkDefaultFont",
            padx=10,
            pady=0,
            insertwidth=0,
        )

        self.pages = None
        self.current_page_number = 0
        self.current_page_image = None
        self.image_label = None
        self.prev_page_button = None
        self.next_page_button = None
        self.pdf_name = None
        get_workbench().bind("PreviewLatex", self.show_latex)
        get_workbench().bind("HideView", self.hidden_latex)

    def hidden_latex(self, event):
        if self.pdf_name:
            # 清理生成的临时文件
            if running_on_linux() or running_on_mac_os():
                subprocess.run(["rm", self.pdf_name])  # Linux/MacOS
            else:
                subprocess.run(["del", self.pdf_name],
                               shell=True)  # Windows
        self.unbind("PreviewLatex")
        self.unbind("HideView")
        get_workbench().get_view("LatextView").destroy()
        get_workbench().add_view(LatextView, tr("Latext"), "se", visible_by_default=False)
    def _render_pdf(self, path):
        self.pages = convert_from_path(path)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        image_width = min(800, screen_width * 0.8)  # 占用80%的屏幕宽度
        image_height = min(800, screen_height * 0.8)  # 占用80%的屏幕高度
        resized_image = self.pages[self.current_page_number].resize((image_width, image_height), Image.LANCZOS)
        self.current_page_image = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(self.text, image=self.current_page_image)
        self.image_label.grid(row=1, column=0, columnspan=3)

        # 创建“上一个”和“下一个”按钮
        self.prev_page_button = tk.Button(self.text, text="上一页", command=self.prev_page)
        self.prev_page_button.grid(row=0, column=0)

        self.next_page_button = tk.Button(self.text, text="下一页", command=self.next_page)
        self.next_page_button.grid(row=0, column=1)

        self.download_btn = tk.Button(self.text, text="下载", command=self.download_pdf)
        self.download_btn.grid(row=0, column=2)

    def _run_build_latex(self, event):
        self._render_pdf(event.content)

    def download_pdf(self):
        filename = self.find_pdf_files_in_current_directory()
        print('找到了', filename)
        if filename:
            folder_path = filedialog.askdirectory()
            if folder_path:
                shutil.copy(filename, folder_path)
                messagebox.showinfo('成功', '下载成功')
        else:
            messagebox.showerror('下载错误', '编译可能出现问题，进检查语法是否有问题')
    def find_pdf_files_in_current_directory(self):
        # 获取当前目录
        current_directory = os.getcwd()

        # 遍历当前目录中的文件
        for filename in os.listdir(current_directory):
            # 检查文件是否以 .pdf 结尾
            if filename.endswith(".pdf"):
                return filename
        return None

    def show_latex(self, event):
        if hasattr(event, 'type'):
            self._run_build_latex(event)
            return
        path = preview_latex(event.content)
        self.pdf_name = path
        # 渲染pdf
        self._render_pdf(path)

    def prev_page(self):
        # 显示上一页PDF图像
        if self.current_page_number > 0:
            self.current_page_number -= 1
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            image_width = min(800, screen_width * 0.8)  # 占用80%的屏幕宽度
            image_height = min(800, screen_height * 0.8)  # 占用80%的屏幕高度
            resized_image = self.pages[self.current_page_number].resize((image_width, image_height), Image.LANCZOS)
            self.current_page_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.current_page_image)
        else:
            messagebox.showinfo('第一页' , '已经是第一页了哦')

    def next_page(self):
        # 显示下一页PDF图像
        if self.current_page_number < len(self.pages) - 1:
            self.current_page_number += 1
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            image_width = min(800, screen_width * 0.8)  # 占用80%的屏幕宽度
            image_height = min(800, screen_height * 0.8)  # 占用80%的屏幕高度
            resized_image = self.pages[self.current_page_number].resize((image_width, image_height), Image.LANCZOS)
            self.current_page_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.current_page_image)
        else:
            messagebox.showinfo('最后一页', '已经是最后一页了哦')


def preview_latex(content):
    name = str(uuid.uuid4())

    # 将 LaTeX 内容保存到 .tex 文件中
    with open(name + ".tex", "w", encoding="utf-8") as tex_file:
        tex_file.write(content)

    try:
        # 使用 pdflatex 编译 LaTeX 文件并指定输出目录
        if running_on_linux() or running_on_mac_os():
            subprocess.run(["pdflatex", name + ".tex"])
        else:
            subprocess.run(["pdflatex", name + ".tex"], shell=True)  # Windows

        print("LaTeX 编译成功")

        get_workbench().show_view("LatextView", set_focus=False)

    except subprocess.CalledProcessError:
        print("LaTeX 编译失败")
    finally:
        # 清理生成的临时文件
        if running_on_linux() or running_on_mac_os():
            subprocess.run(["rm", name + ".tex", name + ".aux", name + ".log", name + ".pytxcode"])  # Linux/MacOS
        else:
            subprocess.run(["del", name + ".tex", name + ".aux", name + ".log", name + ".pytxcode"],
                           shell=True)  # Windows
        return name + ".pdf"


def create_latex(content):
    output_folder = filedialog.askdirectory(title="选择输出文件夹")

    name = str(uuid.uuid4())

    # 将 LaTeX 内容保存到 .tex 文件中
    with open(name + ".tex", "w", encoding="utf-8") as tex_file:
        tex_file.write(content)

    try:
        # 使用 pdflatex 编译 LaTeX 文件并指定输出目录
        if running_on_linux() or running_on_mac_os():
            subprocess.run(["pdflatex", name + ".tex"])
        else:
            subprocess.run(["pdflatex", name + ".tex"], shell=True)  # Windows

        # 移动生成的 PDF 文件到指定位置
        shutil.move(name + ".pdf", output_folder)

        messagebox.showinfo('成功', '编译成功')
    except subprocess.CalledProcessError:
        messagebox.showerror('失败', '编译失败')
    finally:
        # 清理生成的临时文件
        if running_on_linux() or running_on_mac_os():
            subprocess.run(["rm", name + ".tex", name + ".aux", name + ".log", name + ".pytxcode"])  # Linux/MacOS
        else:
            subprocess.run(["del", name + ".tex", name + ".aux", name + ".log", name + ".pytxcode"],
                           shell=True)  # Windows


def init():
    get_workbench().add_view(LatextView, tr("Latext"), "se", visible_by_default=False)

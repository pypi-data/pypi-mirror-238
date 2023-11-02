from thonny.ui_utils import CommonDialog
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import shutil


class ImageDialog(CommonDialog):
    def __init__(self, master):
        super().__init__(master=master)
        self.title("图片管理器")
        self.geometry("900x650")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.image_folder = "./images"  # 图片存储文件夹
        self.image_tks = []
        # 创建界面组件
        self.create_widgets()

        self.current_path = self.image_folder

        # 创建图片文件夹（如果不存在）
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        # 在窗口打开时加载并展示所有图片
        self.load_and_display_images()

        # 加载树形文件栏
        self.update_treeview()

    def create_widgets(self):
        # 操作栏
        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.pack(side="top", fill="x")

        self.create_folder_button = ttk.Button(self.toolbar_frame, text="创建文件夹", command=self.create_folder)
        self.create_folder_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_folder_button = ttk.Button(self.toolbar_frame, text="删除文件夹", command=self.delete_folder)
        self.delete_folder_button.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.toolbar_frame, text="添加图片", command=self.add_image)
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        # self.delete_button = ttk.Button(self.toolbar_frame, text="删除", command=self.delete_selected)
        # self.delete_button.grid(row=0, column=3, padx=5, pady=5)

        # 树形栏
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(side="left", fill="y")

        self.treeview = ttk.Treeview(self.tree_frame)
        self.treeview.pack(side="left", fill="y")

        self.treeview.bind("<<TreeviewSelect>>", self.tree_item_selected)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.treeview.yview)
        self.tree_scroll.pack(side="right", fill="y")

        self.treeview.config(yscrollcommand=self.tree_scroll.set)

        # 图片显示区域
        self.image_frame = tk.Canvas(self)
        self.image_frame.pack(side="right", fill="both", expand=True)

        self.image_frame_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.image_frame.yview)
        self.image_frame_scrollbar.pack(side="right", fill="y")

        self.image_frame.configure(yscrollcommand=self.image_frame_scrollbar.set)

        self.image_frame_container = ttk.Frame(self.image_frame)
        self.image_frame.create_window((0, 0), window=self.image_frame_container, anchor="nw")

        self.image_labels = []  # 存储图片标签的列表
        self.selected_items = []  # 存储选中的项
        self.select_checkboxes = []  # 存储选择框的列表
    def copy_image_path(self, event, img_tk):
        root = self.winfo_toplevel()  # 获取主窗口
        root.clipboard_clear()  # 清空剪贴板
        root.clipboard_append(img_tk)  # 添加图像文件名到剪贴板
        root.update()  # 更新剪贴板内容

    def add_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            # 将选择的图片复制到图片文件夹
            file_name = os.path.basename(file_path)
            destination = os.path.join(self.current_path, file_name)
            try:
                shutil.copy(file_path, destination)
            except Exception as e:
                messagebox.showerror("错误", f"添加图片失败：{str(e)}")
                return

            # messagebox.showinfo("成功", f"图片已成功添加到 {self.current_path}")

            # 重新加载和展示所有图片
            self.load_and_display_images()

    def load_and_display_images(self):
        print(1111)
        print(self)
        # 清空之前的图片标签和ImageTk.PhotoImage对象
        for label in self.image_labels:
            label.destroy()
            print('label', label)

        # 清空之前的选择框
        for checkbox in self.select_checkboxes:
            checkbox.destroy()
        self.select_checkboxes.clear()

        self.image_labels.clear()
        self.image_tks.clear()

        image_files = [f for f in os.listdir(self.current_path) if
                       f.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
        print('我喜欢你', image_files)

        # 创建并展示图片标签
        for i, image_file in enumerate(image_files):
            img = Image.open(os.path.join(self.current_path, image_file))
            img.thumbnail((200, 200))  # 调整图像大小为缩略图
            img_tk = ImageTk.PhotoImage(img)

            div = ttk.Frame(self.image_frame_container)
            div.grid(row=i // 2, column=i % 2, padx=5, pady=5)
            label = ttk.Label(div, image=img_tk)
            label.image = img_tk
            label.pack()

            # 放置按钮，靠下居中
            copy_path = ttk.Button(div, text="复制路径")
            copy_path.pack(side="bottom")
            res_path = self.replace_backslash_with_forwardslash(os.path.join(self.current_path, image_file))
            # 绑定按钮的点击事件
            copy_path.bind("<Button-1>", lambda event, img_tk=res_path: self.copy_image_path(event, img_tk))
            self.image_labels.append(div)

        # 更新画布窗口大小以适应图像数量
        self.image_frame.update_idletasks()
        self.image_frame.config(scrollregion=self.image_frame.bbox("all"))

    def replace_backslash_with_forwardslash(self, string):
        new_string = string.replace('\\', '/')
        return new_string
    def create_folder(self):
        folder_name = simpledialog.askstring("创建文件夹", "请输入文件夹名称")
        if folder_name:
            folder_path = os.path.join(self.image_folder, folder_name)
            try:
                os.makedirs(folder_path)
            except Exception as e:
                messagebox.showerror("错误", f"创建文件夹失败：{str(e)}")
                return

            messagebox.showinfo("成功", f"文件夹 {folder_name} 已成功创建")

            # 更新树形栏
            self.update_treeview()

    def delete_folder(self):
        selected_items = self.treeview.selection()

        if not selected_items:
            messagebox.showinfo("提示", "请选择要删除的文件夹")
            return

        for item in selected_items:
            folder_name = self.treeview.item(item, "text")
            if folder_name == ".":
                messagebox.showinfo("提示", "不允许删除默认图片文件夹")
            else:
                confirmation = messagebox.askyesno("确认删除", f"确定要删除文件夹 '{folder_name}' 吗？")
                if confirmation:
                    try:
                        shutil.rmtree(os.path.join(self.image_folder, folder_name))
                        messagebox.showinfo("成功", f"文件夹 '{folder_name}' 已成功删除")
                    except Exception as e:
                        messagebox.showerror("错误", f"删除文件夹失败：{str(e)}")

        # 更新树形栏
        self.update_treeview()

    def update_treeview(self):
        # 清空树形栏
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # 重新加载树形栏
        for root, dirs, files in os.walk(self.image_folder):
            folder_name = os.path.relpath(root, self.image_folder)
            parent_item = "" if folder_name == "." else os.path.dirname(folder_name)
            self.treeview.insert(parent_item, "end", folder_name, text=os.path.basename(folder_name))

    def tree_item_selected(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            folder_name = self.treeview.item(selected_item[0], "text")
            self.current_path = os.path.join(self.image_folder, folder_name)

            # 清空之前的图片标签和选择框
            for label in self.image_labels:
                label.destroy()
            self.image_labels.clear()

            for checkbox in self.select_checkboxes:
                checkbox.destroy()
                self.select_checkboxes.remove(checkbox)

            # 清空选中的项
            self.selected_items.clear()
            self.image_tks.clear()  # 清空存储的图像对象

            image_files = [f for f in os.listdir(self.current_path) if
                           f.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]

            # 创建并展示图片标签
            for i, image_file in enumerate(image_files):
                img = Image.open(os.path.join(self.current_path, image_file))
                img.thumbnail((200, 200))  # 调整图像大小为缩略图
                img_tk = ImageTk.PhotoImage(img)

                div = ttk.Frame(self.image_frame_container)
                div.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                label = ttk.Label(div, image=img_tk)
                label.image = img_tk
                label.pack()
                print('我是img_tk', os.path.join(self.current_path, image_file))

                # 放置按钮，靠下居中
                copy_path = ttk.Button(div, text="复制路径")
                copy_path.pack(side="bottom")
                res_path = self.replace_backslash_with_forwardslash(os.path.join(self.current_path, image_file))
                # 绑定按钮的点击事件
                copy_path.bind("<Button-1>",
                               lambda event, img_tk=res_path: self.copy_image_path(
                                   event, img_tk))
                self.image_labels.append(div)
            # 更新画布窗口大小以适应图像数量
            self.image_frame.update_idletasks()
            self.image_frame.config(scrollregion=self.image_frame.bbox("all"))
    def on_closing(self):
        self.destroy()  # 销毁窗口

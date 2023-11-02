import wx
import fitz
import os


class PDFViewer(wx.Frame):
    def __init__(self, parent, title):
        super(PDFViewer, self).__init__(parent, title=title, size=(800, 600))
        self.panel = wx.Panel(self)
        self.splitter = wx.SplitterWindow(self.panel)
        self.file_list = wx.ListBox(self.splitter, style=wx.LB_SINGLE)
        self.pdf_view = wx.ScrolledWindow(self.splitter)
        self.splitter.SplitVertically(self.file_list, self.pdf_view)
        self.Bind(wx.EVT_LISTBOX, self.on_file_selected, self.file_list)

        self.prev_button = wx.Button(self.panel, label="上一页")
        self.next_button = wx.Button(self.panel, label="下一页")
        self.prev_button.Bind(wx.EVT_BUTTON, self.on_prev_page)
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_page)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        sizer.Add(self.prev_button, 0, wx.ALIGN_LEFT)
        sizer.Add(self.next_button, 0, wx.ALIGN_LEFT)
        self.panel.SetSizer(sizer)
        self.load_files()

    def load_files(self):
        dlg = wx.DirDialog(self, "选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.folder_path = dlg.GetPath()
            files = os.listdir(self.folder_path)
            pdf_files = [file for file in files if file.lower().endswith('.pdf')]
            self.file_list.Set(pdf_files)
        dlg.Destroy()

    def on_file_selected(self, event):
        selected_file = self.file_list.GetStringSelection()
        file_path = os.path.join(self.folder_path, selected_file)
        doc = fitz.open(file_path)
        self.pages = []

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            image = wx.Image(pix.width, pix.height, pix.samples)
            image.SetData(pix.samples)
            bitmap = image.ConvertToBitmap()
            self.pages.append(wx.StaticBitmap(self.pdf_view, -1, bitmap))

        self.show_page(0)

    def show_page(self, page_num):
        if 0 <= page_num < len(self.pages):
            current_page = self.pages[page_num]
            self.current_page_num = page_num
            self.pdf_view.SetScrollbars(20, 20, int(current_page.GetSize()[0] / 20),
                                        int(current_page.GetSize()[1] / 20))
            self.pdf_view.SetVirtualSize(current_page.GetSize())
            self.pdf_view.ClearBackground()
            dc = wx.ClientDC(self.pdf_view)
            dc.DrawBitmap(current_page.GetBitmap(), 0, 0)

    def on_prev_page(self, event):
        if hasattr(self, 'current_page_num'):
            if self.current_page_num > 0:
                self.show_page(self.current_page_num - 1)

    def on_next_page(self, event):
        if hasattr(self, 'current_page_num'):
            if self.current_page_num < len(self.pages) - 1:
                self.show_page(self.current_page_num + 1)


app = wx.App()
frame = PDFViewer(None, "PDF Viewer")
frame.Show()
app.MainLoop()

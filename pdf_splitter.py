import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk

def is_valid_depth(value):
    """验证 TOC 深度输入是否为正整数"""
    try:
        depth = int(value)
        if depth <= 0:
            raise ValueError("深度必须是正整数。")
        return depth
    except ValueError:
        return None

def get_pdf_toc(doc):
    """从 PDF 获取目录（TOC）"""
    return doc.get_toc()

def filter_toc_by_depth(toc, depth):
    """根据指定深度过滤目录（TOC）"""
    return [(level, title.strip(), page) for level, title, page in toc if level == depth]

def create_output_folder(base_path):
    """创建输出文件夹（如果不存在）"""
    folder_name = os.path.join(base_path, "split_pdf_output")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def split_pdf_by_toc(doc, toc, output_folder, page_offset=0):
    """根据目录（TOC）将 PDF 分割成多个小 PDF"""
    title_count = {}  # 用于跟踪标题出现的次数，确保文件名唯一

    for i, (level, title, start_page) in enumerate(toc):
        start_page_display = max(start_page - page_offset, 1)

        if title not in title_count:
            title_count[title] = 1
        else:
            title_count[title] += 1

        title_suffix = f"_{title_count[title]}" if title_count[title] > 1 else ""

        if i + 1 < len(toc):
            end_page = toc[i + 1][2] - 1
        else:
            end_page = doc.page_count

        end_page_display = max(end_page - page_offset, 1)

        filename = f"{title}{title_suffix}_p{start_page_display}-{end_page_display}.pdf" if start_page != end_page else f"{title}{title_suffix}_p{start_page_display}.pdf"
        filename = filename.translate(str.maketrans("", "", ":/*?<>|"))

        save_path = os.path.join(output_folder, filename)

        split_doc = fitz.open()
        split_doc.insert_pdf(doc, from_page=start_page - 1, to_page=end_page - 1)
        split_doc.save(save_path)
        split_doc.close()

def load_toc():
    """加载目录并实时显示在 GUI 上"""
    global filtered_toc

    try:
        pdf_path = pdf_entry.get().strip()
        depth_value = depth_entry.get().strip()
        depth = is_valid_depth(depth_value)

        if not pdf_path:
            messagebox.showerror("错误", "请先选择一个 PDF 文件。")
            return

        if depth is None:
            messagebox.showerror("错误", "请输入有效的正整数作为 TOC 深度。")
            return

        global doc
        doc = fitz.open(pdf_path)
        toc = get_pdf_toc(doc)

        filtered_toc = filter_toc_by_depth(toc, depth)

        toc_listbox.delete(0, tk.END)
        for entry in filtered_toc:
            title, page = entry[1], entry[2]
            toc_listbox.insert(tk.END, f"{title} (页 {page})")

    except Exception as e:
        messagebox.showerror("错误", f"无法加载目录：{str(e)}")

def preview_page(event):
    """双击目录选项时预览对应页的 PDF 内容"""
    try:
        selected_index = toc_listbox.curselection()
        if not selected_index:
            return
        selected_index = selected_index[0]

        _, title, page = filtered_toc[selected_index]

        pix = doc[page - 1].get_pixmap()
        img_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        preview_window = tk.Toplevel(root)
        preview_window.title(f"预览 - {title} (第 {page} 页)")

        img_resized = img_data.resize((600, 800), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)

        label = tk.Label(preview_window, image=img_tk)
        label.image = img_tk
        label.pack()

    except Exception as e:
        messagebox.showerror("错误", f"无法预览页面：{str(e)}")

def execute_split():
    """根据用户输入执行 PDF 分割操作"""
    pdf_path = pdf_entry.get()
    save_path = save_entry.get()
    page_offset_value = page_offset_entry.get().strip()

    if not pdf_path:
        messagebox.showerror("错误", "请先选择一个 PDF 文件。")
        return

    if not save_path:
        messagebox.showerror("错误", "请先选择保存文件夹。")
        return

    try:
        page_offset = int(page_offset_value) if page_offset_value else 0

        if not filtered_toc:
            messagebox.showerror("错误", "没有可用的章节进行分割。")
            return

        output_folder = create_output_folder(save_path)
        split_pdf_by_toc(doc, filtered_toc, output_folder, page_offset)

        messagebox.showinfo("成功", f"PDF 分割完成。\n文件已保存至: {output_folder}")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{str(e)}")

def open_split_window():
    """打开单独分割的子窗口"""
    load_toc()

    if not filtered_toc:
        messagebox.showerror("错误", "没有有效的 TOC 数据。请先加载 PDF 文件并设置 TOC 深度。")
        return

    split_window = tk.Toplevel(root)
    split_window.title("单独选择 TOC 分割")
    split_window.geometry("600x400")

    split_toc_listbox = tk.Listbox(split_window, selectmode=tk.MULTIPLE, font=("Arial", 10), height=15, width=80)
    split_toc_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    for entry in filtered_toc:
        split_toc_listbox.insert(tk.END, entry[1])

    def save_selected_toc():
        try:
            selected_indices = split_toc_listbox.curselection()
            if not selected_indices:
                messagebox.showerror("错误", "请先选择至少一个 TOC 项。")
                return

            page_offset_value = page_offset_entry.get().strip()
            page_offset = int(page_offset_value) if page_offset_value else 0

            selected_titles = [filtered_toc[i] for i in selected_indices]
            save_path = save_entry.get()

            if not save_path:
                messagebox.showerror("错误", "请先选择保存文件夹。")
                return

            output_folder = create_output_folder(save_path)
            split_pdf_by_toc(doc, selected_titles, output_folder, page_offset)

            messagebox.showinfo("成功", f"所选 TOC 项已成功分割并保存至: {output_folder}")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")

    save_button = ttk.Button(split_window, text="保存选择", command=save_selected_toc)
    save_button.pack(pady=10)

root = tk.Tk()
root.title("PDF 分割器与预览工具")
root.geometry("800x600")

file_frame = ttk.Frame(root, padding="10")
file_frame.pack(pady=10, fill="x")

ttk.Label(file_frame, text="PDF 文件:").pack(side=tk.LEFT, padx=10)
pdf_entry = ttk.Entry(file_frame, width=50)
pdf_entry.pack(side=tk.LEFT, padx=10)
ttk.Button(file_frame, text="浏览", command=lambda: pdf_entry.insert(0, filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")]))).pack(side=tk.LEFT)

save_frame = ttk.Frame(root, padding="10")
save_frame.pack(pady=10, fill="x")

ttk.Label(save_frame, text="保存文件夹:").pack(side=tk.LEFT, padx=10)
save_entry = ttk.Entry(save_frame, width=50)
save_entry.pack(side=tk.LEFT, padx=10)
ttk.Button(save_frame, text="浏览", command=lambda: save_entry.insert(0, filedialog.askdirectory())).pack(side=tk.LEFT)

toc_frame = ttk.Frame(root, padding="10")
toc_frame.pack(pady=10, fill="x")

ttk.Label(toc_frame, text="请输入 TOC 深度:").pack(side=tk.LEFT, padx=10)
depth_entry = ttk.Entry(toc_frame, width=15)
depth_entry.pack(side=tk.LEFT, padx=10)

page_offset_label = ttk.Label(toc_frame, text="页码偏移量:")
page_offset_label.pack(side=tk.LEFT, padx=10)
page_offset_entry = ttk.Entry(toc_frame, width=15)
page_offset_entry.pack(side=tk.LEFT, padx=10)

buttons_frame = ttk.Frame(root, padding="10")
buttons_frame.pack(pady=10, fill="x")

ttk.Button(buttons_frame, text="确认分割", command=execute_split).pack(side=tk.LEFT, padx=10)
ttk.Button(buttons_frame, text="单独分割 TOC", command=open_split_window).pack(side=tk.RIGHT, padx=10)

listbox_frame = ttk.Frame(root, padding="10")
listbox_frame.pack(pady=10, fill="both", expand=True)

scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
toc_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set, width=80, height=20)
toc_listbox.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.config(command=toc_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

toc_listbox.bind("<Double-1>", preview_page)
depth_entry.bind("<KeyRelease>", lambda event: load_toc())

root.mainloop()

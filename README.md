PDF 分割器与预览工具
一个基于 Python 和 Tkinter 的实用工具，用于通过 PDF 的目录（TOC）将 PDF 分割为多个文件，并支持预览和单独分割功能。

功能特点
按 TOC 深度分割 PDF：根据用户输入的 TOC 深度，分割 PDF 文件。
目录实时显示：加载 PDF 的目录（TOC）并显示在 GUI 中。
页面预览：双击目录项可以预览对应的 PDF 页面。
单独分割：支持用户选择部分目录项进行单独分割。
文件保存：将分割后的 PDF 文件保存到指定文件夹中。
环境要求
Python 3.7 或以上
依赖库：
PyMuPDF (fitz)
Pillow (PIL)
tkinter（Python 内置）
安装依赖项：

bash
复制代码
pip install PyMuPDF Pillow
使用方法
克隆此仓库：

bash
复制代码
git clone https://github.com/yourusername/pdf-splitter-tool.git
cd pdf-splitter-tool
运行程序：

bash
复制代码
python pdf_splitter.py
按照以下步骤操作：

选择 PDF 文件：点击“浏览”按钮，选择一个 PDF 文件。
设置保存文件夹：点击“浏览”按钮，选择保存分割文件的文件夹。
输入 TOC 深度：输入需要分割的目录深度（正整数）。
预览页面：在目录列表中双击条目预览页面内容。
执行分割：点击“确认分割”按钮，按照目录深度分割 PDF。
单独分割：点击“单独分割 TOC”按钮，选择特定目录项进行分割。
分割后的文件会保存到指定的文件夹中。

界面截图

主界面示例


页面预览示例

注意事项
TOC 深度必须为正整数，例如：1 表示第一级目录，2 表示第二级目录。
如果 PDF 没有嵌入目录（TOC），工具将无法加载目录。
页码偏移量可用于调整目录页码与实际页码的差异。
贡献
欢迎提交 issues 和 pull requests 来改进此工具！
如有建议或问题，请联系 your.email@example.com。

许可证
本项目基于 MIT 许可证 开源。

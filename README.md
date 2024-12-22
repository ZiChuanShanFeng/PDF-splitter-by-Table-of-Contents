# PDF 分割器与预览工具

一个基于 Python 和 Tkinter 的实用工具，用于通过 PDF 的目录（TOC）将 PDF 分割为多个文件，并支持预览和单独分割功能。

## 功能特点

- **按 TOC 深度分割 PDF**：根据用户输入的 TOC 深度，自动分割 PDF 文件。
- **实时目录显示**：加载 PDF 的目录（TOC）并显示在用户界面中。
- **页面预览**：双击目录项即可预览对应的 PDF 页面内容。
- **单独分割**：支持选择部分目录项单独分割 PDF。
- **灵活设置**：支持页码偏移调整，保存到指定的输出文件夹。

## 环境要求

- **Python**：3.7 或更高版本
- **依赖库**：
  - [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
  - [Pillow](https://pillow.readthedocs.io/en/stable/)
  - tkinter（Python 内置）

## 安装依赖项：
```bash
pip install PyMuPDF Pillow

## 使用说明

## 克隆仓库：

```bash
git clone https://github.com/yourusername/pdf-splitter-tool.git
cd pdf-splitter-tool

## 运行程序

```bash
python pdf_splitter.py

## 操作步骤：

1. 点击“浏览”按钮选择 PDF 文件。
2. 设置保存的输出文件夹。
3. 输入需要分割的 TOC 深度（正整数）。
4. 点击“确认分割”按钮进行批量分割，或使用“单独分割 TOC”按钮选择特定章节分割。
5. 双击目录项可预览对应 PDF 页面。
## 分割结果：

- 所有分割后的 PDF 文件将保存到指定的输出文件夹。
- 文件名格式为：`章节名称_p开始页-结束页.pdf`。
## 界面截图

### 主界面
![主界面](https://your-image-url-here)

### 页面预览
![页面预览](https://your-image-url-here)

## 注意事项

- **TOC 深度**：必须输入正整数，例如 1 表示第一级目录，2 表示第二级目录。
- **页码偏移**：可调整目录页码与实际 PDF 页码之间的差异。
- 如果 PDF 文件没有嵌入目录（TOC），工具将无法加载目录数据。

## 贡献指南

欢迎贡献代码和功能改进！如有任何问题或建议，请提交 [Issues](https://github.com/yourusername/pdf-splitter-tool/issues) 或发送 Pull Request。
## 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

import os,sys
from PyPDF2 import PdfFileMerger,PdfFileReader
import pdfkit

def merge_pdf(file_list,title):
    """
            file_list = [file for file in os.listdir('.') if os.path.splitext(file)[-1] == '.pdf']
            merge_pdf(file_list,title)
    """
    try:
        merger = PdfFileMerger()
        for file_ in file_list:
            merger.append(PdfFileReader(open(file_, 'rb')),import_bookmarks=False)
        output = open('{}.pdf'.format(title),'wb')
        merger.write(output)
    except Exception as e:
        print(e)
    finally:
        return 0 

def save_pdf(html):
    """
    把所有html文件转换成pdf文件
    """

    file_name = ''.join([os.path.splitext(html)[0],'.pdf'])
    print('进程%s正在运行'%os.getpid())
    print('正在处理',file_name)
    options = {
        'margin-top': '0.3in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
        'dpi':'300',
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
    try:
        pdfkit.from_file(html, file_name, options=options)
    except Exception as e:
        print(e)
    finally:
        print(file_name,'创建成功,进程退出')
        return 0

if __name__ == '__main__':
    for file_path in [path for path in os.listdir('.') if os.path.isdir(path)]:
        os.chdir(file_path)
        for html in  [html for html in os.listdir('.') if os.path.splitext(html)[-1] == '.html']:
            save_pdf(html)
        print(os.listdir('.'))
        file_list = [file for file in os.listdir('.') if os.path.splitext(file)[-1] == '.pdf']
        merge_pdf(file_list,file_path)
        os.chdir('..')
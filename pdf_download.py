import requests
import re, os, sys
from PyPDF2 import PdfFileMerger,PdfFileReader
import random
from multiprocessing import Pool,cpu_count
from bs4 import BeautifulSoup
import pdfkit

def merge_pdf(file_list,title):
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
def save_html_to_file(sess, url,index):
    print("进程%s正在运行" % os.getpid())
    print('当前目录为%s' % os.path.abspath('.'))
    r = sess.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    if soup.find_all('img', alt=True):
        soup.find_all('img', alt=True)[0]['src'] = ''.join(['https://www.safaribooksonline.com', soup.find_all('img', alt=True)[0]['src']])
    for i in soup.find_all('link', type='text/css')[-2:]:
        i['href'] = ''.join(['https://www.safaribooksonline.com', i['href']])
    html = str(soup)
    print(index+1,'抓取成功，正在保存')
    with open('{}.html'.format(index),'w',encoding='utf-8') as f:
        f.write(html)
    print("{}.html保存成功".format(index))
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
    pdfkit.from_file(html, file_name, options=options)
    print(file_name,'创建成功,进程退出')


    # url = 'https://www.safaribooksonline.com/home/'
def main(url):

    r = sess.get(url=url,headers=headers,)
    # print(r.text)
    soup = BeautifulSoup(r.text,'lxml')
    title = re.sub(r'[ :\/"<>|]','_',soup.find('h1').get_text())
    if not os.path.exists(title):
        os.mkdir(title)
    os.chdir(title)
    soup.find_all('img',alt=True)[0]['src'] = ''.join(['https://www.safaribooksonline.com',soup.find_all('img',alt=True)[0]['src']])
    for i in soup.find_all('link',type='text/css')[-2:]:
        i['href'] = ''.join(['https://www.safaribooksonline.com',i['href']])
    html = str(soup)
    # print(soup)
    with open('1.html','w',encoding='utf-8') as f:
        f.write(html)
    print('1页面保存完整')
    # save_pdf('1.html','1.pdf')

    other_chapter = soup.select('ol.detail-toc li a')
    chapter_list = []
    for index,chapter in enumerate(other_chapter):
        chapter_url = ''.join(['https://www.safaribooksonline.com',chapter['href']])
        chapter_list.append(chapter_url)
    for index,chapter in enumerate(chapter_list):
        save_html_to_file(sess,chapter,index + 2)
    print('等待全部进程结束')


    # p2 = Pool(cpu_count())
    for html in  [html for html in os.listdir('.') if os.path.splitext(html)[-1] == '.html']:
        save_pdf(html)
    # p2.close()
    # p2.join()
    print(os.listdir('.'))
    file_list = [file for file in os.listdir('.') if os.path.splitext(file)[-1] == '.pdf']
    merge_pdf(file_list,title)


if __name__ == '__main__':

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,ja;q=0.6',
        'cache-control': 'max-age=0',
        'referer': 'https://www.safaribooksonline.com/',
    }
    cookies = {
        'optimizelyEndUserId': 'oeu1509975871757r0.7508240468174463',
        'optimizelySegments': '%7B%7D',
        'optimizelyBuckets': '%7B%7D',
        'BrowserCookie': '9ccbce7d-1c4c-4c44-bfb4-160732694657',
        'corp_sessionid': 'cgvo3kw9b7bhkx595czh1o8atl7gp898',
        'liveagent_oref': 'http://my.safaribooksonline.com/',
        'liveagent_ptid': '2f1516dd-8b8e-4334-81ed-ab47aca7630e',
        '_vwo_uuid_v2': '70FEB63E56A04774A6F3BD6D9A59F4B7|d810a4af0373e4dd4a14dead0e923407',
        'dwf_anybird_skip_topics_experiment': 'True',
        'dwf_dashboard_v10': 'True',
        'recently-viewed': '%5B%229781787288225%3Ach05.html%22%2C%229781783983407%22%2C%229781787121386%22%2C%229780134547046%22%2C%229781788471176%22%5D',
        'original_referer': 'direct',
        'dashboard_v10': '1',
        '_uetsid': '_uetc38f1067',
        'timezoneoffset': '-28800',
        'liveagent_sid': 'f7497b0d-1bc8-437c-8c4b-3760535ad361',
        'liveagent_vc': '12',
        '_gat': '1',
        'salesforce_id': 'a66cda34720db081f2fd5bbfa8aca4fe',
        'csrfsafari': 'Nt5l5xMYmnidXppSTKFLymizt0l3exLy',
        '_ga': 'GA1.2.1666217267.1509976252',
        '_gid': 'GA1.2.801030076.1509976252',
        'logged_in': 'y',
        'sessionid': 'tbu07z4899d20pbgv4yqt8xrryl8xcbc'
    }
    sess = requests.Session()
    sess.cookies = requests.utils.cookiejar_from_dict(cookies)
    # r = sess.get(url=url,headers=headers,)
    # print(r.text)
    url_list = sys.argv[1:]
    for url in url_list:
        main(url)
import requests,os,sys,re
from multiprocessing import Pool,cpu_count
from bs4 import BeautifulSoup

class safari_crawler(object):
    
    def __init__(self,url):
        self.url = url
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,ja;q=0.6',
        'cache-control': 'max-age=0',
        'referer': 'https://www.safaribooksonline.com/',
    }
        self.cookies = cookies = {
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
        self.sess = requests.Session()
        self.sess.cookies = requests.utils.cookiejar_from_dict(self.cookies)
        self.pool = Pool(cpu_count())

    def save_html_to_file(self, sess, url, index):

        print("进程%s正在运行" % os.getpid())
        print('当前目录为%s' % os.path.abspath('.'))

        r = sess.get(url,headers=self.headers)
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

    def run(self):
        r = self.sess.get(url=self.url,headers=self.headers,)
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
            print(chapter)
            # self.pool.apply_async(save_html_to_file,args=(self.sess,chapter,index + 2,headers=self.headers,))
            self.save_html_to_file(self.sess,chapter,index + 2)
        self.pool.close()
        print('等待全部进程结束')
        self.pool.join()
        os.chdir('..')
        print('全部进程结束')


if __name__ == '__main__':
    url_list = sys.argv[1:]
    for url in url_list:
        safari_crawler(url).run()


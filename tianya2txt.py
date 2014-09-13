#!python
#-*- coding=utf-8 -*-
import sys
import urllib2
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool


reload(sys)
sys.setdefaultencoding('utf8')

def get_soup(url):
    req = urllib2.Request(url, headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'})
    html = urllib2.urlopen(req)
    soup = BeautifulSoup(html)
    return soup

def get_post_info(url):
    start_page = re.search(r'-(\d+).shtml', url).group(1)
    url = url = re.sub(r'-\d+.shtml', '-1.shtml', url)
    soup = get_soup(url)
    #get post subject as file_name
    subject = soup.find('span', {'class':'s_title'}).findChildren('span')[0].text
    file_name = subject.strip(' ')+start_page+'.txt'
    file_name = file_name.replace(' ','')
    file_name = file_name.replace('?','')
    file_name = file_name.replace('/','')
    file_name = file_name.replace('\\','')
    file_name = file_name.replace(':','')
    #get page count from navigation form
    forms = soup.find_all('form')
    if len(forms) == 1:
        page_amount = 1
    else:
        form_a = forms[1].findChildren('a')[-2]
        page_amount = int(form_a.text)
    return (file_name, page_amount)

def get_page_content(params):
    (url, page) = params
    url = re.sub(r'-\d+.shtml', '-'+str(page)+'.shtml', url)
    print u'正在获取第{}页'.format(page)
    page_content = ''
    soup = get_soup(url)
    items = soup.find_all('div', class_='atl-item')
    reply_id = int(items[-1]['id'])
    for item in items:
        if item.findChildren('div', class_='atl-head') == [] or item.findChildren('strong', class_='host') != []:
            post = item.findChildren('div', class_='bbs-content')[0]
            post_content =  post.text
            if re.search(r'\d+-\d+-\d+\s\d+:\d+:\d+', post_content) != None:
                continue
            post_content = re.sub(r'\t+|(<br>)+|(<\/br>)+', '', post_content)
            post_content = re.sub(u'\u3000+', "\n", post_content)
            page_content += post_content
    return (page_content, reply_id)


if __name__ == '__main__':
    #get url from user input
    print u'''
    ------------------------------------
    *天涯帖子脱水爬虫*
    用途：保存脱水后的天涯帖子到txt文件
    用法：输入天涯帖子地址，比如http://bbs.tianya.cn/post-16-1008143-1.shtml
    说明：如果输入的地址不是第一页，则会从该页开始获取
    -------------------- ----------------
    '''
    print u"请输入天涯帖子的地址："
    url = raw_input()
    #test if input URL is correct
    while re.match(r'http:\/\/bbs.tianya.cn\/post-[0-9a-zA-Z]+-\d+-\d+.shtml', url) == None:
        print u"帖子地址不正确，重新输入："
        url = raw_input()

    page = int(re.search(r'-(\d+).shtml', url).group(1))
    file_name, page_amount= get_post_info(url)
    print u"共{}页，将从第{}页开始获取".format(page_amount, page)


    post_content = ''

    pool = Pool(processes = 4)
    params = [(url, page) for page in range(page, page_amount+1)]
    post_result= pool.map(get_page_content, params)
    post_content_result = []
    latest_reply_result = []
    for post_content, latest_reply in post_result:
        post_content_result.append(post_content)
        latest_reply_result.append(latest_reply)
    pool.close()
    pool.join()

    post_content_result = ''.join(post_content_result)
    latest_reply_result = max(latest_reply_result)
    latest_mark = u"已获取到最新楼层数：{}".format(latest_reply_result)

    with open(file_name, 'w+') as f:
        print u"正在保存文件到：{}".format(file_name)
        f.write(post_content_result)
    
    with open(file_name, 'a') as f:
        print latest_mark
        f.write(latest_mark)

    print u"完成！"
        
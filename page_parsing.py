import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
project_58 = client['project_58']
url_list = project_58['url_list']
item_info = project_58['item_info']

def get_links_from(channel,pages,who_sells=0):
    #http://bj.58.com/diannao/0/pn3/
    list_view = '{}/{}/pn{}/'.format(channel,str(who_sells),str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('td.t a.t')
    if soup.find('td','t'):
        for link in links:
            item_list = link.get('href').split('?')[0]
            data = {
                'url':item_list,
            }
            url_list.insert_one(data)
    else:
        pass#nothing


def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    no_longer_exist = '404' in soup.find('script',type='text/javascript').get('src').split('/')
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('div.su_con > span.price.c_f50')[0].text
        date = soup.select('ul.mtit_con_left.fl > li.time')[0].text
        area = list(soup.select('.c_25d > a')[0].stripped_strings) if soup.find_all('span','c_25d') else None
        data = {
            'title':title,
            'price':price,
            'date':date,
            'area':area,
        }
        item_info.insert_one(data)
        print(data)



#get_links_from('http://bj.58.com/diannao','3')
get_item_info('http://bj.58.com/pingbandiannao/33607951479884x.shtml')
from selenium import webdriver
import time
import pymongo
from lxml import etree                                                  #导入相应的库文件

client = pymongo.MongoClient('localhost',27017)                         #连接数据库
mydb = client['mydb']
taobao = mydb['taobao']                                                 #创建数据库和数据集合

driver = webdriver.Chrome()                                              #选择谷歌浏览器
driver.maximize_window()                                                 #浏览器窗口最大化

def get_info(url,page):
    page = page + 1
    driver.get(url)
    driver.implicitly_wait(10)                                           #隐式等待10秒
    selector = etree.HTML(driver.page_source)                            #请求网页源代码
    infos = selector.xpath('//div[@class="item J_MouserOnverReq  "]')
    for info in infos:
        data = info.xpath('div/div/a')[0]
        goods = data.xpath('string(.)').strip()
        price = info.xpath('div/div/div/strong/text()')[0]
        sell = info.xpath('div/div/div[@class="deal-cnt"]/text()')[0]
        '''差一个断点测试
            解决办法try判断是否列表越界
            由于今天太累明天再debug
        '''
        #//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]
        #//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]
        shop = info.xpath('div[2]/div[3]/div[1]/a/span[2]/text()')[0]
        address = info.xpath('div[2]/div[3]/div[2]/text()')[0]
        commodity = {
            'good':goods,
            'price':price,
            'sell':sell,
            'shop':shop,
            'address':address
        }
        taobao.insert_one(commodity)                                    #数据插入数据库

    if page <= 50 :
        NextPage(url,page)
    else:
        pass                                                            #进入下一页

def NextPage(url,page):                                                 #顶一下一页函数
    driver.get(url)
    driver.implicitly_wait(10)                                          #隐式等待10秒
    driver.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()   #定位
    time.sleep(4)
    driver.get(driver.current_url)
    driver.implicitly_wait(10)
    get_info(driver.current_url,page)                                   #调用get_info()函数

if __name__ == '__main__':                                             #程序入口
    name = input('请输入你需要爬取的商品名字：')
    page = 1
    url = 'https://www.taobao.com/'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_id('q').clear()
    driver.find_element_by_id('q').send_keys(name)                #输入商品名字
    driver.find_element_by_class_name('btn-search').click()             #单击搜索
    get_info(driver.current_url,page)




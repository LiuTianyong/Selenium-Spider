from selenium import webdriver
import time
import csv
import pymongo                                                          #导入相应的头文件

client = pymongo.MongoClient('localhost',27017)                         #连接数据库
mydb = client['mydb']
qq_shuo = mydb['meituan']                                               #创建数据库和数据集合

driver = webdriver.Chrome()                                              #选择谷歌浏览器
driver.maximize_window()                                                 #窗口最大化


def get_info(url):
    driver.get(url)
    driver.implicitly_wait(10)  # 隐式等待10秒
    name = driver.find_element_by_class_name('d-left')



if __name__ == '__main__':
    urls = ['http://cd.meituan.com/meishi/c11/','http://cd.meituan.com/meishi/c17/',
            'http://cd.meituan.com/meishi/c40/','http://cd.meituan.com/meishi/c36/',
            'http://cd.meituan.com/meishi/c28/','http://cd.meituan.com/meishi/c35/',
            'http://cd.meituan.com/meishi/c395/','http://cd.meituan.com/meishi/c54/',
            'http://cd.meituan.com/meishi/c20003/','http://cd.meituan.com/meishi/c55/',
            'http://cd.meituan.com/meishi/c56/','http://cd.meituan.com/meishi/c20004/',
            'http://cd.meituan.com/meishi/c57/','http://cd.meituan.com/meishi/c400/',
            'http://cd.meituan.com/meishi/c58/','http://cd.meituan.com/meishi/c41/',
            'http://cd.meituan.com/meishi/c59/','http://cd.meituan.com/meishi/c60/',
            'http://cd.meituan.com/meishi/c62/','http://cd.meituan.com/meishi/c63/',
            'http://cd.meituan.com/meishi/c217/','http://cd.meituan.com/meishi/c227/',
            'http://cd.meituan.com/meishi/c228/','http://cd.meituan.com/meishi/c229/',
            'http://cd.meituan.com/meishi/c232/','http://cd.meituan.com/meishi/c233/',
            'http://cd.meituan.com/meishi/c24/']
    for url in urls:
        get_info(url)
        time.sleep(5)



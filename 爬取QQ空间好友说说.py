from selenium import webdriver
import time
import csv
import pymongo                                                          #导入相应的头文件

client = pymongo.MongoClient('localhost',27017)                         #连接数据库
mydb = client['mydb']
qq_shuo = mydb['qq_shuo']                                               #创建数据库和数据集合

driver = webdriver.Chrome()                                              #选择谷歌浏览器
driver.maximize_window()                                                 #窗口最大化

def get_info(name,qq):
    driver.get('https://user.qzone.qq.com/{}/311'.format(qq))
    driver.implicitly_wait(10)                                            #隐式等待10秒
    try:                                                                  #判断是否需要登陆 如果需要跳入登陆框架
        driver.find_element_by_id('login_div')                           #查找login_div标签判断是否需要登陆
        a = True
    except:
        a = False
    if a == True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()                            #清空输入框内容
        driver.find_element_by_id('u').send_keys('1063331689')           #输入账号
        driver.find_element_by_id('p').clear()                            #清空输入框
        driver.find_element_by_id('p').send_keys('xiaoyuv587,,')         #输入密码
        driver.find_element_by_id('login_button').click()
        time.sleep(2)
    driver.implicitly_wait(3)                                               #登陆QQ
    try:
        driver.find_element_by_id('aOwnerFeeds')                           #判断是否有访问权限
        '''
        笔记:
            find_element_by_id 和 find_elements_by_id 区别：
            find_element_by_id：一般是id  一般存在于class后 无 .
            find_elements_by_id：一般是class 一般标签前有.  如 .content
        '''
        #<i class="ui-icon icon-homepage"></i>
        # <a href="javascript:;" id="aOwnerFeeds"><i class="ui-icon icon-feeds"></i><span>他的动态</span></a>
        b = True
    except:
        b = False
    if b == True:
        driver.switch_to.frame('app_canvas_frame')
        comtents = driver.find_elements_by_css_selector('.content')
        times = driver.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')

        #<a class="c_tx c_tx3 goDetail

        '''#测试段
        for tim in times:
            print(tim)
            print('测试行')
        '''
        for comtent,tim in zip(comtents,times):
            print('正在爬取{}的说说'.format(name))
            data = {
                'name':name,
                'time':tim.text,
                'comtent':comtent.text
            }
            #print(data)                                                    #测试行
            qq_shuo.insert_one(data)                                        #获取到的说说信息插入数据库
            print('爬取完毕')

if __name__ == '__main__':                                                 #程序入口
    qq_list = []
    qq_list_name = []
    fp = open('QQ好友列表.csv','r',encoding='utf-8')
    reader = csv.DictReader(fp)
    for row in reader:
        qq_list.append(row['电子邮件'].split('@')[0])                       #存入QQ账号
        qq_list_name.append(row['First Name'])                                     #存入姓名
    fp.close()
    for name,item in zip(qq_list_name,qq_list):
        get_info(name,item)

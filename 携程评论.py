from selenium import webdriver
import re
import csv
import time

driver = webdriver.Chrome()                                              #选择谷歌浏览器
driver.maximize_window()                                                 #浏览器窗口最大化

fp = open('上海携程/上海携程2.csv','wt',newline='',encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('酒店名字','星级','地理位置','点评数量','用户推荐','总评分','位置','设施','服务','卫生',
                 '点评人','用户等级','点评内容','点评回复','用户评分','有用数','出游类型','出游时间'))

def callback(driver):
    # 酒店名字
    title = driver.find_element_by_xpath('//*[@id="J_htl_info"]/div[1]/h2[1]').text
    # 星级
    starNum = driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceHolder_commonHead_imgStar"]')
    # 地理位置
    site = driver.find_element_by_xpath('//*[@id="J_htl_info"]/div[3]').text
    # 点评数量
    commentNum = driver.find_element_by_xpath('//*[@id="commentTab"]/a').text
    commentNum = re.findall('\d+', commentNum)
    # 用户推荐
    recommend = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[1]/span[4]/span').text
    # 总分
    sumNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[1]/span[3]/span').text
    # 位置得分
    siteNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[1]/span').text
    # 设施得分
    facilityNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[2]/span').text
    # 服务得分
    serverNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[3]/span').text
    # 卫生得分
    sanitationNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[4]/span').text

    '''评论区'''
    # 评论人
    for i in range(1, 16):
        # 点评内容
        comment = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/div/div[1]'.format(i)).text
        # 点评作者
        commentAuthor = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[1]/p[2]/span'.format(i)).text
        # 用户等级
        authorLv = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[3]/div[{}]/div[1]/p[4]'.format(i)).text
        authorLv = re.findall('点评总数 (\d+)', authorLv)[0]
        authorLv = int(authorLv)
        if authorLv <= 4:
            authorLv = '点评新星'
        elif authorLv >= 5 and authorLv <= 29:
            authorLv = '点评达人'
        else:
            authorLv = '点评专家'
        print(authorLv)
        # 用户评分
        authorCommentSumNum = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/p/span[2]/span'.format(i)).text
        print(authorCommentSumNum)
        # 用户各项评分

        # 有用数
        # //*[@id="divCtripComment"]/div[4]/div[1]/div[2]/div/div[3]/a/span
        # //*[@id="divCtripComment"]/div[4]/div[2]/div[2]/div/div[3]/a/span
        # //*[@id="divCtripComment"]/div[4]/div[4]/div[2]/div[1]/div[2]/a/span
        # //*[@id="divCtripComment"]/div[4]/div[6]/div[2]/div/div[3]/a/span
        try:
            useNum = driver.find_element_by_xpath(
                '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/div/div[3]/a/span'.format(i)).text
        except:
            useNum = 0
        # 出游类型
        goType = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/p/span[4]'.format(i)).text
        # 发布时间
        commentTime = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/p/span[3]'.format(i)).text

        try:
            commentReply = driver.find_element_by_xpath(
                '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/div[2]/p[2]'.format(i)).text
            writer.writerow((title, starNum, site, commentNum, commentAuthor, recommend, sumNum, siteNum, facilityNum,
                             serverNum, sanitationNum,
                             commentAuthor, authorLv, comment, commentReply, authorCommentSumNum, useNum, goType,
                             commentTime))
            print((title, starNum, site, commentNum, commentAuthor, recommend, sumNum, siteNum, facilityNum,
                             serverNum, sanitationNum,
                             commentAuthor, authorLv, comment, commentReply, authorCommentSumNum, useNum, goType,
                             commentTime))
        except:
            print(title, starNum, site, commentNum, commentAuthor, recommend, sumNum, siteNum, facilityNum,
                             serverNum, sanitationNum,
                             commentAuthor, authorLv, comment, '无回复', authorCommentSumNum, useNum, goType,
                             commentTime)
            writer.writerow((title, starNum, site, commentNum, commentAuthor, recommend, sumNum, siteNum, facilityNum,
                             serverNum, sanitationNum,
                             commentAuthor, authorLv, comment, '无回复', authorCommentSumNum, useNum, goType,
                             commentTime))

def info(url):
    driver.get(url)
    driver.implicitly_wait(10)

    # 酒店名字
    title = driver.find_element_by_xpath('//*[@id="J_htl_info"]/div[1]/h2[1]').text
    # 星级
    starNum = driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceHolder_commonHead_imgStar"]')
    # 地理位置
    site = driver.find_element_by_xpath('//*[@id="J_htl_info"]/div[3]').text
    # 点评数量
    commentNum = driver.find_element_by_xpath('//*[@id="commentTab"]/a').text
    commentNum = re.findall('\d+', commentNum)
    # 用户推荐
    recommend = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[1]/span[4]/span').text
    # 总分
    sumNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[1]/span[3]/span').text
    # 位置得分
    siteNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[1]/span').text
    # 设施得分
    facilityNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[2]/span').text
    # 服务得分
    serverNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[3]/span').text
    # 卫生得分
    sanitationNum = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[1]/div[2]/p[4]/span').text

    '''评论区'''
    # 评论人
    for i in range(1, 16):
        # 点评内容
        #//*[@id="divCtripComment"]/div[3]/div[1]/div[2]/div/div[1]/text()
        comment = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/div/div[1]'.format(i)).text
        # 点评作者
        #//*[@id="divCtripComment"]/div[3]/div[1]/div[1]/p[2]/span
        commentAuthor = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[1]/p[2]/span'.format(i)).text
        # 用户等级
        authorLv = driver.find_element_by_xpath('//*[@id="divCtripComment"]/div[3]/div[{}]/div[1]/p[4]'.format(i)).text
        authorLv = re.findall('点评总数 (\d+)', authorLv)[0]
        authorLv = int(authorLv)
        if authorLv <= 4:
            authorLv = '点评新星'
        elif authorLv >= 5 and authorLv <= 29:
            authorLv = '点评达人'
        else:
            authorLv = '点评专家'
        print(authorLv)
        # 用户评分
        authorCommentSumNum = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/p/span[2]/span'.format(i)).text
        print(authorCommentSumNum)
        # 用户各项评分

        # 有用数
        # //*[@id="divCtripComment"]/div[4]/div[1]/div[2]/div/div[3]/a/span
        # //*[@id="divCtripComment"]/div[4]/div[2]/div[2]/div/div[3]/a/span
        # //*[@id="divCtripComment"]/div[4]/div[4]/div[2]/div[1]/div[2]/a/span
        # //*[@id="divCtripComment"]/div[4]/div[6]/div[2]/div/div[3]/a/span
        try:
            useNum = driver.find_element_by_xpath(
                '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/div/div[3]/a/span'.format(i)).text
        except:
            useNum = 0
        # 出游类型
        goType = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/p/span[4]'.format(i)).text
        # 发布时间
        commentTime = driver.find_element_by_xpath(
            '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/p/span[3]'.format(i)).text

        try:
            commentReply = driver.find_element_by_xpath(
                '//*[@id="divCtripComment"]/div[3]/div[{}]/div[2]/div[2]/p[2]'.format(i)).text
            writer.writerow((title, starNum, site, commentNum, commentAuthor, recommend, sumNum, siteNum, facilityNum,
                             serverNum, sanitationNum,
                             commentAuthor, authorLv, comment, commentReply, authorCommentSumNum, useNum, goType,
                             commentTime))
        except:
            print(comment)
            writer.writerow((title, starNum, site, commentNum, commentAuthor, recommend, sumNum, siteNum, facilityNum,
                             serverNum, sanitationNum,
                             commentAuthor, authorLv, comment, '无回复', authorCommentSumNum, useNum, goType,
                             commentTime))
    time.sleep(5)
    print('点击')
    #driver.find_element_by_link_text('下一页').click()


    for i in range(0,20):
        print('**********************************************************************************************')
        time.sleep(5)
        callback(driver)

if __name__ == '__main__':                                             #程序入口
    url = 'http://hotels.ctrip.com/hotel/8052290.html?isFull=F#ctm_ref=hod_sr_lst_dl_n_1_3'
    info(url)
    fp.close()
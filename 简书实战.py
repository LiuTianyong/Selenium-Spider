from selenium import webdriver                                  #导入相应的库文件
import pymongo

client = pymongo.MongoClient('localhost',27017)                 #连接本地数据库
mydb = client['mydb']
test = mydb['test']

url = 'http://www.jianshu.com/p/c9bae3e9e252'
def get_info(url):                                               #定义获取信息函数
    include_title = []                                           #初始化列表，存入收录专题信息
    driver = webdriver.Chrome()                                  #指定谷歌浏览器
    s = driver.get(url)
    print('*****',s)
    driver.implicitly_wait(20)                                   #隐式等待20秒
    author = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/div/span/a').text
    data = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/div/div/span[1]').text
    word = driver.find_element_by_xpath('//span[@class="wordage"]').text
    view = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/img')
    comment = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/p[2]').text
    #like = driver.find_element_by_xpath('span[@class="like-count"]').text  
    #included_names = driver.find_element_by_xpath('//span[@class="include-collection"]/a/div')
    #for i in word:
        #include_title.append(i.text)                              #获取数据
    print(author,data,word,view,comment,include_title)       #打印数据
    test.insert_one({'author': author, 'data': data, 'word': word,'coment':comment})  # 插入数据
if __name__ == '__main__':
    get_info(url)

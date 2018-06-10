#测试代码运行时间
import datetime
import re
import json
import requests
#多进程应用 ,进程池
from multiprocessing import Pool
#捕获异常
from requests.exceptions import RequestException

def get_one_page(url):
    #简单的用手机响应头请求
    headers = {"user-agent":'my-app/0.0.1'}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # 爬取 序号 ，图片链接，主演，上映时间，
    #正则匹配要的是括号里面的
    #爬取的内容条 匹配内容出现换行，还有空间的问题如何处理？
    patter = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                        +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                        +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(patter,html)
    for item in items:
        #对爬取到的数据列表进行切片,并且转换为字典形式
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        #把字典形式再转换成字符串的形式
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
#构造连续的url
def main(offset):
    url = "http://maoyan.com/board/4?offset=" +str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

start = datetime.datetime.now()

#执行主程序
if __name__ =="__main__":
    #方案一：没有使用多进程   运行时间：0:00:37.417583
    # for i in range(10):
    #     main(i*10)

    #方案二：使用多进程   运行时间：0:00:21.338314
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])

end = datetime.datetime.now()
print(100*"-")
print(end-start)
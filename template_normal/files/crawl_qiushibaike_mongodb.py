import queue
import requests
from lxml import etree
import threading
from pymongo import MongoClient

class crawl_qiushi:

    def __init__(self):
        self.init_url = "https://www.qiushibaike.com/text/page/{}/"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
        self.url_queue = queue.Queue(10)
        self.html_ret_queue = queue.Queue(10)
        self.html_content_queue = queue.Queue(10)
        self.client = MongoClient(host = "127.0.0.1",port = 27017)
        self.collection = self.client["my_test"]["crawl_qiushibaike"]

    def get_url_queue(self):
        for i in range(1,14):
            self.url_queue.put(self.init_url.format(i))

    def send_url_request(self):
        while True:
            url = self.url_queue.get()
            html_ret = requests.get(url,headers = self.headers)
            self.html_ret_queue.put(html_ret.content.decode("utf-8"))
            self.url_queue.task_done()

    def process_html_ret(self):
        while True:
            html_content = self.html_ret_queue.get()
            html_content = etree.HTML(html_content)
            div_list = html_content.xpath("//div[contains(@class,'article block')]")#div对象的列表
            content_list = list()
            for div in div_list:#对每个div对象
                item = {}
                item["content"] = div.xpath("//div[@class='content']/span/text()") if len(div.xpath("//div[@class='content']/span/text()"))>0 else None#因为有br列表中的元素不止一个，所以直接返回一个列表
                item["user"]= div.xpath("//h2/text()")[0] if len(div.xpath("//h2/text()"))>0 else None
                content_list.append(item)#content_list中放的是一页中所有需要的内容,里面每个元素是字典,字典中存放的是每个div中我们爬取的内容
            self.html_content_queue.put(content_list)
            self.html_ret_queue.task_done()

    def save_content(self):
        while True:
            content = self.html_content_queue.get()#获得的是每一页的内容
            self.collection.insert_many(content)
            self.html_content_queue.task_done()

    def run(self):
        tpool = list()
        t1 = threading.Thread(target=self.get_url_queue)
        tpool.append(t1)
        t2 = threading.Thread(target=self.send_url_request)
        tpool.append(t2)
        t3 = threading.Thread(target=self.process_html_ret)
        tpool.append(t3)
        t4 = threading.Thread(target=self.save_content)
        tpool.append(t4)

        for t in tpool:
            t.setDaemon(True)# 将子线程设置为守护线程，主线程结束，子线程结束
            t.start()

        for p in [self.url_queue,self.html_ret_queue,self.html_content_queue]:
            p.join()#队列将主进程阻塞住，当队列为空时，就不阻塞了,主进程执行结束，子线程从而结束
if __name__ == '__main__':
    crawl_qiushi().run()


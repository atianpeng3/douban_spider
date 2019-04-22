from parse import parse_url
import json
from  douban_movie_info_spider import Douban_movie_spider
class DoubanSpider:


    def __init__(self):
        self.temp_url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=2015,%E7%94%B5%E5%BD%B1&start={}"
        self.movie_info_spider = Douban_movie_spider()

    def get_contentf_list(self,html_str):#提取数据
        #print(html_str)
        dict_data = json.loads(html_str)
        content_list = dict_data['data']
        return content_list

    def save_url_list(self,content_list,url_list):

        for content in content_list:
            url_list.append(content['url'])

        #print("保存成功")
        return url_list

    def save_content_list(self,url_list):
        for i in range(0,len(url_list)):
            self.movie_info_spider.run(url_list[i])
            print(i)
        #print("保存成功")

    def run(self):#实现主要逻辑
        url_list = []
        num = 0
        total = 1000
        while num < total:
            #1.start_url
            url = self.temp_url.format(num)
            #print(url)
            #2.发送请求，获取响应
            html_str = parse_url(url)
            #3.提取数据
            content_list= self.get_contentf_list(html_str)
            #4.保存
            self.save_url_list(content_list,url_list)
            #5.构造下一页的URL地址，循环2-5部
            num += 20
            print("************************已经成功爬取%d条数据*************************"%(num))
        print(url_list)
        self.save_content_list(url_list)


if __name__ == '__main__':
    douban = DoubanSpider()
    douban.run()
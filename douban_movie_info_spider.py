import requests,csv
from lxml import etree
import json

class Douban_movie_spider:


    def __init__(self):
        self.url_temp = "https://movie.douban.com/subject/27060077/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}


    def parse_url(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content.decode()

    def get_movie_inf(self,html_str,extern_url):#3.提取数据
        html = etree.HTML(html_str)
        movie_inf = {}
        movie_actor = {}
        movie_inf_list = []
        movie_actor_list = []
        #电影名称
        movie_inf["title"] = html.xpath("//span[@property = 'v:itemreviewed']/text()")[0]
        movie_inf_list.append(movie_inf["title"])
        print(movie_inf_list[0])
        #电影链接
        movie_inf["url"] = extern_url
        movie_inf_list.append(movie_inf["url"])
        movie_actor["url"] = extern_url
        movie_actor_list.append(movie_inf["url"])
        #电影海报
        movie_inf["img"] = html.xpath("//a[@class = 'nbgnbg']/img/@src")[0]
        movie_inf_list.append(movie_inf["img"])
        #电影导演
        movie_inf["daoyan"] = html.xpath("//a[@rel = 'v:directedBy']/text()")[0]
        movie_inf_list.append(movie_inf["daoyan"])
        #电影演员
        #******************************************************************************************
        movie_actor["yanyuan_list"] = html.xpath("//a[@rel = 'v:starring']/text()")
        movie_actor_list.extend(movie_actor["yanyuan_list"])
        #******************************************************************************************
        #电影类型
        movie_inf["leixing"] = html.xpath("//span[@property = 'v:genre']/text()")[0]
        movie_inf_list.append(movie_inf["leixing"])
        #电影上映时间
        movie_inf["shangying_time"] = html.xpath("//span[@property = 'v:initialReleaseDate']/text()")[0][0:10]
        movie_inf_list.append(movie_inf["shangying_time"])
        #电影国家和语言
        movie = {}
        movie["info"] = html.xpath("//div[@id = 'info']/text()")
        i = 0
        for temp in movie["info"]:
            if len(temp.replace("\\", "").replace("/", "").strip()) != 0:
                if i == 0:
                    movie_inf["guojia"] = temp.strip().split("/")[0]
                    movie_inf_list.append(movie_inf["guojia"])
                    i = i + 1
                elif i == 1:
                    movie_inf["yuyan"] = temp.strip().split("/")[0]
                    movie_inf_list.append(movie_inf["yuyan"])
                    i = i + 1
        #电影评分
        movie_inf["pingfen"] = html.xpath("//strong/text()")[0]
        movie_inf_list.append(movie_inf["pingfen"])
        #电影评论人数
        movie_inf["pingjia_renshu"] = html.xpath("//span[@property = 'v:votes']/text()")[0]
        movie_inf_list.append(movie_inf["pingjia_renshu"])

        return movie_inf_list,movie_actor_list

    def save_content_list(self,movie_inf,movie_actor):
        with open("豆瓣电影2015.csv", 'a+', encoding='utf_8_sig', newline='') as file:  # 文件路径
            writer = csv.writer(file)
            writer.writerow(movie_inf)
        with open("豆瓣电影_演员2015.csv", 'a+', encoding='utf_8_sig', newline='') as file:  # 文件路径
            writer = csv.writer(file)
            writer.writerow(movie_actor)


    def run(self,extern_url):#实现主要逻辑

        #1.根据URL地址的规律，构造url_list
        url = extern_url
        #2.发送请求，获取响应

        html_str = self.parse_url(url)
        #3.提取数据
        movie_inf,movie_actor = self.get_movie_inf(html_str,extern_url)
        #print(movie_inf)
        #4.保存
        self.save_content_list(movie_inf,movie_actor)

if __name__ == '__main__':
    douban = Douban_movie_spider()
    douban.run()

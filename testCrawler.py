import requests
import time
import pandas as pd
import random
from lxml import etree
from io import BytesIO
import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image



class nezha():
    def __init__(self):
        
        self.session = requests.session()
        
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

        self.url_login = 'https://www.douban.com/login'
        
        self.url_comment = 'https://movie.douban.com/subject/26794435/comments?start=%d&limit=20&sort=new_score&status=P'

    def scrapy_(self):
        
        login_request = self.session.get(self.url_login, headers=self.headers)
        
        selector = etree.HTML(login_request.content)
        
        post_data = {'source': 'None',  
                     'redir': 'https://www.douban.com',  
                     'form_email': '18290243328',
                     'form_password': '1996611zjj',
                     'login': '登录'}  
        
        captcha_img_url = selector.xpath('//img[@id="captcha_image"]/@src')
        
        if captcha_img_url != []:
            
            pic_request = requests.get(captcha_img_url[0])
            
            img = Image.open(BytesIO(pic_request.content))
            img.show()
            
            string = input('请输入验证码：')
            post_data['captcha-solution'] = string
            
            captcha_id = selector.xpath('//input[@name="captcha-id"]/@value')
            
            post_data['captcha-id'] = captcha_id[0]
        
        self.session.post(self.url_login, data=post_data)
        print('已登录豆瓣')

        
        
        users = []
        stars = []
        times = []
        comment_texts = []
        
        for i in range(0, 1, 20):
            
            data = self.session.get(self.url_comment % i, headers=self.headers)
            
            print('进度', i, '条', '状态是：',data.status_code)
            
            time.sleep(random.random())
            
            selector = etree.HTML(data.text)
            
            comments = selector.xpath('//div[@class="comment"]')
            
            for comment in comments:
                
                user = comment.xpath('.//h3/span[2]/a/text()')[0]
                
                star = comment.xpath('.//h3/span[2]/span[2]/@class')[0][7:8]
                
                date_time = comment.xpath('.//h3/span[2]/span[3]/@title')
                
                if len(date_time) != 0:
                    date_time = date_time[0]
                else:
                    date_time = None
                
                comment_text = comment.xpath('.//p/span/text()')[0].strip()
                
                users.append(user)
                stars.append(star)
                times.append(date_time)
                comment_texts.append(comment_text)
        
        comment_dic = {'user': users, 'star': stars, 'time': times, 'comments': comment_texts}
        comment_df = pd.DataFrame(comment_dic)  
        comment_df.to_csv('duye_comments.csv')  
        comment_df['comments'].to_csv('comment.csv', index=False)  
        print(comment_df)

    def jieba_(self):
        
        content = open('comment.csv', 'r', encoding='utf-8').read()
        
        word_list = jieba.cut(content)
        
        with open('自定义词.txt') as f:
            jieba.load_userdict(f)
        
        word = []
        
        for i in word_list:
            with open('停用词库.txt') as f:
                meaningless_file = f.read().splitlines()
                f.close()
            if i not in meaningless_file:
                word.append(i.replace(' ', ''))
        
        global word_cloud
        
        word_cloud = '，'.join(word)
        print(word_cloud)

    def word_cloud_(self):
        
        cloud_mask = np.array(Image.open('nezha.jpg'))
        
        wc = WordCloud(
            background_color="white",  
            mask=cloud_mask,  
            max_words=300,  
            font_path='./fonts/simhei.ttf',
            min_font_size=5,
            max_font_size=100,  
            width=400  
        )
        global word_cloud
        
        x = wc.generate(word_cloud)
        
        image = x.to_image()
        
        image.show()
        
        wc.to_file('pic.png')


nezha = nezha()

nezha.scrapy_()

nezha.jieba_()

nezha.word_cloud_()
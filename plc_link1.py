#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd 
import numpy as np 
import requests
import urllib.request
import time
import datetime


# In[5]:


path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get('https://control.com/forums/forums/human-machine-interface-hmi.8/')
html = driver.page_source
soup = bs(html, 'lxml')
print(soup)


# In[6]:


driver.close()


# In[8]:


topics = soup.find_all('div',class_="structItem-cell structItem-cell--main")
topics


# In[9]:


topics[0].find('a').text


# In[10]:


topics[0].text


# In[11]:


topics[0].find('a',class_="").get('href')


# In[12]:


driver1 = webdriver.Chrome(path)
driver1.get('https://control.com/forums/threads/abb-cp676-hmi-white-screen.49644/')
html1 = driver1.page_source
soup1 = bs(html1, 'lxml')
print(soup1)


# In[13]:


replies = soup1.find_all('div',class_="message-cell message-cell--main")
replies


# In[14]:


len(replies)


# In[15]:


replies[0].find('div',class_="bbWrapper").find(class_="bbImage").get('src')


# In[88]:


for reply in replies:
    text =reply.find('div',class_="bbWrapper").text
    print(text)
    attached_img = reply.find('div',class_="bbWrapper").find(class_="bbImage")
    if attached_img:
        print(attached_img.get('src'))
    try :
        attached_link = reply.find('iframe').get('src')
        print(attached_link)
    except:
        pass
    print('-----------------------')
         


# In[61]:


replies[1].find('div',class_="bbWrapper").find('iframe').get('src')#.text#.get('br')


# In[2]:


print(datetime.datetime.now())


# In[8]:


topics_names = []
questions_content = []
question_img = []
replies_content = []
replies_order = []
image1 = []
video_link1  = []
topic_urls = []

print(f'start time {datetime.datetime.now()}')

for x in range(63,152):

    path = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(path)



    driver.get(f'https://control.com/forums/forums/human-machine-interface-hmi.8/page-{x}')
    html = driver.page_source
    soup = bs(html, 'lxml')
    topics = soup.find_all('div',class_="structItem-cell structItem-cell--main")
    driver.close()
    topic_counter = 0

    for topic in topics:
        topic_counter = topic_counter+1

        title = topic.find('a').text
        topic_url = 'https://control.com' + topic.find('a',class_="").get('href')
        #print(topic_url)
        topic_url = topic_url.rstrip(topic_url[-1])
        driver1 = webdriver.Chrome(path)
        driver1.get(topic_url)
        html1 = driver1.page_source
        soup1 = bs(html1, 'lxml')
        replies = soup1.find_all('div',class_="message-cell message-cell--main")
        #print('getting topic: ' + title)
        #print(f'found {len(replies)} replies')
        question_text = replies[0].find('div',class_="bbWrapper").text
        #print(f'Topic question details : {question_text}')
        attached_q_img = replies[0].find('div',class_="bbWrapper").find(class_="bbImage")
        if attached_q_img:
            pass
            #print(attached_q_img.get('src'))
        else:
            attached_q_img = 'no_img'
            
        reply_counter = 0
        for reply in replies[1:]:
            reply_counter = reply_counter+1
            text =reply.find('div',class_="bbWrapper").text
            #print(text)
            attached_img = reply.find('div',class_="bbWrapper").find(class_="bbImage")
            if attached_img:
                pass
                #print(attached_img.get('src'))
            else:
                attached_img = 'no_img'
            try :
                attached_link = reply.find('iframe').get('src')
                #print(attached_link)
            except:
                attached_link = 'no_link'

            topics_names.append(title)
            questions_content.append(question_text)
            question_img.append(attached_q_img)
            replies_content.append(text)
            replies_order.append(reply_counter)
            image1.append(attached_img)
            video_link1.append(attached_link)
            topic_urls.append(topic_url)
            print('-----------------------')
        driver1.close()
        print(f'In Page : {x} , finished topic : {topic_counter} , data points :{len(topic_urls)}')
        print(datetime.datetime.now())
        time.sleep(10)

print(f'end time {datetime.datetime.now()}')


# In[3]:


len(topics_names)


# In[4]:


len(image1)


# In[26]:


attached_link


# In[27]:


video_link1.append(attached_link)
image1.append(attached_img)


# In[24]:


len(video_link1)


# In[25]:


len(image1)


# In[9]:


# first patch 1- 6 
# second patch 6- 56 , 2022-10-02 17:01:49.979878    ::  2022-10-03 00:39:47.015977
# Third patch 57- 62 , 2022-10-03 13:26:38.679141    ::  2022-10-03 14:24:16.085088
# Third patch 63- 62 , 2022-10-03 13:26:38.679141    ::  2022-10-03 14:24:16.085088


df = pd.DataFrame()
df['Topic'] = topics_names
df['question_text'] = questions_content
df['question_img'] = question_img
df['reply'] = replies_content
df['reply_rank'] = 'no_rank_in_site'
df['reply_order'] = replies_order
df['image1'] = image1
df['link1'] = video_link1


# In[10]:


df


# In[11]:


df.to_csv('pull_63_to_page_151.csv')


# In[31]:


df.to_excel('test1.xlsx')


# In[2]:


url1= 'https://control.com/forums/forums/human-machine-interface-hmi.8/'


# In[3]:


r = urllib.request.urlopen(url1)


# In[6]:


page = requests.get('https://control.com/forums/forums')
print(page.text)

soup = bs(page.content, "html.parser")


# In[8]:


s = requests.Session()
res = s.get('https://control.com/forums/forums')
cookies = dict(res.cookies)
cookies


# In[9]:


r = requests.get(
    'https://control.com/forums/forums',
    headers = {
        'User-Agent': 'Popular browser\'s user-agent',
    }
)
print(r.text)


# In[7]:


page.cookies


# In[14]:


page = requests.get('https://support.industry.siemens.com/forum/US/en/threads/132/?page=0&pageSize=10')
print(page.text)

soup = bs(page.content, "html.parser")


# In[16]:


page = requests.get('https://support.industry.siemens.com/forum/US/en/posts/backup-eprom-data/284667/?page=0&pageSize=10')
print(page.text)

soup = bs(page.content, "html.parser")


# In[ ]:





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
import re
import logging


# In[2]:


url = "https://support.industry.siemens.com/forum/US/en/conf/"


# In[3]:


page = requests.get(url)
print(page.text)

soup = bs(page.content, "html.parser")
page.close()


# In[4]:


topics1 = soup.find_all('tr',class_="conferencePadding conference evenOdd")
topics2= soup.find_all('tr',class_="conferencePadding conference evenOdd zebra")
topics = topics1 + topics2
len(topics)


# In[5]:


links = []
for topic in topics:
    link = topic.find('a').get('href')
    link = 'https://support.industry.siemens.com' + link
    if 'requestmembership' in link:
        pass
    else:
        links.append(link)
    
links
# 'https://support.industry.siemens.com/forum/US/en/conference/requestmembership/333/' == Process Control System SIMATIC PCS neo
# this requires membership 


# In[6]:


#link1 - first conf is done


# In[7]:


conf_titles = []
topics_titles =[]
q_titles = []
q_texts = []
q_hyper_link_titles = []
q_hyper_links = [] 

q_imgs = []
q_attachs = []
q_rates = []
q_votes = []

hyper_link_titles = []
hyper_links = [] 
r_rates = []
r_votes=[]
r_texts = []
r_orders = []

imgs = []
attachs = []
# adding 1 to acount for done links 
link_counter = 13 
error_counter = 0 


# In[ ]:




print(f'start time {datetime.datetime.now()}')
while link_counter < 67:
    try:
        for link in links[link_counter:14]:
            link_counter  = link_counter + 1 

            page1 = requests.get(link)
            soup1 = bs(page1.content, "html.parser")
            lasts = soup1.find_all('dd',class_="last")
            if len(lasts)>0:
                last = lasts[0].find('a').get('href')
                result = re.search('page=(.*)&pageSize', last)
                total_pages = int(result.group(1))
            else:
                total_pages = 0

            conf_title = soup1.find_all('div',style ="display:block")[0].find('h1').text[10:-7]

            page1.close()

            time.sleep(10)
            
            #change according to your stop
            page_counter = 834
            
            while page_counter < total_pages+1:
                try:
                    for page in range(page_counter, total_pages+1):
                        page_counter = page_counter + 1

                        current_page = f'page={str(page)}'
                        link_page = link.replace('page=0' , current_page)

                        page2 = requests.get(link_page)
                        soup2 = bs(page2.content, "html.parser")
                        topic_qs1 = soup2.find_all('tr',class_="conferencePadding thread evenOdd")
                        topic_qs2 = soup2.find_all('tr',class_="conferencePadding thread evenOdd zebra")
                        topic_qs = topic_qs1 + topic_qs2

                        topic_qs_links = []
                        for topic in topic_qs:
                            t_link = topic.find('a').get('href')
                            t_link = 'https://support.industry.siemens.com' + t_link
                            if 'requestmembership' in t_link:
                                pass
                            else:
                                topic_qs_links.append(t_link)
                        topic_counter = 0 

                        page2.close()

                        time.sleep(10)

                        for t_l in topic_qs_links:
                            topic_counter = topic_counter + 1
                            print('----------------------------')
                            print('----------------------------')
                            print('New Topic')
                            print(t_l)
                            page3 = requests.get(t_l)

                            soup3 = bs(page3.content, "html.parser")
                            title_sec  = soup3.find('span', class_ = 'threadsubject')

                            trail = 0 

                            if title_sec :
                                title = title_sec.text
                            else:
                                while trail < 5 :
                                    try:
                                        time.sleep(300)
                                        trail = 1+trail
                                        print(f'This is trail no. : {trail}')
                                        page3 = requests.get(t_l)

                                        soup3 = bs(page3.content, "html.parser")
                                        title_sec  = soup3.find('span', class_ = 'threadsubject')
                                    except:
                                        pass
                                if title_sec :
                                    title = title_sec.text
                                else:
                                    title = 'odd_link'


                            print(title)
                            
                            if title !=  'odd_link':                               
                                replies = soup3.find_all('table', class_ = 'dns')
                                #print(len(replies))
                                entries_sec = soup3.find_all('div' , class_ = 'search-header')[0]
                                entries = entries_sec.find('h2').text
                                replies_pages = int(re.findall(r'\d+', entries)[0])//10
                                print('reply pages count : '+str(replies_pages))

                                if replies_pages > 0:
                                    for r_page in range(1, replies_pages+1):
                                        time.sleep(10)
                                        #print(r_page)
                                        added_l = t_l.replace('page=0' , f'page={r_page}')
                                        #print(added_l)
                                        page4 = requests.get(added_l)
                                        soup4 = bs(page4.content, "html.parser")
                                        added_replies = soup4.find_all('table', class_ = 'dns')
                                        replies =   replies + added_replies

                                q = replies[0].find('td', class_ = 'body')

                                q_text = q.text.replace('\n' , '  ')

                                q_hyper_link_title = []
                                q_hyper_link = []

                                scriptTags = replies[0].findAll('a')
                                for script in scriptTags:
                                    if script.has_attr('data-original-href'):
                                        q_hyper_link_title.append(script.text)
                                        q_hyper_link.append(script.get('href'))

                                vote_sec = replies[0].find('a' , class_ = "within flyout-ur")

                                if vote_sec:
                                    vote = replies[0].find('a' , class_ = "within flyout-ur").text
                                    q_vote = re.findall(r'\d+', vote)[0]
                                else:
                                    q_vote = 0

                                star_sec = replies[0].find('a' , class_ = "within flyout-ur")

                                if star_sec:
                                    star_rate = replies[0].find('a' , class_ = "within flyout-ur").find('img',class_ = 'stars').get('src')
                                    result = re.search('Star(.*).post.gif', star_rate)
                                    q_rate = float(result.group(1))
                                else:
                                    q_rate = 0.0

                                q = replies[0].find('td', class_ = 'body')

                                q_text = q.text.replace('\n' , '  ')

                                attach = replies[0].find('div', class_ = 'appendix add-bottom')
                                if attach:
                                    img_link = attach.find('img')
                                    if img_link:
                                        img_link = img_link.get('src')
                                        img_link = 'https://support.industry.siemens.com' +img_link
                                        q_img = img_link
                                        q_attach = attach
                                    else:
                                        q_img = 'no_img'
                                        q_attach = attach
                                else:
                                    q_img = 'no_img'
                                    q_attach = 'no_attach'

                                counter_r = 0
                                if len(replies) > 1:
                                    for r in replies[1:]:
                                        r_content = r.find('td', class_ = 'body')
                                        
                                        if r_content:
                                            counter_r = counter_r + 1
                                            attach = r.find('div', class_ = 'appendix add-bottom')
                                            if attach:
                                                img_link = attach.find('img')
                                                if img_link:
                                                    img_link = img_link.get('src')
                                                    img_link = 'https://support.industry.siemens.com' +img_link

                                                else:
                                                    img_link = 'no_img'
                                                    #imgs.append(img_link)
                                                    #attachs.append(attach)
                                            else:
                                                img_link = 'no_img'
                                                #imgs.append(img_link)
                                                attach = 'no_attach'
                                                #attachs.append(attach)
                                            scriptTags = r.findAll('a')
                                            h_links = []
                                            h_links_titles = []
                                            for script in scriptTags:
                                                if script.has_attr('data-original-href'):
                                                    h_links_titles.append(script.text)
                                                    h_links.append(script.get('href'))
                                            vote = r.find('a' , class_ = "within flyout-ur")
                                            if vote:
                                                vote = r.find('a' , class_ = "within flyout-ur").text
                                                r_vote = re.findall(r'\d+', vote)[0]
                                            else:
                                                r_vote = 0

                                            star_rate_sec = r.find('a' , class_ = "within flyout-ur")

                                            if star_rate_sec:
                                                star_rate = r.find('a' , class_ = "within flyout-ur").find('img',class_ = 'stars')

                                                if star_rate:
                                                    star_rate = r.find('a' , class_ = "within flyout-ur").find('img',class_ = 'stars').get('src')
                                                    result = re.search('Star(.*).post.gif', star_rate)
                                                    r_rate = float(result.group(1))
                                                else:
                                                    r_rate = 0 
                                            else:
                                                r_rate = 0 

                                            r_content = r.find('td', class_ = 'body')

                                            r_text = r_content.text.replace('\n' , '  ')


                                            conf_titles.append(conf_title)
                                            q_titles.append(title)
                                            q_texts.append(q_text)
                                            r_texts.append(r_text)
                                            q_hyper_link_titles.append(q_hyper_link_title)
                                            q_hyper_links.append(q_hyper_link)
                                            hyper_link_titles.append(h_links_titles)
                                            hyper_links.append(h_links)
                                            q_rates.append(q_rate)
                                            q_votes.append(q_vote)
                                            q_imgs.append(q_img)
                                            q_attachs.append(q_attach)
                                            r_rates.append(r_rate)
                                            r_votes.append(r_vote)
                                            r_orders.append(counter_r)
                                            imgs.append(img_link)
                                            attachs.append(attach) 
                                        else:
                                            pass


                                else:
                                    conf_titles.append(conf_title)
                                    q_titles.append(title)
                                    q_texts.append(q_text)
                                    r_texts.append('no_reply')
                                    q_hyper_link_titles.append(q_hyper_link_title)
                                    q_hyper_links.append(q_hyper_link)
                                    hyper_link_titles.append('no_reply')
                                    hyper_links.append('no_reply')
                                    q_rates.append(q_rate)
                                    q_votes.append(q_vote)
                                    q_imgs.append(q_img)
                                    q_attachs.append(q_attach)
                                    r_rates.append('no_reply')
                                    r_votes.append('no_reply')
                                    r_orders.append('no_reply')  
                                    imgs.append('no_reply')
                                    attachs.append('no_reply')
                            else:
                                conf_titles.append(conf_title)
                                q_titles.append(title)
                                q_texts.append(t_l)
                                r_texts.append('odd_link')
                                q_hyper_link_titles.append('odd_link')
                                q_hyper_links.append('odd_link')
                                hyper_link_titles.append('odd_link')
                                hyper_links.append('odd_link')
                                q_rates.append('odd_link')
                                q_votes.append('odd_link')
                                q_imgs.append('odd_link')
                                q_attachs.append('odd_link')
                                r_rates.append('odd_link')
                                r_votes.append('odd_link')
                                r_orders.append('odd_link')  
                                imgs.append('odd_link')
                                attachs.append('odd_link')                                



                            print(f'At Conf N. : {link_counter} , Page N. : {int(page)+1}  out of : {int(total_pages)+1} , Topic N. :{topic_counter}  out of : 10')
                            print(f'Remaining Confs : {66- link_counter} ')
                            print('-------------------------------------')
                            print(datetime.datetime.now())
                            time.sleep(10)

                            df = pd.DataFrame()
                            df['conf'] = conf_titles
                            df['question_title'] = q_titles
                            df['question_text'] = q_texts
                            df['question_rate'] = q_rates
                            df['question_vote_count'] = q_votes
                            df['question_img'] = q_imgs
                            df['question_attachs'] = q_attachs
                            df['question_hyper_links_titles'] = q_hyper_link_titles
                            df['question_hyper_links'] = q_hyper_links
                            df['reply'] = r_texts
                            df['reply_rank'] = r_rates
                            df['reply_vote_count'] = r_votes
                            df['reply_order'] = r_orders
                            df['reply_image'] = imgs
                            df['reply_attachs'] = attachs
                            df['reply_hyper_links_titles'] = hyper_link_titles
                            df['reply_hyper_links'] = hyper_links
                            
                            print('Preping copy')
                            df.to_csv('siemens_from_conf14_page_835.csv',index = False )
                            #print(f'Saved a copy At Conf N. : {link_counter} , Page N. : {int(page)+1}  out of {int(total_pages)+1} ')
                            print(f'Saved a copy')
                
                except Exception as e:
                    
                    print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
                    print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
                    print(e)
                    logging.exception("An exception was thrown!")
                    print('Encoutered error , waiting for 15 min and running again ')
                    print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
                    print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
                    page_counter = page_counter - 1
                    error_counter = error_counter + 1
                    print(f'Error number : {error_counter}')
                    time.sleep(900)
                
                    
    except Exception as e:
        print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
        print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
        print(e)
        logging.exception("An exception was thrown!")
        print('Encoutered error , waiting for 15 min and running again ')
        print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
        print('*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/')
        link_counter = link_counter - 1
        error_counter = error_counter + 1
        print(f'Error number : {error_counter}')
        time.sleep(900)
        


# In[ ]:


len(imgs)


# In[ ]:


len(conf_titles)


# In[ ]:





df = pd.DataFrame()
df['conf'] = conf_titles
df['question_title'] = q_titles
df['question_text'] = q_texts
df['question_rate'] = q_rates
df['question_vote_count'] = q_votes
df['question_img'] = q_imgs
df['question_attachs'] = q_attachs
df['question_hyper_links_titles'] = q_hyper_link_titles
df['question_hyper_links'] = q_hyper_links
df['reply'] = r_texts
df['reply_rank'] = r_rates
df['reply_vote_count'] = r_votes
df['reply_order'] = r_orders
df['reply_image'] = imgs
df['reply_attachs'] = attachs
df['reply_hyper_links_titles'] = hyper_link_titles
df['reply_hyper_links'] = hyper_links

df


# In[ ]:


df.to_csv('siemens_from_conf3_page_630.csv',index = False )


# In[ ]:


# this is just to finish conf 1 


print(f'start time {datetime.datetime.now()}')

for link in links[:1]:
    link_counter  = link_counter + 1 
    
    page1 = requests.get(link)
    soup1 = bs(page1.content, "html.parser")
    lasts = soup1.find_all('dd',class_="last")
    if len(lasts)>0:
        last = lasts[0].find('a').get('href')
        result = re.search('page=(.*)&pageSize', last)
        total_pages = int(result.group(1))
    else:
        total_pages = 0
        
    conf_title = soup1.find_all('div',style ="display:block")[0].find('h1').text[10:-7]
    
    page1.close()
    
    time.sleep(10)
    
    for page in range(339,total_pages+1):
        
        current_page = f'page={str(page)}'
        link_page = link.replace('page=0' , current_page)
        
        page2 = requests.get(link_page)
        soup2 = bs(page2.content, "html.parser")
        topic_qs1 = soup2.find_all('tr',class_="conferencePadding thread evenOdd")
        topic_qs2 = soup2.find_all('tr',class_="conferencePadding thread evenOdd zebra")
        topic_qs = topic_qs1 + topic_qs2
        
        topic_qs_links = []
        for topic in topic_qs:
            t_link = topic.find('a').get('href')
            t_link = 'https://support.industry.siemens.com' + t_link
            if 'requestmembership' in t_link:
                pass
            else:
                topic_qs_links.append(t_link)
        topic_counter = 0 
        
        page2.close()
        
        time.sleep(10)
        
        for t_l in topic_qs_links:
            topic_counter = topic_counter + 1
            print(t_l)
            page3 = requests.get(t_l)

            soup3 = bs(page3.content, "html.parser")
            title_sec  = soup3.find('span', class_ = 'threadsubject')
            
            trail = 0 
            
            if title_sec :
                title = title_sec.text
            else:
                while title_sec is None:
                    try:
                        trail = 1+trail
                        print(f'This is trail no. : {trail}')
                        page3 = requests.get(t_l)

                        soup3 = bs(page3.content, "html.parser")
                        title_sec  = soup3.find('span', class_ = 'threadsubject')
                    except:
                        pass
                title = title_sec.text  
                    
                    
            print(title)

            replies = soup3.find_all('table', class_ = 'dns')
            #print(len(replies))
            entries_sec = soup3.find_all('div' , class_ = 'search-header')[0]
            entries = entries_sec.find('h2').text
            replies_pages = int(re.findall(r'\d+', entries)[0])//10
            print('reply pages count : '+str(replies_pages))
            
            if replies_pages > 0:
                for r_page in range(1, replies_pages+1):
                    time.sleep(10)
                    #print(r_page)
                    added_l = t_l.replace('page=0' , f'page={r_page}')
                    #print(added_l)
                    page4 = requests.get(added_l)
                    soup4 = bs(page4.content, "html.parser")
                    added_replies = soup4.find_all('table', class_ = 'dns')
                    replies =   replies + added_replies
            
            q = replies[0].find('td', class_ = 'body')

            q_text = q.text.replace('\n' , '  ')
            
            q_hyper_link_title = []
            q_hyper_link = []

            scriptTags = replies[0].findAll('a')
            for script in scriptTags:
                if script.has_attr('data-original-href'):
                    q_hyper_link_title.append(script.text)
                    q_hyper_link.append(script.get('href'))
            
            vote_sec = replies[0].find('a' , class_ = "within flyout-ur")
            
            if vote_sec:
                vote = replies[0].find('a' , class_ = "within flyout-ur").text
                q_vote = re.findall(r'\d+', vote)[0]
            else:
                q_vote = 0
                
            star_sec = replies[0].find('a' , class_ = "within flyout-ur")
            
            if star_sec:
                star_rate = replies[0].find('a' , class_ = "within flyout-ur").find('img',class_ = 'stars').get('src')
                result = re.search('Star(.*).post.gif', star_rate)
                q_rate = float(result.group(1))
            else:
                q_rate = 0.0

            q = replies[0].find('td', class_ = 'body')

            q_text = q.text.replace('\n' , '  ')

            attach = replies[0].find('div', class_ = 'appendix add-bottom')
            if attach:
                img_link = attach.find('img')
                if img_link:
                    img_link = img_link.get('src')
                    img_link = 'https://support.industry.siemens.com' +img_link
                    q_img = img_link
                    q_attach = attach
                else:
                    q_img = 'no_img'
                    q_attach = attach
            else:
                q_img = 'no_img'
                q_attach = 'no_attach'

            counter_r = 0
            if len(replies) > 1:
                for r in replies[1:]:
                    counter_r = counter_r + 1
                    attach = r.find('div', class_ = 'appendix add-bottom')
                    if attach:
                        img_link = attach.find('img')
                        if img_link:
                            img_link = img_link.get('src')
                            img_link = 'https://support.industry.siemens.com' +img_link

                        else:
                            img_link = 'no_img'
                            #imgs.append(img_link)
                            #attachs.append(attach)
                    else:
                        img_link = 'no_img'
                        #imgs.append(img_link)
                        attach = 'no_attach'
                        #attachs.append(attach)
                    scriptTags = r.findAll('a')
                    h_links = []
                    h_links_titles = []
                    for script in scriptTags:
                        if script.has_attr('data-original-href'):
                            h_links_titles.append(script.text)
                            h_links.append(script.get('href'))
                    vote = r.find('a' , class_ = "within flyout-ur")
                    if vote:
                        vote = r.find('a' , class_ = "within flyout-ur").text
                        r_vote = re.findall(r'\d+', vote)[0]
                    else:
                        r_vote = 0
                        
                    star_rate_sec = r.find('a' , class_ = "within flyout-ur")
                    
                    if star_rate_sec:
                        star_rate = r.find('a' , class_ = "within flyout-ur").find('img',class_ = 'stars')

                        if star_rate:
                            star_rate = r.find('a' , class_ = "within flyout-ur").find('img',class_ = 'stars').get('src')
                            result = re.search('Star(.*).post.gif', star_rate)
                            r_rate = float(result.group(1))
                        else:
                            r_rate = 0 
                    else:
                        r_rate = 0 

                    r_content = r.find('td', class_ = 'body')

                    r_text = r_content.text.replace('\n' , '  ')


                    conf_titles.append(conf_title)
                    q_titles.append(title)
                    q_texts.append(q_text)
                    r_texts.append(r_text)
                    q_hyper_link_titles.append(q_hyper_link_title)
                    q_hyper_links.append(q_hyper_link)
                    hyper_link_titles.append(h_links_titles)
                    hyper_links.append(h_links)
                    q_rates.append(q_rate)
                    q_votes.append(q_vote)
                    q_imgs.append(q_img)
                    q_attachs.append(q_attach)
                    r_rates.append(r_rate)
                    r_votes.append(r_vote)
                    r_orders.append(counter_r)
                    imgs.append(img_link)
                    attachs.append(attach)                    


            else:
                conf_titles.append(conf_title)
                q_titles.append(title)
                q_texts.append(q_text)
                r_texts.append('no_reply')
                q_hyper_link_titles.append(q_hyper_link_title)
                q_hyper_links.append(q_hyper_link)
                hyper_link_titles.append('no_reply')
                hyper_links.append('no_reply')
                q_rates.append(q_rate)
                q_votes.append(q_vote)
                q_imgs.append(q_img)
                q_attachs.append(q_attach)
                r_rates.append('no_reply')
                r_votes.append('no_reply')
                r_orders.append('no_reply')  
                imgs.append(img_link)
                attachs.append(attach)
            


            print(f'At Conf N. : {link_counter} , Page N. : {int(page)+1}  out of : {int(total_pages)+1} , Topic N. :{topic_counter}  out of : 10')
            print(f'Remaining Confs : {66- link_counter} ')
            print('-------------------------------------')
            print(datetime.datetime.now())
            time.sleep(10)
            
            df = pd.DataFrame()
            df['conf'] = conf_titles
            df['question_title'] = q_titles
            df['question_text'] = q_texts
            df['question_rate'] = q_rates
            df['question_vote_count'] = q_votes
            df['question_img'] = q_imgs
            df['question_attachs'] = q_attachs
            df['question_hyper_links_titles'] = q_hyper_link_titles
            df['question_hyper_links'] = q_hyper_links
            df['reply'] = r_texts
            df['reply_rank'] = r_rates
            df['reply_vote_count'] = r_votes
            df['reply_order'] = r_orders
            df['reply_image'] = imgs
            df['reply_attachs'] = attachs
            df['reply_hyper_links_titles'] = hyper_link_titles
            df['reply_hyper_links'] = hyper_links

            df.to_csv('siemens_test2.csv',index = False )
            #print(f'Saved a copy At Conf N. : {link_counter} , Page N. : {int(page)+1}  out of {int(total_pages)+1} ')
            print(f'Saved a copy')


# In[ ]:


# first trail start time 2022-11-12 00:16:29.696809



df = pd.DataFrame()
df['conf'] = conf_titles
df['question_title'] = q_titles
df['question_text'] = q_texts
df['question_rate'] = q_rates
df['question_vote_count'] = q_votes
df['question_img'] = q_imgs
df['question_attachs'] = q_attachs
df['question_hyper_links_titles'] = q_hyper_link_titles
df['question_hyper_links'] = q_hyper_links
df['reply'] = r_texts
df['reply_rank'] = r_rates
df['reply_vote_count'] = r_votes
df['reply_order'] = r_orders
df['reply_image'] = imgs
df['reply_attachs'] = attachs
df['reply_hyper_links_titles'] = hyper_link_titles
df['reply_hyper_links'] = hyper_links

df


# In[ ]:


df.to_csv('siemens_1st_conf.csv',index = False )


# In[ ]:


len(r_orders)


# In[ ]:


len(df)


# In[ ]:


df.loc[0,'reply']


# In[ ]:


img_pos = 0 
new_imgs = []
new_attchs = []

for i in range(0, len(df)):
    if df.loc[i,'reply'] == 'no_reply':
        df.loc[i,'reply_image'] = 'no_reply'
        df.loc[i,'reply_attachs'] = 'no_reply'
        new_imgs.append('no_reply')
        new_attchs.append('no_reply')
        img_pos = img_pos + 1
    else:
        loc_in = i - img_pos
        fix_img = imgs[loc_in]
        fix_attach = attachs[loc_in]
        #df.loc[i,'reply_image'] = fix_img
        #df.loc[i,'reply_attachs'] = fix_attach
        new_imgs.append(imgs[loc_in])
        new_attchs.append(attachs[loc_in])
    


# In[ ]:


loc_in


# In[ ]:


len(new_imgs)


# In[ ]:


new_attchs[0]


# In[ ]:


# At Conf N. : 1 , Page N. : 23  out of : 342 , Topic N. :8  out of : 10


# In[ ]:


# first conf fixer

df = pd.DataFrame()
df['conf'] = conf_titles
df['question_title'] = q_titles
df['question_text'] = q_texts
df['question_rate'] = q_rates
df['question_vote_count'] = q_votes
df['question_img'] = q_imgs
df['question_attachs'] = q_attachs
df['question_hyper_links_titles'] = q_hyper_link_titles
df['question_hyper_links'] = q_hyper_links
df['reply'] = r_texts
df['reply_rank'] = r_rates
df['reply_vote_count'] = r_votes
df['reply_order'] = r_orders
df['reply_image'] = new_imgs
df['reply_attachs'] = new_attchs
df['reply_hyper_links_titles'] = hyper_link_titles
df['reply_hyper_links'] = hyper_links

df


# In[ ]:


#df[~(df['question_title'].duplicated())&(df['question_hyper_links_titles'].duplicated())]


# In[ ]:


df.to_csv('siemens_conf1_fixed.csv',index = False )


# In[ ]:





#!/usr/bin/env python
#coding:utf-8
from urllib import request
import time
import random
from urllib.error import URLError, HTTPError
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import smtplib
from lxml import etree

class Spider:
    def __init__(self):
        self.old_model = list()

    def check_update(self):

        link = "https://www.casio.com.cn/wat/search.html"
        print('link: ' + link)
        self.get_old_model()
        self.get_new_model(link)
        
    def get_old_model(self):
        self.old_model = list()
        f = open("watch.txt", 'r')    
        for line in open('watch.txt'):
            line = f.readline()
            line = line.strip()
            self.old_model.append(line)
        f.close()
                
    def open_url(self, link):
        wanted_page = link
        req = request.Request(wanted_page)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                   '(KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393')
        response = request.urlopen(req)
        html = response.read().decode('utf-8')
        return html
            
    # get watch model
    def get_new_model(self, link):  
        html = self.open_url(link)
        tree = etree.HTML(html)
        node = tree.xpath(u"/descendant::h5[@class='t-size-x-small']")
        
        new_model = list()
        for i in node:
            if (i.text not in self.old_model):
                print("new model found: " + i.text)
                new_model.append(i.text)
        
        if new_model:
            f = open("watch.txt", "a")
            for i in new_model:
                f.write(i + '\n')
            f.close()
            
            #send_email
            
        else:
            print("no new Model found")

if __name__ == '__main__':
    update_Spider = Spider()
    while(1):
        update_Spider.check_update()
        #break
        #check every 600s
        time.sleep(20)
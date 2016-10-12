#!/usr/bin/env python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import contextlib

from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector

from lxml import html

class ClassSearch():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.subjects = []
        self.num_pages = 0


    def start_connection(self):
        driver = self.driver
        driver.get("http://classes.ucr.edu")

        
    def end_connection(self):
        self.driver.close()

      
    def click_search(self):
        search = self.driver.find_element_by_name("btn_search").click()


    def get_subject_options(self):
        subject_element = self.driver.find_element_by_name("drp_subjectArea")
        all_options = subject_element.find_elements_by_tag_name("option")        
        for option in all_options:
            if option.get_attribute("value") == "Subject Area" or option.get_attribute("value") == "" :
                continue
            self.subjects.append(option.get_attribute("value"))


    def get_next_page(self):
        try:
            classes_element = self.driver.find_element_by_id("pnel_Classes")
        except: 
            self.num_pages = 0
            return

        try:
	    print "at page %s" %self.num_pages
            
            if self.num_pages == 0:
                page_link = "javascript:__doPostBack('grid_students','Page$2')"
                self.driver.find_element_by_xpath('//a[@href="'+page_link+'"]')
            else:
                page_link = "javascript:__doPostBack('grid_students','Page$%s')" %(self.num_pages + 1)
                self.driver.find_element_by_xpath('//a[@href="'+page_link+'"]')
        except:
            self.num_pages = 0
            return

        if self.num_pages == 0:
          self.num_pages = self.num_pages + 2 
        else:
          self.num_pages = self.num_pages + 1
        print "going to page %s" %self.num_pages


    def iterate_subject_options(self):
        #self.subjects = []
        #self.subjects.append("BSWT")
        #self.subjects.append("BCH ")
        for subject in self.subjects:  
            time.sleep(2)  ###IMPROVABLE
            subject_element = Select(self.driver.find_element_by_name("drp_subjectArea"))
            subject_element.select_by_value(subject)
            time.sleep(2)  ###IMPROVABLE
            self.click_search()
            time.sleep(3)  ###IMPROVABLE
            
            
            #---RETRIEVE DATA FROM ALL PAGES FOR THIS SUBJECT---
            table = []
            table = self.driver.find_elements_by_xpath('//*[@id="grid_students"]/tbody/tr/td')
            for i in table:
               print i.text

            self.get_next_page()
            while self.num_pages != 0:
                page_link = "javascript:__doPostBack('grid_students','Page$%s')" %self.num_pages 
                self.driver.find_element_by_xpath('//a[@href="'+page_link+'"]').click()

                time.sleep(2)  ###IMPROVABLE
                self.get_next_page()
                table = self.driver.find_elements_by_xpath('//*[@id="grid_students"]/tbody/tr/td')
                for i in table:
                   print i.text

                            #---RETRIEVE DATA FROM ALL PAGES FOR THIS SUBJECT---

if __name__ == "__main__":
    retriever = ClassSearch()
    retriever.start_connection()
    retriever.get_subject_options()
    retriever.iterate_subject_options()
    retriever.end_connection()

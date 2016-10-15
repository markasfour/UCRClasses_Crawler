#!/usr/bin/env python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import contextlib

from firebase import firebase
import json
import serial
import time
import requests
import json

firebase_url = 'https://cs180-bf6af.firebaseio.com/'

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
        
    #---MAIN FUNCTION TO RETRIEVE TEXT OF TABLE PAGES---#    
    def getinfo(self):
      for x in range (02, 12):
        if (x < 10):
            popup = "javascript:__doPostBack('grid_students$ctl0"+str(x)+"$lnkbtn_courseTitle','')"
        else:
            popup = "javascript:__doPostBack('grid_students$ctl"+str(x)+"$lnkbtn_courseTitle','')"
        table = []
        self.driver.find_element_by_xpath('//a[@href="'+popup+'"]').click()
        time.sleep(2)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_courseTitle"]/b/font').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_courseNum"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_callNo"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_instructor"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_units"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_maxEnrollment"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[1]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[2]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[3]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[4]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[5]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_availableSeats"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_waitlistMax"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_onWaitList"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_coquisites"]/font').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_prerequisties"]/font').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_restrictionsA"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_finalExamDate"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_finalExamDateA"]').text)
        table.append(self.driver.find_element_by_xpath('//*[@id="lbl_notes"]').text)
        #each table will have 0 to 19 indexes
        
        data = {'CourseTitle': table[0], 'name': table[2]}
        
#        data = {'CourseTitle': table[0], 'CourseNumber': table[1], 'CallNumber': table[2], 'Instructor': table[3], 'Units': table[4], 'MaxEnrollment': table[5], 'Lec/Dis': table[6], 'Days': table[7], 'Time': table[8], 'RoomAbrv': table[9], 'BuildingName': table[10], 'AvailableSeats': table[11], 'WaitListMax': table[12], 'NumberonWaitList': table[13], 'Co-requisites': table[14], 'Prerequisites': table[15], 'Restrictions': table[16], 'FinalExamDate': table[17], 'FinalExamTime': table[18], 'CatalogDescription': table[19]}
        
        result = requests.post(firebase_url + '/' + table[0] + '/' + 'course.json', data=json.dumps(data))
#        result = requests.post(firebase_url + '/' + table[0] + '/course.json', data=json.dumps(data))
        print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text

        
        #subject -> anthro -> class_name -> class_sec -> call_num/instructor/units/max_enroll...restrictions
        #
#        class_name = table[0]
#        class_sec = table [1]
#        class classinfo(object):
#            def __init__(self):
#
#                self.call_num = table[2]
#                self.instructor = table[3] 
#                self.units = table[4]
#                self.max_enroll = table[5]
#                self.class_type = table[6]
#                self.days =  table[7]
#                self.time =  table[8]
#                self.rm_num = table[9]
#                self.rm_loc = table[10]
#                self.avail_seats = table[11]
#                self.max_waitlist = table[12]
#                self.on_waitlist = table[13]
#                self.coreqs = table[14]
#                self.prereqs = table[15]
#                self.restrictions = table[16]
#                self.final_date = table[17]
#                self.final_time = table[18]
#                self.description = table[19]
#       
#        class_info = classinfo()
#        class_info_json = json.dumps(class_info.__dict__)
##        
#        first = firebase.put(class_name, class_sec, class_info_json) 
#        first = firebase.put('class_name','class_sec', 'call_num' ) 
#        print(first)


#        for t in table:
#          print t


        self.driver.find_element_by_xpath('//*[@id="ClassInfo"]/a').click()
        time.sleep(2)
        
#       table = []
#      table += self.driver.find_elements_by_xpath('//*[@id="lbl_callNo"]')
#      for t in table:
#      print t.get_attribute('innerText').strip()
#      
#test
#      for x in range(2, 12):
#        table += self.driver.find_elements_by_xpath('//*[@id="grid_students"]/tbody/tr[' + str(x) + ']/td')
#        if x == 2:
#          table += self.driver.find_elements_by_xpath('//*[@id="grid_students"]/tbody/tr[' + str(x) + ']/td/span/span')
#        else:
#          table += self.driver.find_elements_by_xpath('//*[@id="grid_students"]/tbody/tr[' + str(x) + ']/td/span/b/span')

#      for t in table:
#        print t.get_attribute('innerText').strip()


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
            
            self.getinfo()
            print('\n')
          #---RETRIEVE DATA FROM ALL PAGES FOR THIS SUBJECT---
            self.get_next_page()
            while self.num_pages != 0:
              page_link = "javascript:__doPostBack('grid_students','Page$%s')" %self.num_pages 
              self.driver.find_element_by_xpath('//a[@href="'+page_link+'"]').click()
              time.sleep(2)  ###IMPROVABLE
              self.get_next_page()
              
              self.getinfo()
              print('\n')
          #---RETRIEVE DATA FROM ALL PAGES FOR THIS SUBJECT---

if __name__ == "__main__":
    firebase = firebase.FirebaseApplication('https://cs180-bf6af.firebaseio.com/', authentication=None)
#    authentication = firebase.Authentication('SECRET', 'bchen022@ucr.edu', extra={'id':123})
#    firebase.authentication = authentication
#    print authentication.extra

    retriever = ClassSearch()
    retriever.start_connection()
    retriever.get_subject_options()
    retriever.iterate_subject_options()
    retriever.end_connection()

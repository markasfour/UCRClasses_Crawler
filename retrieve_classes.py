#!/usr/bin/env python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import contextlib

from firebase import firebase
import json
import serial
import time
import requests
import json
import sys

firebase_url = 'https://cs180-bf6af.firebaseio.com/'

class ClassSearch():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.quarter = ''
	self.subjects = []
        self.num_pages = 0
        self.wait = WebDriverWait(self.driver, 5)


    def start_connection(self):
        driver = self.driver
        driver.get("http://classes.ucr.edu")

        
    def end_connection(self):
        self.driver.close()

      
    def click_search(self):
        search = self.driver.find_element_by_name("btn_search").click()


    def get_quarter(self):
        quarters = []
        quarter_elements = self.driver.find_element_by_name("drp_term")
        all_options = quarter_elements.find_elements_by_tag_name("option")        
        for option in all_options:
            if option.get_attribute("value") == "" :
                continue
            quarters.append(option.get_attribute("value"))
        self.quarter = quarters[0]


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
    
    
    def get_info(self, subject):
      for x in range (2, 12):
        try:
          if (x < 10):
            popup = "javascript:__doPostBack('grid_students$ctl0"+str(x)+"$lnkbtn_courseTitle','')"
          else:
            popup = "javascript:__doPostBack('grid_students$ctl"+str(x)+"$lnkbtn_courseTitle','')"

          table = []
          self.driver.find_element_by_xpath('//a[@href="'+popup+'"]').click()
          #time.sleep(3)
          self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="exposeMask"][contains(@style, "display: block; opacity: 0.8")]')))
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_courseTitle"]/b/font').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_courseNum"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_callNo"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_instructor"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_units"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_maxEnrollment"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[1]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[2]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[3]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[4]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[5]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_availableSeats"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_waitlistMax"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_onWaitList"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_coquisites"]/font').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_prerequisties"]/font').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_restrictionsA"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_finalExamDate"]').text)
          except:
            table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_finalExamDateA"]').text)
          except:
              table.append("n/a")
          try:
            table.append(self.driver.find_element_by_xpath('//*[@id="lbl_notes"]').text)
          except:
            table.append("n/a")
          self.driver.find_element_by_xpath('//*[@id="ClassInfo"]/a').click()
          #each table will have 0 to 19 indexes
          data = {'Subject': subject, 'CourseTitle': table[0], 'CourseNum': table[1], 'CallNo': table[2], 'Instructor': table[3], 'Units': table[4], 'MaxEnrollment': table[5], 'Lec_Dis': table[6], 'Days': table[7], 'Time': table[8], 'RoomAbrv': table[9], 'BuildingName': table[10], 'AvailableSeats': table[11], 'WaitListMax': table[12], 'NumberonWaitList': table[13], 'Co-requisites': table[14], 'Prerequisites': table[15], 'Restrictions': table[16], 'FinalExamDate': table[17], 'FinalExamTime': table[18], 'CatalogDescription': table[19]}

          #Do not send data to DB if there is no CourseNum
          if table[1] == '' or table[1] == 'n/a':
              continue

          result = requests.patch(firebase_url + '/' + self.quarter + '/' + subject + '/' + table[2] + '.json', data=json.dumps(data))
          print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text
          #time.sleep(3)
        except:
          continue


    def reverse_subjects(self):
        self.subjects.reverse()   
        print "Reversed subject order to retrieve"


    def half_subjects_list(self):
        self.subjects = self.subjects[:len(self.subjects)/2]
        print "Halved the subject list"


    def set_start_subject(self, start):
        if start != '':
            try:
                index = self.subjects.index(start)
            except:
                print "Subject " + start + " was not found. Starting at " + self.subjects[0]
                return 
            for i in range (index):
                self.subjects.pop(0)
            print "Starting at " + start


    def set_end_subject(self, end):
        if end != '':
            try:
                index = self.subjects.index(end)
            except:
                print "Subject " + end + " was not found. Ending at " + self.subjects[len(self.subjects) - 1]
            for i in range (len(self.subjects) - index - 1):
                self.subjects.pop(len(self.subjects) - 1)   
            print "Ending at " + end


    def iterate_subject_options(self):
        for subject in self.subjects:  
            #time.sleep(2)  ###IMPROVABLE
            self.wait.until(EC.presence_of_element_located((By.NAME, "drp_subjectArea"))) 
            subject_element = Select(self.driver.find_element_by_name("drp_subjectArea"))
            subject_element.select_by_value(subject)
            #time.sleep(2)  ###IMPROVABLE
            self.click_search()
            time.sleep(3)  ###IMPROVABLE
            #self.wait.until(EC.presence_of_element_located((By.ID, "pnel_Classes")))

            self.get_info(subject)
            print('\n')
            self.get_next_page()
            while self.num_pages != 0:
              page_link = "javascript:__doPostBack('grid_students','Page$%s')" %self.num_pages
              self.driver.find_element_by_xpath('//a[@href="'+page_link+'"]').click()
              time.sleep(2)  ###IMPROVABLE
              #self.wait.until(EC.presence_of_element_located((By.ID, "pnel_Classes")))
              self.get_next_page()
              
              self.get_info(subject)
              print('\n')


def arguments_reader(retriever):
    try:
       sys.argv.index('-r') 
       retriever.reverse_subjects()
       sys.argv.pop(sys.argv.index('-r'))
    except: 
       pass
    try:
       sys.argv.index('-h')
       retriever.half_subjects_list()
       sys.argv.pop(sys.argv.index('-h'))
    except:
       pass
    if len(sys.argv) >= 2:
    	retriever.set_start_subject(sys.argv[1])
        if len(sys.argv) == 3:
    	    retriever.set_end_subject(sys.argv[2])


if __name__ == "__main__":
    firebase = firebase.FirebaseApplication('https://cs180-bf6af.firebaseio.com/', authentication=None)
    retriever = ClassSearch()
    retriever.start_connection()
    retriever.get_quarter()
    retriever.get_subject_options()
    arguments_reader(retriever)
    retriever.iterate_subject_options()
    retriever.end_connection()

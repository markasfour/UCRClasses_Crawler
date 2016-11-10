#!/usr/bin/python
# -*- coding: utf-8 -*-

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
table = 1
def tableInc():
    global table
    table += 1
def tableClear():
    global table
    table = 1


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''


def quarter_translate(quarter):
    term = quarter[0]
    year = quarter[len(quarter) - 2] + quarter[len(quarter) - 1]
    return year + term


class course:
    def __init__(self):
        self.AvailableSeats = ''
        self.BuildingName = ''
        self.CallNo = ''
        self.CatalogDescription = ''
        self.Co_requisites = ''
        self.CourseNum = ''
        self.CourseTitle = ''
        self.Days = ''
        self.FinalExamDate = ''
        self.FinalExamTime = ''
        self.Instructor = ''
        self.Lec_Dis = ''
        self.MaxEnrollment = ''
        self.NumberonWaitList = ''
        self.Prerequisites = ''
        self.Restrictions = ''
        self.RoomAbrv = ''
        self.Subject = ''
        self.Time = ''
        self.Units = ''
        self.WaitListMax = ''

    def print_info(self):
        print 'Available Seats: ' + self.AvailableSeats
        print 'Building Name: ' + self.BuildingName
        print 'Call Number: ' + self.CallNo
        print 'Catalog Description: ' + self.CatalogDescription.strip('\n')
        print 'Corequisites: ' + self.Co_requisites
        print 'Course Number: ' + self.CourseNum
        print 'Course Title: ' + self.CourseTitle
        print 'Days: ' + self.Days
        print 'Final Exam Date: ' + self.FinalExamDate
        print 'Final Exam Time: ' + self.FinalExamTime
        print 'Instructor: ' + self.Instructor
        print 'Lec_Dis: ' + self.Lec_Dis
        print 'Max Enrollment: ' + self.MaxEnrollment
        print 'Number on Wait List: ' + self.NumberonWaitList
        print 'Prerequisites: ' + self.Prerequisites
        print 'Restrictions: ' + self.Restrictions
        print 'Room Abrv: ' + self.RoomAbrv
        print 'Subject: ' + self.Subject
        print 'Time: ' + self.Time
        print 'Units: ' + self.Units
        print 'Wait List Max: ' + self.WaitListMax

    def clear_info(self):
        self.AvailableSeats = ''  # done
        self.BuildingName = ''
        self.CallNo = ''  # done
        self.CatalogDescription = ''
        self.Co_requisites = ''  # done
        self.CourseNum = ''
        self.CourseTitle = ''  # done
        self.Days = ''
        self.FinalExamDate = ''
        self.FinalExamTime = ''
        self.Instructor = ''
        self.Lec_Dis = ''  # done
        self.MaxEnrollment = ''
        self.NumberonWaitList = ''
        self.Prerequisites = ''  # done
        self.Restrictions = ''  # done
        self.RoomAbrv = ''
        self.Subject = ''  # done
        self.Time = ''
        self.Units = ''  # done
        self.WaitListMax = ''

    def clean_data(self):
        self.AvailableSeats = self.AvailableSeats.strip().replace('\n', ' ')
        self.BuildingName = self.BuildingName.strip().replace('\n', ' ')
        self.CallNo = self.CallNo.strip().replace('\n', ' ')
        self.CatalogDescription = self.CatalogDescription.strip().replace('\n', ' ')
        self.Co_requisites = self.Co_requisites.strip().replace('\n', ' ')
        self.CourseNum = self.CourseNum.strip().replace('\n', ' ')
        self.CourseTitle = self.CourseTitle.strip().replace('\n', ' ')
        self.Days = self.Days.strip().replace('\n', ' ')
        self.FinalExamDate = self.FinalExamDate.strip().replace('\n', ' ')
        self.FinalExamTime = self.FinalExamTime.strip().replace('\n', ' ')
        self.Instructor = self.Instructor.strip().replace('\n', ' ')
        self.Lec_Dis = self.Lec_Dis.strip().replace('\n', ' ')
        self.MaxEnrollment = self.MaxEnrollment.strip().replace('\n', ' ')
        self.NumberonWaitList = self.NumberonWaitList.strip().replace('\n', ' ')
        self.Prerequisites = self.Prerequisites.strip().replace('\n', ' ')
        self.Restrictions = self.Restrictions.strip().replace('\n', ' ')
        self.RoomAbrv = self.RoomAbrv.strip().replace('\n', ' ')
        self.Subject = self.Subject.strip().replace('\n', ' ')
        self.Time = self.Time.strip().replace('\n', ' ')
        self.Units = self.Units.strip().replace('\n', ' ')
        self.WaitListMax = self.WaitListMax.strip().replace('\n', ' ')


class ClassSearch:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.quarter = ''
        self.reverse = 0
        self.half = 0
        self.total_pages = 0
        self.classes_list = []
        self.class_info = course()
        self.wait = WebDriverWait(self.driver, 5)

    def start_connection(self):
        driver = self.driver
        driver.get('http://classes.ucr.edu')

    def end_connection(self):
        self.driver.close()

    def reverse_order(self):
        self.reverse = 1

    def half_total_pages(self):
        half = 1

    def term_select(self):
        self.driver.find_element_by_id('s2id_txt_term').click()
        self.wait.until(EC.presence_of_element_located((By.ID,
                                        'select2-result-label-2')))
        print self.driver.find_element_by_id('select2-result-label-2'
                        ).text
        self.quarter = quarter_translate(self.driver.find_element_by_id('select2-result-label-2'
                                                    ).text)
        self.driver.find_element_by_id('select2-result-label-2').click()
        self.driver.find_element_by_id('term-go').click()

    def click_search(self):
        self.wait.until(EC.presence_of_element_located((By.ID,
                                        'search-go')))
        self.driver.find_element_by_id('search-go').click()

    def increase_classes_per_page(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                        'page-size-select')))
        total_pages = self.driver.find_element_by_class_name('total-pages').text
        page_size_element = Select(self.driver.find_element_by_class_name('page-size-select'))
        page_size_element.select_by_value('50')
        while 1:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                            'total-pages')))
            try:
                if self.driver.find_element_by_class_name('total-pages'
                                ).text != total_pages:
                    self.total_pages = int(self.driver.find_element_by_class_name('total-pages').text)
                    break
            except:
                pass
        if self.half:
            self.total_pages = self.total_pages / 2

    def get_next_page(self):
        try:
            if self.reverse == 0:
                time.sleep(2)
                self.driver.find_element_by_class_name('next').click()
                return 1
            elif self.reverse == 1:
                time.sleep(2)
                self.driver.find_element_by_class_name('previous'
                                ).click()
                return 1
        except:
            return 0

    def get_classes_on_page(self):
        self.classes_list = self.driver.find_elements_by_class_name('section-details-link')
        print str(len(self.classes_list)) + ' classes on this page'

    def click_class(self, x):
        self.classes_list[x].click()
        try:
            self.wait.until(EC.presence_of_element_located((By.ID,
                                            'courseReferenceNumber')))
        except:
            pass

    def close_class(self):
        self.driver.find_element_by_class_name('ui-icon-closethick'
                        ).click()
        try:
            self.wait.until(EC.invisibility_of_element_located((By.ID,
                                            'courseReferenceNumber')))
        except:
            pass

    def get_class_info(self):
        self.class_info.clear_info()

        try:
            class_details = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
        except:
            class_details = "n/a"
            pass

        #Available Seats
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.AvailableSeats = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[6]').text
        except:
            self.class_info.AvailableSeats = "n/a"
            pass

        #Building Name
        try:
            self.driver.find_element_by_id('facultyMeetingTimes').click()
            time.sleep(.5)
            if(self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]').text == ""):
                pass
            else:
                self.class_info.BuildingName = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]').text
        except:
            self.class_info.BuildingName = "n/a"
            pass

        #CALL NUMBER
        try:
            self.class_info.CallNo = find_between(class_details, 'CRN:', 'Campus:').strip()
        except:
            self.class_info.CallNo = "n/a"
            pass

        #DAYS
        try:
            self.driver.find_element_by_id('facultyMeetingTimes').click()
            time.sleep(.5)
            try:
                self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/')
            except:
                sun = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[1]').get_attribute('aria-checked')
                mon = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[2]').get_attribute('aria-checked')
                tue = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[3]').get_attribute('aria-checked')
                wed = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[4]').get_attribute('aria-checked')
                thur = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[5]').get_attribute('aria-checked')
                fri = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[6]').get_attribute('aria-checked')
                sat = self.driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr[' + str(table) + ']/td[8]/div/div/ul/li[7]').get_attribute('aria-checked')
                tableInc()

                temp = ""
                if(sun == "true"):
                    temp += "Sunday\n"
                if(mon == "true"):
                    temp += "Monday\n"
                if(tue == "true"):
                    temp += "Tuesday\n"
                if(wed == "true"):
                    temp += "Wednesday\n"
                if(thur == "true"):
                    temp += "Thursday\n"
                if(fri == "true"):
                    temp += "Friday\n"
                if(sat == "true"):
                    temp += "Saturday\n"
                self.class_info.Days = temp

        except:
            self.class_info.Days = "n/a"
            tableInc()
            pass

        #instructor name
        try:
            self.driver.find_element_by_id('facultyMeetingTimes').click()
            time.sleep(.5)
            try:
                instructor1 = self.class_info.Instructor = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span/span[1]/a').text
            except:
                instructor1 = ""
                pass
            try:
                instructor2 = self.class_info.Instructor = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span[2]/span/a').text
            except:
                instructor2 = ""
                pass

            allinstructors = instructor1 + " " + instructor2
            if (allinstructors == " "):
                allinstructors = "Instructors are not available yet. "

            self.class_info.Instructor = allinstructors

        except:
            self.class_info.Instructor = "n/a"
            pass

        #Max Enrollment
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.MaxEnrollment = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[4]').text
        except:
            self.class_info.MaxEnrollment = "n/a"
            pass

        #Num on WaitList
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.NumberonWaitList = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[10]').text
        except:
            self.class_info.NumberonWaitList = "n/a"
            pass

        #time
        try:
            self.driver.find_element_by_id('facultyMeetingTimes').click()
            time.sleep(.5)
            self.class_info.Time = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[1]').text
        except:
            self.class_info.Time = "n/a"
            pass

        #wait list max
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.WaitListMax = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[8]').text
        except:
            self.class_info.WaitListMax = "n/a"
            pass

        #SCHEDULE TYPE
        try:
            self.class_info.Lec_Dis = find_between(class_details, 'Schedule Type:', 'Instructional')
        except:
            self.class_info.Lec_Dis = "n/a"
            pass

        #SUBJECT
        try:
            self.class_info.Subject = find_between(class_details, 'Subject:' , 'Course Number:')
        except:
            self.class_info.Subject = "n/a"
            pass

        #COURSE NUM
        try:
            self.class_info.CourseNum = find_between(class_details, 'Course Number:', 'Title:')
        except:
            self.class_info.CourseNum = "n/a"
            pass

        #COURSE TITLE
        try:
            self.class_info.CourseTitle = find_between(class_details, 'Title:', 'Units:')
        except:
            self.class_info.CourseTitle = "n/a"
            pass

        #UNITS
        try:
            self.class_info.Units = find_between(class_details, 'Units:',
                        'Grade Mode:')
        except:
            self.class_info.Units = "n/a"
            pass

        #CATALOG DESCRIPTION
        try:
            self.driver.find_element_by_id('courseDescription').click()
            time.sleep(.5)
            self.class_info.CatalogDescription = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
            self.driver.find_element_by_id('facultyMeetingTimes').click()

            #not used for anything
            class_details_2 = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
            self.driver.find_element_by_id('enrollmentInfo').click()
            class_details_3 = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
        except:
            self.class_info.CatalogDescription = "n/a"
            pass

        #PREREQUISITES
        try:
            self.driver.find_element_by_id('preReqs').click()
            time.sleep(.5)
            self.class_info.Prerequisites = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
        except:
            self.class_info.Prerequisites = "n/a"
            pass

        #COREQUISITES click link below?
        try:
            self.driver.find_element_by_id('coReqs').click()
            time.sleep(.5)
            self.class_info.Co_requisites = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
        except:
            self.class_info.Co_requisites = "n/a"
            pass

        #RESTRICTIONS click link below?
        try:
            self.driver.find_element_by_id('restrictions').click()
            time.sleep(.5)
            self.class_info.Restrictions = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
        except:
            self.class_info.Restrictions = "n/a"
            pass
        self.class_info.print_info()


    def send_info(self):
        print "posting to DB"
        data = {
                    'Subject': self.class_info.Subject,
                    'CourseTitle': self.class_info.CourseTitle,
                    'CourseNum': self.class_info.CourseNum,
                    'CallNo': self.class_info.CallNo,
                    'Instructor': self.class_info.Instructor,
                    'Units': self.class_info.Units,
                    'MaxEnrollment': self.class_info.MaxEnrollment,
                    'Lec_Dis': self.class_info.Lec_Dis,
                    'Days': self.class_info.Days,
                    'Time': self.class_info.Time,
                    'RoomAbrv': self.class_info.RoomAbrv,
                    'BuildingName': self.class_info.BuildingName,
                    'AvailableSeats': self.class_info.AvailableSeats,
                    'WaitListMax': self.class_info.WaitListMax,
                    'NumberonWaitList': self.class_info.NumberonWaitList,
                    'Co-requisites': self.class_info.Co_requisites,
                    'Prerequisites': self.class_info.Prerequisites,
                    'Restrictions': self.class_info.Restrictions,
                    'FinalExamDate': self.class_info.FinalExamDate,
                    'FinalExamTime': self.class_info.FinalExamTime,
                    'CatalogDescription': self.class_info.CatalogDescription,
                    }

        self.class_info.clean_data()
        temp_Subject = self.class_info.Subject
        temp_callNo = self.class_info.CallNo
        result = requests.patch(firebase_url + '/' + self.quarter + '/' + temp_Subject + '/' + temp_callNo + '.json', data=json.dumps(data))
        print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text


    def iterate_pages(self):
        counter = 1
        if self.reverse:
            self.driver.find_element_by_class_name('last').click()
            try:
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                'loading')))
            except:
                pass
            try:
                self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,
                                                'loading')))
            except:
                pass

     # GET INITIAL PAGE CLASS INFORMATION HERE
        self.get_classes_on_page()
        for x in range(0, len(self.classes_list)):
            self.click_class(x)
            self.get_class_info()
            self.send_info()
            self.close_class()

        while self.get_next_page():
            try:
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                'loading')))
            except:
                pass
            try:
                self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,
                                                'loading')))
            except:
                pass

     # GET CLASS INFORMATION HERE
            self.get_classes_on_page()
            for x in range(0, len(self.classes_list)):
                self.click_class(x)
                self.get_class_info()
                self.send_info()
                self.close_class()

            print 'working'
            counter = counter + 1
            if counter == self.total_pages:
                break
        print 'Done'


def arguments_reader(retriever):
    try:
        sys.argv.index('-r')
        retriever.reverse_order()
        sys.argv.pop(sys.argv.index('-r'))
    except:
        pass
    try:
        sys.argv.index('-h')
        retriever.half_total_pages()
        sys.argv.pop(sys.argv.index('-h'))
    except:
        pass


    # if len(sys.argv) >= 2:
        # retriever.set_start_page(sys.argv[1])
        # if len(sys.argv) == 3:
            # retriever.set_end_page(sys.argv[2])

if __name__ == '__main__':
    firebase = firebase.FirebaseApplication('https://cs180-bf6af.firebaseio.com/', authentication=None)
    retriever = ClassSearch()
    arguments_reader(retriever)
    retriever.start_connection()
    retriever.term_select()
    retriever.click_search()
    retriever.increase_classes_per_page()
    retriever.iterate_pages()
    retriever.end_connection()

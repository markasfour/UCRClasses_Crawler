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
        print 'Catalog Description: ' \
                + self.CatalogDescription.strip('\n')
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
        self.quarter = \
                quarter_translate(self.driver.find_element_by_id('select2-result-label-2'
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
        total_pages = \
                self.driver.find_element_by_class_name('total-pages').text
        page_size_element = \
                Select(self.driver.find_element_by_class_name('page-size-select'
                             ))
        page_size_element.select_by_value('50')
        while 1:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                            'total-pages')))
            try:
                if self.driver.find_element_by_class_name('total-pages'
                                ).text != total_pages:
                    self.total_pages = \
                            int(self.driver.find_element_by_class_name('total-pages'
                                    ).text)
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
            pass
#
#        #Available Seats
#        try:        
#            self.driver.find_element_by_id('enrollmentInfo').click()
#            time.sleep(.5)
#            self.class_info.AvailableSeats = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[6]').text
#        except:
#            pass
#
#        #Building Name
#        try:
#            self.driver.find_element_by_id('facultyMeetingTimes').click()
#            time.sleep(.5)
#            if(self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]').text == ""):
#                pass
#            else:
#                self.class_info.BuildingName = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]').text
#        except:
#            pass
#
#        #CALL NUMBER
#        try:
#            self.class_info.CallNo = find_between(class_details, 'CRN:', 'Campus:').strip()
#        except:
#            pass
#
#        #DAYS
#        try:
#            self.driver.find_element_by_id('facultyMeetingTimes').click()
#            print "in"
#            time.sleep(.5)
#            
#            //*[@id="table1"]/tbody/tr[2]/td[8]
#            
#            sun = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[1]').get_attribute('aria-checked')
#            mon = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[2]').get_attribute('aria-checked')
#            tue = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[3]').get_attribute('aria-checked')
#            wed = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[4]').get_attribute('aria-checked')
#            thur = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[5]').get_attribute('aria-checked')
#            fri = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[6]').get_attribute('aria-checked')
#            sat = self.driver.find_element_by_xpath('//*[@id="201710.30363div"]/ul/li[7]').get_attribute('aria-checked')
#            temp = ""
#            if(sun == "true"):
#                temp += "Sunday\n"
#            if(mon == "true"):
#                temp += "Monday\n"
#            if(tue == "true"):
#                temp += "Tuesday\n"
#            if(wed == "true"):
#                temp += "Wednesday\n"
#            if(thur == "true"):
#                temp += "Thursday\n"
#            if(fri == "true"):
#                temp += "Friday\n"
#            if(sat == "true"):
#                temp += "Saturday\n"
#            self.class_info.Days = temp
#            print self.class_info.Days        
#        
#        except:
#            print "pass"
#            pass
#        
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
            try:
                noinstructor = self.class_info.Instructor = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span/text()').text
                noinstructor = "Instructor not yet available"
            except:
                noinstructor = ""
                pass
            
            allinstructors = instructor1 + " " + instructor2 + " " + noinstructor
            self.class_info.Instructor = allinstructors
            print self.class_info.Instructor
            
            #//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span[1]/span[1]/a
            #//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span[2]/span/a
            #//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span/text()
            
        except:
            pass
#            
#        #Max Enrollment
#        try:
#            self.driver.find_element_by_id('enrollmentInfo').click()
#            time.sleep(.5)
#            self.class_info.MaxEnrollment = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[4]').text
#        except:
#            pass
#            
#        #Num on WaitList
#        try:
#            self.driver.find_element_by_id('enrollmentInfo').click()
#            time.sleep(.5)
#            self.class_info.NumberonWaitList = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[10]').text
#        except:
#            pass
#
#        #time
#        try:
#            self.driver.find_element_by_id('facultyMeetingTimes').click()
#            time.sleep(.5)
#            self.class_info.Time = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[1]').text
#        except:
#            pass
#
#        #wait list max
#        try:
#            self.driver.find_element_by_id('enrollmentInfo').click()
#            time.sleep(.5)
#            self.class_info.WaitListMax = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[8]').text
#        except:
#            pass
#
#        #SCHEDULE TYPE
#        try:
#            self.class_info.LEC_DIS = find_between(class_details, 'Schedule Type:', 'Instructional')
#        except:
#            pass
#            
#        #SUBJECT
#        try:
#            self.class_info.Subject = find_between(class_details, 'Subject:' , 'Course Number:')
#        except:
#            pass
#
#        #COURSE NUM
#        try:
#            self.class_info.CourseNum = find_between(class_details, 'Course Number:', 'Title:')
#        except:
#            pass
#
#        #COURSE TITLE
#        try:
#            self.class_info.CourseTitle = find_between(class_details, 'Title:', 'Units:')
#        except:
#            pass
#
#        #UNITS
#        try:
#            self.class_info.Units = find_between(class_details, 'Units:',
#                        'Grade Mode:')
#        except:
#            pass
#            
#        #CATALOG DESCRIPTION
#        try:
#            self.driver.find_element_by_id('courseDescription').click()
#            time.sleep(.5)
#            self.class_info.CatalogDescription = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
#            self.driver.find_element_by_id('facultyMeetingTimes').click()
#            class_details_2 = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
#            self.driver.find_element_by_id('enrollmentInfo').click()
#            class_details_3 = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
#        except:
#            pass
#
#        #PREREQUISITES
#        try:
#            self.driver.find_element_by_id('preReqs').click()
#            time.sleep(.5)
#            self.class_info.Prerequisites = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
#        except:
#            pass
#
#        #COREQUISITES
#        try:
#            self.driver.find_element_by_id('coReqs').click()
#            time.sleep(.5)
#            self.class_info.Co_requisites = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
#        except:
#            pass
#
#        #RESTRICTIONS
#        try:
#            self.driver.find_element_by_id('restrictions').click()
#            time.sleep(.5)
#            self.class_info.Restrictions = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text
#        except:
#            pass
#            
#            
#        self.class_info.print_info()

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
                self.close_class()

            print 'working'
            counter = counter + 1
            if counter == self.total_pages:
                break
        print 'Done'

    def get_info(self, subject):
        for x in range(2, 12):
            try:
                if x < 10:
                    popup = \
                            "javascript:__doPostBack('grid_students$ctl0" \
                            + str(x) + "$lnkbtn_courseTitle','')"
                else:
                    popup = \
                            "javascript:__doPostBack('grid_students$ctl" \
                            + str(x) + "$lnkbtn_courseTitle','')"

                table = []
                self.driver.find_element_by_xpath('//a[@href="' + popup
                                + '"]').click()

    # time.sleep(3)

                self.wait.until(EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="exposeMask"][contains(@style, "display: block; opacity: 0.8")]'
                                                )))
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_courseTitle"]/b/font'
                                             ).text)
                except:
                    table.append('TEST TEST TEST')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_courseNum"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_callNo"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_instructor"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_units"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_maxEnrollment"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[1]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[2]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[3]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[4]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_classActivities"]/table/tbody/tr/td[5]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_availableSeats"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_waitlistMax"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_onWaitList"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_coquisites"]/font'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_prerequisties"]/font'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_restrictionsA"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_finalExamDate"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_finalExamDateA"]'
                                             ).text)
                except:
                    table.append('n/a')
                try:
                    table.append(self.driver.find_element_by_xpath('//*[@id="lbl_notes"]'
                                             ).text)
                except:
                    table.append('n/a')
                self.driver.find_element_by_xpath('//*[@id="ClassInfo"]/a'
                                ).click()

    # each table will have 0 to 19 indexes

                data = {
                        'Subject': subject,
                        'CourseTitle': table[0],
                        'CourseNum': table[1],
                        'CallNo': table[2],
                        'Instructor': table[3],
                        'Units': table[4],
                        'MaxEnrollment': table[5],
                        'Lec_Dis': table[6],
                        'Days': table[7],
                        'Time': table[8],
                        'RoomAbrv': table[9],
                        'BuildingName': table[10],
                        'AvailableSeats': table[11],
                        'WaitListMax': table[12],
                        'NumberonWaitList': table[13],
                        'Co-requisites': table[14],
                        'Prerequisites': table[15],
                        'Restrictions': table[16],
                        'FinalExamDate': table[17],
                        'FinalExamTime': table[18],
                        'CatalogDescription': table[19],
                        }

    # Do not send data to DB if there is no CourseNum

                if table[1] == '' or table[1] == 'n/a':
                    continue

                result = requests.patch(firebase_url + '/'
                                + self.quarter + '/' + subject + '/' + table[2]
                                + '.json', data=json.dumps(data))
                print 'Record inserted. Result Code = ' \
                        + str(result.status_code) + ',' + result.text
            except:

    # time.sleep(3)

                continue


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
    firebase = \
            firebase.FirebaseApplication('https://cs180-bf6af.firebaseio.com/'
                    , authentication=None)
    retriever = ClassSearch()
    arguments_reader(retriever)
    retriever.start_connection()
    retriever.term_select()
    retriever.click_search()
    retriever.increase_classes_per_page()
    retriever.iterate_pages()
    retriever.end_connection()

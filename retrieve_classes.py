#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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
        self.AvailableSeats = self.AvailableSeats.replace('\n', ' ')
        self.BuildingName = self.BuildingName.replace('\n', ' ')
        self.CallNo = self.CallNo.replace('\n', '')
        self.CatalogDescription = self.CatalogDescription.replace('\n', ' ')
        self.Co_requisites = self.Co_requisites.replace('\n', ' ')
        self.CourseNum = self.CourseNum.replace('\n', ' ')
        self.CourseTitle = self.CourseTitle.replace('\n', ' ')
        self.Days = self.Days.replace('\n', ' ')
        self.FinalExamDate = self.FinalExamDate.replace('\n', ' ')
        self.FinalExamTime = self.FinalExamTime.replace('\n', ' ')
        self.Instructor = self.Instructor.replace('\n', ' ')
        self.Lec_Dis = self.Lec_Dis.replace('\n', ' ')
        self.MaxEnrollment = self.MaxEnrollment.replace('\n', ' ')
        self.NumberonWaitList = self.NumberonWaitList.replace('\n', ' ')
        self.Prerequisites = self.Prerequisites.replace('\n', ' ')
        self.Restrictions = self.Restrictions.replace('\n', ' ')
        self.RoomAbrv = self.RoomAbrv.replace('\n', ' ')
        self.Subject = self.Subject.replace('\n', ' ')
        self.Time = self.Time.replace('\n', ' ')
        self.Units = self.Units.replace('\n', ' ')
        self.WaitListMax = self.WaitListMax.replace('\n', ' ')


class ClassSearch:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.quarter = ''
        self.reverse = 0
        self.half = 0
        self.total_pages = 0
        self.classes_list = []
        self.class_info = course()
        self.wait = WebDriverWait(self.driver, 3)
        self.start_page = 0

    def start_connection(self):
        driver = self.driver
        driver.get('http://classes.ucr.edu')

    def end_connection(self):
        self.driver.close()

    def reverse_order(self):
        self.reverse = 1

    def half_total_pages(self):
        half = 1

    def set_start_page(self, page):
        text_box = self.driver.find_element_by_class_name('page-number')
        text_box.clear()
        text_box.send_keys(page)
        text_box.send_keys(Keys.ENTER)
        
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
        try:
            self.classes_list[x].click()
        except:
            return -1 
        try:
            self.wait.until(EC.presence_of_element_located((By.ID,
                                            'courseReferenceNumber')))
        except:
            pass
        return 0 

    def close_class(self):
        self.driver.find_element_by_class_name('ui-icon-closethick'
                        ).click()
        try:
            self.wait.until(EC.invisibility_of_element_located((By.ID,
                                            'courseReferenceNumber')))
        except:
            pass
######################################################################################################
    def abreviate_subjects(self, subject):
        try:
            temp = ""
            if(subject == "Academic Resource Center"):
                temp = "ARC"
            elif(subject == "Anthropology"):
                temp = "ANTH"
            elif(subject == "Arabic Language"):
                temp = "ARBC"
            elif(subject == "Arabic Literature and Cultures"):
                temp = "ARLC"
            elif subject == "Art" or subject == "Art History":
                temp = "ART"
            elif(subject == "Asian Studies"):
                temp = "AST"
            elif(subject == "Biochemistry"):
                temp = "BCH"
            elif(subject == "Bioengineering"):
                temp = "BIEN"
            elif(subject == "Biology"):
                temp = "BIOL"
            elif(subject == "Biomedical Sciences"):
                temp = "BMSC"
            elif(subject == "Botany/Plant Science"):
                temp = "BPSC"
            elif(subject == "Basic Writing"):
                temp = "BSWT"
            elif(subject == "Business"):
                temp = "BUS"
            elif(subject == "Cell Biology and Neuroscience"):
                temp = "CBNS"
            elif(subject == "Cell, Molecular, and Develpmnt"):
                temp = "CMDB"
            elif(subject == "Creative Writing"):
                temp = "CRWT"
            elif(subject == "Dance"):
                temp = "DNCE"
            elif(subject == "Economics"):
                temp = "ECON"
            elif(subject == "Education"):
                temp = "EDUC"
            elif(subject == "Global Studies"):
                temp = "GBST"
            elif(subject == "German"):
                temp = "GER"
            elif(subject == "Greek"):
                temp = "GRK"
            elif(subject == "Humanities, Arts and Soc Sci"):
                temp = "HASS"
            elif(subject == "History of the Americas"):
                temp = "HISA"
            elif(subject == "History of Europe"):
                temp = "HISE"
            elif(subject == "History"):
                temp = "HIST"
            elif(subject == "Honors"):
                temp = "HNPG"
            elif(subject == "Italian"):
                temp = "ITAL"
            elif(subject == "Japanese"):
                temp = "JPN"
            elif(subject == "Korean"):
                temp = "KOR"
            elif(subject == "Latin"):
                temp = "LATN"
            elif(subject == "Lesbian, Gay, Bisexual Studies"):
                temp = "LGBS"
            elif(subject == "Linguistics"):
                temp = "LING"
            elif(subject == "Latin American Studies"):
                temp = "LNST"
            elif(subject == "Law & Society"):
                temp = "LWSO"
            elif(subject == "Mathematics"):
                temp = "MATH"
            elif(subject == "Microbiology"):
                temp = "MCBL"
            elif(subject == "Media and Cultural Studies"):
                temp = "MCS"
            elif(subject == "School of Medicine"):
                temp = "MDCL"
            elif(subject == "Mechanical Engineering"):
                temp = "ME"
            elif(subject == "Middle East and Islamic Studies"):
                temp = "MEIS"
            elif(subject == "Management"):
                temp = "MGT"
            elif(subject == "Materials Sci and Engineering"):
                temp = "MSE"
            elif(subject == "Music"):
                temp = "MUS"
            elif(subject == "Natural &Agricultural Sciences"):
                temp = "NASC"
            elif(subject == "Nematology"):
                temp = "NEM"
            elif(subject == "Neuroscience"):
                temp = "NRSC"
            elif(subject == "Public Policy"):
                temp = "PBPL"
            elif(subject == "Peace and Conflict Studies"):
                temp = "PCST"
            elif(subject == "Philosophy"):
                temp = "PHIL"
            elif(subject == "Physics"):
                temp = "PHYS"
            elif(subject == "Plant Pathology"):
                temp = "PLPA"
            elif(subject == "Political Science"):
                temp = "POSC"
            elif(subject == "Psychology"):
                temp = "PSYC"
            elif(subject == "Recreation"):
                temp = "REC"
            elif(subject == "Religious Studies"):
                temp = "RLST"
            elif(subject == "Russian Studies"):
                temp = "RUSN"
            elif(subject == "Southeast Asian Studies"):
                temp = "SEAS"
            elif(subject == "Sociology"):
                temp = "SOC"
            elif(subject == "Spanish"):
                temp = "SPN"
            elif(subject == "Statistics"):
                temp = "STAT"
            elif(subject == "Soil and Water Science"):
                temp = "SWSC"
            elif(subject == "Theater, Film & Digital Prod"):
                temp = "TFDP"
            elif(subject == "Urban Studies"):
                temp = "URST"
            elif(subject == "Vietnamese"):
                temp = "VNM"
            return temp
        except:
            temp = subject + "?"
            return temp
######################################################################################################

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
            self.class_info.AvailableSeats = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[6]').text.replace('\n', '')
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
                self.class_info.BuildingName = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]').text.replace('\n', ' ')
                
                tempBuildingName = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[2]').text.replace('\n', ' ')
                indexBuildingName = 0
                while indexBuildingName >= 0:
                    indexBuildingName = tempBuildingName.find("|")
                    tempBuildingName = tempBuildingName[indexBuildingName+1:]
                
                self.class_info.RoomAbrv = tempBuildingName
        except:
            self.class_info.BuildingName = "n/a"
            pass

        #CALL NUMBER
        try:
#            self.class_info.CallNo = find_between(class_details, 'CRN: ', 'Campus:')
            self.driver.find_element_by_id('classDetails').click()
            time.sleep(.5)
            self.class_info.CallNo = self.driver.find_element_by_xpath('//*[@id="courseReferenceNumber"]').text.replace(' ', '')
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
                    temp += "SUN"
                if(mon == "true"):
                    temp += "M"
                if(tue == "true"):
                    temp += "T"
                if(wed == "true"):
                    temp += "W"
                if(thur == "true"):
                    temp += "R"
                if(fri == "true"):
                    temp += "F"
                if(sat == "true"):
                    temp += "SAT"
                self.class_info.Days = temp.replace('\n', ' ')

        except:
            self.class_info.Days = "n/a"
            tableInc()
            pass

        #instructor name
        try:
            self.driver.find_element_by_id('facultyMeetingTimes').click()
            time.sleep(.5)
            try:
                instructor1 = self.class_info.Instructor = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span/span[1]/a').text.replace('\n', ' ')
            except:
                instructor1 = ""
                pass
            try:
                instructor2 = self.class_info.Instructor = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[1]/span[2]/span/a').text.replace('\n', ' ')
            except:
                instructor2 = ""
                pass

            allinstructors = instructor1 + " " + instructor2
            if (allinstructors == " "):
                allinstructors = "Instructors are not available yet. "

            self.class_info.Instructor = allinstructors.replace('\n', ' ')

        except:
            self.class_info.Instructor = "n/a"
            pass

        #Max Enrollment
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.MaxEnrollment = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[4]').text.replace('\n', ' ')
        except:
            self.class_info.MaxEnrollment = "n/a"
            pass

        #Num on WaitList
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.NumberonWaitList = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[10]').text.replace('\n', ' ')
        except:
            self.class_info.NumberonWaitList = "n/a"
            pass

        #time
        try:
            self.driver.find_element_by_id('facultyMeetingTimes').click()
            time.sleep(.5)
            self.class_info.Time = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/div/div[2]/div/div[2]/div[1]').text.replace('\n', ' ')
        except:
            self.class_info.Time = "n/a"
            pass

        #wait list max
        try:
            self.driver.find_element_by_id('enrollmentInfo').click()
            time.sleep(.5)
            self.class_info.WaitListMax = self.driver.find_element_by_xpath('//*[@id="classDetailsContentDetailsDiv"]/span[8]').text.replace('\n', ' ')
        except:
            self.class_info.WaitListMax = "n/a"
            pass

        #SCHEDULE TYPE
        try:
            tempLecDis = find_between(class_details, 'Schedule Type: ', '\nInstructional')
            if tempLecDis == "Lecture":
                self.class_info.Lec_Dis = "LEC"
            elif tempLecDis[0:3] == "Act":
                self.class_info.Lec_Dis = "ACT"
            elif tempLecDis[0:3] == "Add":
                self.class_info.Lec_Dis = "LCA"
            elif tempLecDis[0:3] == "Cli":
                self.class_info.Lec_Dis = "CLN"
            elif tempLecDis[0:3] == "Col":
                self.class_info.Lec_Dis = "COL"
            elif tempLecDis[0:3] == "Con":
                self.class_info.Lec_Dis = "CON"
            elif tempLecDis[0:3] == "Dem":
                self.class_info.Lec_Dis = "DEM"
            elif tempLecDis == "Discussion":
                self.class_info.Lec_Dis = "DIS"
            elif tempLecDis == "Discussion, Lab, and Lecture":
                self.class_info.Lec_Dis = "DLL"
            elif tempLecDis[0:3] == "Field":
                self.class_info.Lec_Dis = "FLD"
            elif tempLecDis[0:3] == "Ind":
                self.class_info.Lec_Dis = "IND"
            elif tempLecDis[0:3] == "Int":
                self.class_info.Lec_Dis = "INT"
            elif tempLecDis[0:3] == "Lab":
                self.class_info.Lec_Dis = "LAB"
            elif tempLecDis == "Lecture and Discussion":
                self.class_info.Lec_Dis = "LCD"
            elif tempLecDis == "Lecture and Laboratory":
                self.class_info.Lec_Dis = "LCL"
            elif tempLecDis == "Lecture, Lab, Field":
                self.class_info.Lec_Dis = "LLF"
            elif tempLecDis == "Lecture, Sem, Lab & Sch Res":
                self.class_info.Lec_Dis = "LSLSR"
            elif tempLecDis[0:3] == "Onl":
                self.class_info.Lec_Dis = "ODL"
            elif tempLecDis[0:3] == "Pra":
                self.class_info.Lec_Dis = "Practium"
            elif tempLecDis[0:3] == "Rea":
                self.class_info.Lec_Dis = "RED"
            elif tempLecDis[0:3] == "Res":
                self.class_info.Lec_Dis = "RESB"
            elif tempLecDis[0:3] == "Scr":
                self.class_info.Lec_Dis = "SCR"
            elif tempLecDis == "Seminar":
                self.class_info.Lec_Dis = "SEM"
            elif tempLecDis == "Seminar and Laboratory":
                self.class_info.Lec_Dis = "SL"
            elif tempLecDis[0:3] == "Stu":
                self.class_info.Lec_Dis = "STU"
            elif tempLecDis[0:3] == "Ter":
                self.class_info.Lec_Dis = "TRP"
            elif tempLecDis[0:3] == "The":
                self.class_info.Lec_Dis = "THE"
            elif tempLecDis[0:3] == "Tut":
                self.class_info.Lec_Dis = "TUT"
            elif tempLecDis == "Workshop":
                self.class_info.Lec_Dis = "WRK"
            elif tempLecDis == "Workshop and Screening":
                self.class_info.Lec_Dis = "WKS"
            elif tempLecDis[0:3] == "Wri":
                self.class_info.Lec_Dis = "WWK"                
        except:
            self.class_info.Lec_Dis = "n/a"
            pass

        #SUBJECT
        try:
#            self.class_info.Subject = find_between(class_details, 'Subject: ' , '\nCourse Number:')
            self.driver.find_element_by_id('classDetails').click()
            time.sleep(.5)
            self.class_info.Subject = self.abreviate_subjects(self.driver.find_element_by_xpath('//*[@id="subject"]').text)
            print self.class_info.Subject
            time.sleep(10)
        except:
            self.class_info.Subject = "n/a"
            pass

        #COURSE NUM
        try:
#            self.class_info.CourseNum = find_between(class_details, 'Course Number: ', '\nTitle:')
            self.driver.find_element_by_id('classDetails').click()
            time.sleep(.5)
            tempSubject = self.class_info.Subject
            tempCourseNum = self.driver.find_element_by_xpath('//*[@id="courseNumber"]').text
            sectionNum = self.driver.find_element_by_xpath('//*[@id="sectionNumber"]').text
            self.class_info.CourseNum = tempSubject + " " + tempCourseNum + " - " + sectionNum
        except:
            self.class_info.CourseNum = "n/a"
            pass

        #COURSE TITLE
        try:
#            self.class_info.CourseTitle = find_between(class_details, 'Title: ', '\nUnits:')
            self.driver.find_element_by_id('classDetails').click()
            time.sleep(.5)
            self.class_info.CourseTitle = self.driver.find_element_by_xpath('//*[@id="courseTitle"]').text
        except:
            self.class_info.CourseTitle = "n/a"
            pass

        #UNITS
        try:
            self.class_info.Units = find_between(class_details, 'Units: ', '\nGrade Mode:')
#            self.driver.find_element_by_id('classDetails').click()
#            time.sleep(.5)
#            self.class_info.CourseNum = self.driver.find_element_by_xpath('//*[@id="courseTitle"]').text
        except:
            self.class_info.Units = "n/a"
            pass

        #CATALOG DESCRIPTION
        try:
            self.driver.find_element_by_id('courseDescription').click()
            time.sleep(.5)
            self.class_info.CatalogDescription = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text.replace('\n', ' ')
            self.driver.find_element_by_id('facultyMeetingTimes').click()

            #not used for anything
            class_details_2 = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text.replace('\n', ' ')
            self.driver.find_element_by_id('enrollmentInfo').click()
            class_details_3 = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text.replace('\n', ' ')
        except:
            self.class_info.CatalogDescription = "n/a"
            pass

        #PREREQUISITES
        try:
            self.driver.find_element_by_id('preReqs').click()
            time.sleep(.5)
            self.class_info.Prerequisites = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text.replace('\n', ' ')
        except:
            self.class_info.Prerequisites = "n/a"
            pass

        #COREQUISITES click link below?
        try:
            self.driver.find_element_by_id('coReqs').click()
            time.sleep(.5)
            self.class_info.Co_requisites = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text.replace('\n', ' ')
        except:
            self.class_info.Co_requisites = "n/a"
            pass

        #RESTRICTIONS click link below?
        try:
            self.driver.find_element_by_id('restrictions').click()
            time.sleep(.5)
            self.class_info.Restrictions = self.driver.find_element_by_id('classDetailsContentDetailsDiv').text.replace('\n', ' ')
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

#        self.class_info.clean_data()
        temp_Subject = self.class_info.Subject
        temp_callNo = self.class_info.CallNo
        result = requests.patch(firebase_url + '/' + self.quarter + '/' + temp_Subject + '/' + temp_callNo + '.json', data=json.dumps(data))
        print 'Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text


    def iterate_pages(self):
        counter = 1
        time.sleep(3)
        if self.reverse:
            self.driver.find_element_by_class_name('last').click()
            try:
                #self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                #'loading')))
                time.sleep(3)
            except:
                pass
            #try:
                #self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,
                                                #'loading')))
            #except:
                #pass

        if self.start_page != 0:
            retriever.set_start_page(self.start_page)
            print "Starting at page " + str(self.start_page)
            time.sleep(3)

     # GET INITIAL PAGE CLASS INFORMATION HERE
        self.get_classes_on_page()
        for x in range(0, len(self.classes_list)):
            time.sleep(2)
            if self.click_class(x) == -1:
                print "UNCLICKABLE CLASS!!!"
                continue
            self.get_class_info()
            self.send_info()
            self.close_class()

        while self.get_next_page():
            try:
                #self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                #'loading')))
                time.sleep(3)
            except:
                pass
            #try:
                #self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME,
                                                #'loading')))
            #except:
                #pass

     # GET CLASS INFORMATION HERE
            self.get_classes_on_page()
            for x in range(0, len(self.classes_list)):
                time.sleep(2)
                if self.click_class(x) == -1:
                    print "UNCLICKABLE CLASS!!!"
                    continue
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


    if len(sys.argv) >= 2:
        retriever.start_page = sys.argv[1] 
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

# https://www.youtube.com/watch?v=twRQNSFXiYs

import argparse
import os
import time
import urlparse
import random
from selenium import webdriver
# from selenium. webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def getPeopleLinks(page):  # a beautifulSoup page instance
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)
    return links


def getJobsLinks(page):  # a beautifulSoup page instance
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/job' in url:
                links.append(url)
    return links


def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]


def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    while True:
        # sleep to make sure everything loads.
        # add random to make us look human
        time.sleep(random.uniform(3.5, 6.9))
        page = BeautifulSoup(browser.page_source)
        people = getPeopleLinks(page)  # list of people links
        if people and len(pList) <= 10:
            for person in people:
                ID = getID(person)
                if ID not in visited:
                    pList.append(person)
                    visited[ID] = 1
        if pList:  # If there is people to look at, look
            person = pList.pop(random.randrange(0, len(pList)))
            browser.get(person)
            count += 1
        else:  # otherwise find people via the job pages
            jobs = getJobsLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'http://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'http://www.linkedin.com' + job
                browser.get(job)
            else:
                print "I'm Lost Exiting"
                break
        print '[+]', browser.title, 'Visited! \n(', count, '/', len(pList), ') Visited / Queue\n'


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='linkedIn email')
    parser.add_argument('password', help='linkedIn password')
    args = parser.parse_args()

    browser = webdriver.Firefox()
    browser.get('https://www.linkedin.com/uas/login')
    time.sleep(5)
    emailElement = browser.find_element_by_id('session_key-login')
    emailElement.send_keys(args.email)
    passElement = browser.find_element_by_id('session_password-login')
    passElement.send_keys(args.password)
    passElement.submit()

    os.system('clear')
    print 'XD'
    print '[+] Succes!! loggedIN, bot starting!!'
    ViewBot(browser)
    browser.close()

if __name__ == '__main__':
    Main()

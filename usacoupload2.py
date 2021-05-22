from selenium import webdriver
import re
import os
import time

driver = webdriver.Firefox()

driver.get("http://usaco.org")
assert "USACO" in driver.title

username = driver.find_element_by_name("uname")
username.clear()
username.send_keys("minyoungheo")

password = driver.find_element_by_name("password")
password.clear()
password.send_keys("a32ede5")

driver.find_element_by_xpath("//input[@value='Login']").click()

logoutButton = driver.find_elements_by_xpath('//button[text()="Logout"]')
if len(logoutButton) > 0:
    print('Logged in!')
    year = 0
    while True:
        year = input("Which year? (2015-2021) ")
        if re.search("20(1[5-9]|2[01])", year):
            year = int(year)
            break
        else:
            print("Error: please enter a valid year")
    month = ""
    while True:
        month = input("Which month? (dec, jan, feb, open) ")
        if re.search("dec|jan|feb|open", month):
            break
        else:
            print("Error: please enter a valid month")
    division = ""
    while True:
        division = input("Which division? (bronze, silver, gold, platinum) ")
        if re.search("bronze|silver|gold|platinum", division):
            break
        else:
            print("Error: please enter a valid division")
    driver.get('http://usaco.org/index.php?page={}{}results'.format(month,year%100))
    allproblems = driver.find_elements_by_xpath("//div[@class='panel historypanel']")
    index = 0
    if division == 'bronze':
        index = 9
    elif division == 'silver':
        index = 6
    elif division == 'gold':
        index = 3
    divisionproblems = []
    for i in range(3):
        divisionproblems.append(allproblems[index+i].find_element_by_tag_name('b'))
    problemChoice = 0
    while True:
        for i, divisionproblem in enumerate(divisionproblems):
            print("{}: {}".format(i+1, divisionproblem.text))
        problemChoice = input("Which problem? (1-{}) ".format(len(divisionproblems)))
        if re.search("[1-{}]".format(len(divisionproblems)), problemChoice):
            problemChoice = int(problemChoice)-1
            break
        else:
            print('Error: please enter a valid problem choice')
    problemLink = allproblems[index + problemChoice].find_element_by_tag_name('a').get_attribute('href')
    driver.get(problemLink)
    driver.find_element_by_name("language").find_element_by_xpath("//option[@value='7']").click()
    print(os.getcwd()+"\\billboard.cpp")
    driver.find_element_by_name("sourcefile").send_keys(os.getcwd()+"\\billboard.cpp")
    driver.find_element_by_name("solution-submit").click()
    print('Submitted...Please Wait...')
    for i in range(20, -1, -1):
        print('{} seconds'.format(i))
        time.sleep(1)
    result = driver.find_element_by_id("trial-information")
    results = result.find_elements_by_tag_name('a')
    print('Here is the result of your submission: ')
    for i, r in enumerate(results):
        print("case {}: {}".format(i+1, r.get_attribute('title')))
else:
    print('hmmmmm')
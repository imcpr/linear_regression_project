from bs4 import BeautifulSoup
import urllib2
import time
import random
import praw
import pickle

def getID(url):
    comm = False
    id = ""
    for str in url.split("/") :
        if comm :
            id = str         
            break
        if str == "comments" :
            comm = True
    print id
    if id != "" :
        return id
    return ""

def readReddit(allIds) :
    r = praw.Reddit(user_agent='Machine Learning 598 crawler by Eric Quinn')
    
    submissions = []
    i = 0    
    for id in allIds :
        submission = r.get_submission(submission_id = id)
        submissions.append(submission)
        print(submission.title)
        print(str(i) + " / " + str(len(allIds)))
        i += 1
        
    i = 0
    output = open("cmv_submissions", "w")
    pickle.dump(submissions, output)
    output.close()

def collectIDS():
    s = BeautifulSoup(open('data/new_cmv.html'))

    f = open('cmv', 'a')
    for i in range(0, 100):
        entries = s.findAll("div", {"class": "entry"})

        for entry in entries:
            a = entry.findAll("a", {"class":"title"})
            link = a[0]['href']
            print link
            f.write(getID(link)+"\n")

        n = s.findAll("span", {"class":"nextprev"})
        next_page = n[0].findAll("a")[1]['href']
        print "next page " + next_page
        time.sleep(30)
        page = urllib2.urlopen(next_page).read()
        s = BeautifulSoup(page)
    f.close()

with open('cmv') as f:
    allIds = f.readlines()
    readReddit(allIds)
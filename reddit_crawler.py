from bs4 import BeautifulSoup
import urllib2
import time
import random
import praw
import pickle

# returns the reddit post id from a reddit link URL
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

# uses the PRAW API to get the submission object from Reddit by each post ID given
# allIds: a list containing strings of ids of reddit posts we want to capture
# outputs a pickled file of the list of submission objects
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
    output = open("reddit_submissions", "w")
    pickle.dump(submissions, output)
    output.close()


# web scraper to follow reddit new links and scrape all the URLs
s = BeautifulSoup(open('data/reddit.html'))

f = open('reddit', 'a')
for i in range(0, 100):
    entries = s.findAll("div", {"class": "entry"})

    for entry in entries:
        a = entry.findAll("a", {"class":"title"})
        link = a[0]['href']
        print link
        f.write(getID(link)+"\n")

    n = s.findAll("span", {"class":"nextprev"})
    # if there is next page
    try:
        next_page = n[0].findAll("a")[1]['href']
    except:
        break
    print "next page " + next_page
    time.sleep(30)
    page = urllib2.urlopen(next_page).read()
    s = BeautifulSoup(page)
f.close()

with open('reddit') as f:
    allIds = f.readlines()
    readReddit(allIds)
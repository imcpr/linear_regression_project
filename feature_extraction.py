import pickle
from datetime import datetime
from random import shuffle
import indicoio
from indicoio import political, sentiment
import csv

word_feature_map = {'danish': 63, 'petting': 36, 'gold': 26, 'housewarming': 48, 'Lil': 21, 'pussy': 35, 'jewellers': 30, 'lascivious': 42, 'skinning': 56, 'flattering': 58, 'fuckups': 32, 'airplane': 34, 'bongs': 46, 'belt': 41, 'quiero': 45, 'skitzo': 57, 'flaming': 52, 'charisma': 59, 'darted': 38, 'avail': 39, 'wrestling': 37, 'jaws': 68, 'pristine': 20, 'movements': 28, 'Gollum': 53, 'fines': 47, 'rapid-fire': 43, 'redoing': 51, 'Denmark': 27, 'sorrow': 31, 'pained': 23, 'factored': 29, 'Insert': 61, 'purring': 66, 'milestone': 24, 'Knocked': 33, 'cape': 54, 'low-budget': 62, 'Smeagol': 55, 'bewildered': 40, 'nectar': 22, 'cuckoo': 49, 'meow': 67, 'evade': 69, 'repellent': 50, 'mosquito': 25, 'clears': 60, 'Syrian': 65, 'giggly': 44, 'arabic': 64}
indicoio.config.api_key = '2e0f865e9cc4e4f4be74452ec7d78c39'

def get_indico_features(posts):
    texts = [ post.title.encode('UTF8') for post in posts]
    print "Getting sentiment scores..."
    sentiment = indicoio.batch_sentiment(texts)
    print "Getting political scores..."
    political = indicoio.batch_political(texts)

    return (sentiment, political)

def set_features(post, sentiment, political):
    f = [0]*71
    f[0] = len(post.title)
    f[1] = len(post.selftext)
    utc = post.created_utc
    creation_time = datetime.utcfromtimestamp(utc)
    dayOfWeek = creation_time.today().weekday()
    timeOfDay = creation_time.hour * 60 * 60 + creation_time.minute * 60 + creation_time.second
    timeOfDaySq = timeOfDay * timeOfDay
    f[2] = timeOfDay
    f[3] = timeOfDaySq
    f[dayOfWeek+4] = 1
    if (post.subreddit_id == 'qqqqqq'): #changemyview
        f[11] = 1
    if (post.subreddit_id == 't5_2qjvn'): #relationships
        f[12] = 1
    if (post.subreddit_id == 't5_2qh96'): #self
        f[13] = 1
    if (post.subreddit_id == 't5_2to41'): #tifu
        f[14] = 1
    f[15] = sentiment
    f[16] = political["Liberal"]
    f[17] = political["Libertarian"]
    f[18] = political["Conservative"]
    f[19] = political["Green"]
    # add one to each word seen
    for word in post.selftext.split(" "):
        if (word in word_feature_map):
            f[word_feature_map[word]] += 1
    # upvotes
    f[70] = post.score
    return f

def posts_to_matrix(submissions):
    (sentiment, political) = get_indico_features(submissions)
    data = numpy.matrix(set_features(submissions[0], sentiment[0], political[0]))
    for i in range(1, len(submissions)):
        print "Extracting submission %d" % i
        # create one row 
        temp = numpy.matrix(set_features(submissions[i], sentiment[i], political[i]))
        # stack on previous matrix
        data = numpy.vstack((data, temp))
    (rows,cols) = data.shape

    X = data[:, :cols-1]
    Y = data[:, cols-1:]
    return (X, Y)

def posts_to_csv(filename, submissions):
    (sentiment, political) = get_indico_features(submissions)
    inputs = []
    for i in range(0, len(submissions)):
        print "Extracting submission %d" % i
        # create one row 
        inputs.append(set_features(submissions[i], sentiment[i], political[i]))
    write_to_csv(filename, inputs)
    return (sentiment, political)


def write_to_csv(filename, data):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in data:
            writer.writerow(row)
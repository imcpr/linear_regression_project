# COMP 598:<br/>Linear Regression Mini Project 1
by Casper Liu, Eric Quinn, Howard Huang

Detailed project report can be found here: https://github.com/imcpr/linear_regression_project/blob/master/report/report.pdf

## Dependencies
In our code, we used several libraries, including numpy, praw, indicoio, nltk and progress.
To install, run
```
pip install numpy
pip install praw
pip install indicoio
```

## Running the code
In the python interpretor, run
```
execfile(`main.py`)
```
to load all the necessary code for the regression analysis

First, we must load the data set:
```
(X,Y) = (X,Y) = read_csv_into_matrices('data/OnlineNewsPopularity.csv', 2, 60)
# or 
(X,Y) = read_csv_into_matrices('reddit_full_data_76.csv', 0, 76)
```

To reproduce the data in the report, we normalize the data:
```
normalize_data(X)
```

Now that we have the X and Y variable, we can run the closed form linear regression:
```
# 0.01 is the lambda parameter for ridge regression
w_optimal = closed_form_regression(X, Y, 0.01)
```

To run the gradient descent algorithm, do:
```
# 0.01 is the learning rate, or alpha
# 10 is the lambda parameter
w_gradient = gradient_descent(X, Y, 1000, 0.01, 10)
```

To tune the hyperparameters, we can use the k-cross-validation algorithm:
```
# total_error = k_cross_validation(X, Y, k, iter, alpha, lambda)
total_error = k_cross_validation(X, Y, 5, 1000, 0.1, 10)
```
This reports the total error of this particular set of hyperparameters as a result of k fold cross validation.
To tune the hyperparameter, iterate through the cross validation step with different parameters and choose the one with lowest error.

To calculate the error using the w we optimized:
```
computeSSE(X, Y, w_optimal) # computes sum squared error
computePError(X, Y, w_optimal) # computes mean squared percentage error 
computeMSE(X, Y, w_optimal) # computes the MSE
```

To output the predicted Y vs. actual Y:
```
write_output("output.csv", X, Y, w_optimal)
```
which creates a csv file output.csv with one column of predicted Y and another of actual Y in matching rows for data plotting.


## Web Crawler
We used BeautifulSoup library combined with PRAW reddit API wrapper to gather the data.
To run the crawler, place the first reddit page to crawl at 'data/reddit.html'
and execute:
```
python reddit_crawler.py
```
It first uses BeautifulSoup library to crawl all the page links starting from the page of reddit.html, 
and follows the next page link until the end.
After saving the links to a file, we extract each unique post ID from the links, and use PRAW to visit each page.
At the end, each submission will be stored to a list and pickled to a file 'reddit_submissions'

## Feature Extraction

To extract the features from reddit posts, load the previously pickled file and convert to csv.
```
execfile('feature_extraction.py')
all_submissions = pickle.load(open('reddit_submissions'))
posts_to_csv("reddit_data.csv", all_submissions)
```


*README file by Casper*
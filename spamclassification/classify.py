__author__ = 'atanguturi'

"""
Assignment 4. Implement a Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

import glob
from collections import defaultdict
import math


class Document(object):
    """ A Document. DO NOT MODIFY.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename):
        self.filename = filename
        self.label = 'spam' if 'spmsg' in filename else 'ham'
        self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):

    def train(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your book.
        condprobdict maps token to list [spamcondprob,hamcondprob]
        """
        numberofhamdocs =0
        numberofdocs = len(documents)
        condprobdict = defaultdict(lambda: [1,1])
        numberofhamtoks = 0
        numberofspamtoks =0
        for each in documents:
            if each.label =="ham":
                numberofhamdocs +=1
            for every in each.tokens:
                if each.label == "ham":
                    condprobdict[every][1] += 1
                    numberofhamtoks +=1
                elif each.label == "spam":
                    condprobdict[every][0] += 1
                    numberofspamtoks +=1
        self.probofham = 1.*numberofhamdocs/numberofdocs
        numberofspamdocs = numberofdocs-numberofhamdocs
        self.probofspam = 1. *numberofspamdocs/numberofdocs
        vocab = len(condprobdict)
        hamdenom = vocab + numberofhamtoks
        spamdenom = vocab + numberofspamtoks
        self.conditionaldict = dict((x,[1.*y/spamdenom,1.*z/hamdenom]) for (x,[y,z]) in condprobdict.items())
        return

    def classify(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Return a list of strings, either 'spam' or 'ham', for each document.
        documents....A list of Document objects to be classified.
        """
        resultant_list = []
        for each in documents:
            hamprobscore = ["ham",math.log10(self.probofham)]
            spamprobscore = ["spam",math.log10(self.probofspam)]
            for every in each.tokens:
                if every in self.conditionaldict:
                    spamprobscore[1] += math.log10(self.conditionaldict[every][0])
                    hamprobscore[1] += math.log10(self.conditionaldict[every][1])
            resultant_list.append(max([hamprobscore,spamprobscore],key = lambda x: x[1])[0])
        return resultant_list


def evaluate(predictions, documents):
    """
    TODO: COMPLETE THIS METHOD.

    Evaluate the accuracy of a set of predictions.
    Print the following:
    accuracy=xxx, yyy false spam, zzz missed spam
    where
    xxx = percent of documents classified correctly
    yyy = number of ham documents incorrectly classified as spam
    zzz = number of spam documents incorrectly classified as ham

    See the provided log file for the expected output.

    predictions....list of document labels predicted by a classifier.
    documents......list of Document objects, with known labels.
    """
    numcorrect = 0
    yyy = 0
    zzz = 0
    for i in range(0,len(predictions)):
        if predictions[i]==documents[i].label:
            numcorrect +=1
        elif documents[i].label=="ham":
            yyy +=1
        else:
            zzz +=1
    xxx = 1.*numcorrect/len(predictions)
    print "accuracy=%.3f, %d false spam, %d missed spam "% (xxx,yyy,zzz)
    return

def main():
    """ DO NOT MODIFY. """
    train_docs = [Document(f) for f in glob.glob("train/*.txt")]
    print 'read', len(train_docs), 'training documents.'
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(f) for f in glob.glob("test/*.txt")]
    print 'read', len(test_docs), 'testing documents.'
    predictions = nb.classify(test_docs)
    evaluate(predictions, test_docs)

if __name__ == '__main__':
    main()

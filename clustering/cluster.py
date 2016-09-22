"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter,defaultdict
import io
import math

import numpy as np

def norm_squared(dicty):
    result = 0.
    for each in dicty:
        result += 1. * dicty[each]**2
    return result

def dotproduct(dictya,dictyb):
    dotprod = 0.
    for each in dictya:
        dotprod += 1. * dictya[each] * dictyb[each]
    return dotprod

class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        Each iteration consists of calls to compute_means and compute_clusters.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector)
        See Log.txt for expected output.
        """
        self.mean_vecs = []
        for i in range(0,self.k):
            self.mean_vecs.append((documents[i],norm_squared(documents[i])))

        for j in range(0,iters):
            self.compute_clusters(documents)
            self.compute_means()
            print self.len_of_clusters
            print self.error


    def compute_means(self):
        """ Compute the mean vectors for each cluster (storing the results in an
        instance variable)."""
        self.len_of_clusters = [len(x) for x in self.clusters_list]
        self.error = 0
        for num,each_cluster in enumerate(self.clusters_list):
            mean_vec = Counter()
            for (doc,distance) in each_cluster:
                mean_vec.update(doc)
                self.error += distance
            for every in mean_vec:
                mean_vec[every] = 1.* mean_vec[every]/float(self.len_of_clusters[num])
            self.mean_vecs[num] = (mean_vec,norm_squared(mean_vec))
        return

    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable). """
        self.clusters_list = []
        for j in range(0,self.k):
            self.clusters_list.append([])
        for each in documents:
            distance_list = []
            for i in range(0,self.k):
                mean = self.mean_vecs[i][0]
                mean_norm = self.mean_vecs[i][1]
                distance_list.append((i,self.distance(each,mean,mean_norm)))
            cluster = sorted(distance_list, key = lambda x: x[1])[0][0]
            error = 1. * sorted(distance_list, key = lambda x: x[1])[0][1]
            self.clusters_list[cluster].append((each,error))
        return

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        a = mean_norm
        b = norm_squared(doc)
        c = a + b - 2.0*dotproduct(doc,mean)
        return math.sqrt(c)


    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster, sorted by distance to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (which will be out of order from the original
        document).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        stringr = "Cluster "
        for num,each_cluster in enumerate(self.clusters_list):
            print "Cluster ", num
            list = [(doc,distance) for (doc,distance) in each_cluster if len(doc)>3]
            sorted_list = sorted(list,key=lambda x: x[1])
            for i in range(0,n):
                print " ".join(sorted_list[i][0].keys())
        return



def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    resultant_dict = defaultdict(lambda :0)
    final_list = []
    for each in docs:
        for every in each:
            resultant_dict[every] += 1
    terms_not_to_prune =  [x for (x,y) in resultant_dict.items() if y>=min_df]
    for eachtwo in docs:
        resultant_doc_dict = {}
        for everytwo in eachtwo:
            if everytwo in terms_not_to_prune:
                resultant_doc_dict[everytwo] = eachtwo[everytwo]
        if resultant_doc_dict:
            final_list.append(Counter(resultant_doc_dict))
    return final_list


def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with io.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles

def main():
    """ DO NOT MODIFY. """
    profiles = read_profiles('profiles.txt')
    print 'read', len(profiles), 'profiles.'
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
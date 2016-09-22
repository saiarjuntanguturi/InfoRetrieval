""" Assignment 2

You will modify Assignment 1 to support cosine similarity queries.

The documents are read from documents.txt.

The index will store tf-idf values using the formulae from class.

The search method will sort documents by the cosine similarity between the
query and the document (normalized only by the document length, not the query
length, as in the examples in class).

The search method also supports a use_champion parameter, which will use a
champion list (with threshold 10) to perform the search.

"""
from collections import defaultdict
import codecs
import math
import re
from run import recall
from run import precision
from run import f1
from run import MAP_dict
import run
from run import MAP
from run import average_prec


class Index(object):

    def __init__(self, filename=None,  identifier=None, champion_threshold=10):
        """ DO NOT MODIFY.
        Create a new index by parsing the given file containing documents,
        one per line. You should not modify this. """
        if filename and identifier:  # filename may be None for testing purposes.
            self.documents = self.read_lines(filename,identifier)
            stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
            self.doc_freqs = self.count_doc_frequencies(stemmed_docs)
            self.collection_freq = self.count_collection_frequencies(stemmed_docs)
            self.index = self.create_tfidf_index(stemmed_docs, self.doc_freqs)
            self.doc_lengths = self.compute_doc_lengths(self.index)
            self.champion_index = self.create_champion_index(self.index, champion_threshold)
            self.average_length = self.average_length(stemmed_docs)

    def compute_doc_lengths(self, index):
        """
        Return a dict mapping doc_id to length, computed as sqrt(sum(w_i**2)),
        where w_i is the tf-idf weight for each term in the document.

        E.g., in the sample index below, document 0 has two terms 'a' (with
        tf-idf weight 3) and 'b' (with tf-idf weight 4). It's length is
        therefore 5 = sqrt(9 + 16).

        >>> lengths = Index().compute_doc_lengths({'a': [[0, 3]], 'b': [[0, 4]]})
        >>> lengths[0]
        5.0
        >>> arjun = Index().compute_doc_lengths({'a': [[0,3],[1,2],[2,3]] , 'b': [[0,4],[1,3],[1,6],[2,4]]})
        >>> arjun[0]
        5.0
        >>> arjun[1]
        7.0
        >>> arjun[2]
        5.0
    """
        resultant_dict = defaultdict(lambda: [])
        for each in index:
            i = 0
            while i < len(index[each]):
                resultant_dict[index[each][i][0]].append(index[each][i][1])
                i += 1
        return {key:sum(map(lambda x: x**2, value)) **0.5 for key,value in resultant_dict.items()}






    def create_champion_index(self, index, threshold=10):
        """
        Create an index mapping each term to its champion list, defined as the
        documents with the K highest tf-idf values for that term (the
        threshold parameter determines K).

        In the example below, the champion list for term 'a' contains
        documents 1 and 2; the champion list for term 'b' contains documents 0
        and 1.

        >>> champs = Index().create_champion_index({'a': [[0, 10], [1, 20], [2,15]], 'b': [[0, 20], [1, 15], [2, 10]]}, 2)
        >>> champs['a']
        [[1, 20], [2, 15]]
        >>> champs['b']
        [[0, 20], [1, 15]]
        """
        resultant_dict = {}
        for each in index:
            resultant_dict[each]= sorted(index[each],key = lambda x: x[1],reverse=True)[:threshold]
        return resultant_dict

    def create_tfidf_index(self, docs, doc_freqs):
        """
        Create an index in which each postings list contains a list of
        [doc_id, tf-idf weight] pairs. For example:

        {'a': [[0, .5], [10, 0.2]],
         'b': [[5, .1]]}

        This entry means that the term 'a' appears in document 0 (with tf-idf
        weight .5) and in document 10 (with tf-idf weight 0.2). The term 'b'
        appears in document 5 (with tf-idf weight .1).

        Parameters:
        docs........list of lists, where each sublist contains the tokens for one document.
        doc_freqs...dict from term to document frequency (see count_doc_frequencies).

        Use math.log10 (log base 10).

        >>> index = Index().create_tfidf_index([['a', 'b', 'a'], ['a']], {'a': 2., 'b': 1., 'c': 1.})
        >>> sorted(index.keys())
        ['a', 'b']
        >>> index['a']
        [[0, 0.0], [1, 0.0]]
        >>> index['b']  # doctest:+ELLIPSIS
        [[0, 0.301...]]
        """
        resultant_dict = defaultdict(lambda:[])
        for doc_number,each in enumerate(docs):
            for doc in each:
                tf_value = 1.0 + math.log10(each.count(doc))
                idf_value = 1.0 * (math.log10(len(docs)/doc_freqs[doc]))
                tfidfval = tf_value * idf_value
                tf_idf_value_sublist = [doc_number,tfidfval]
                if tf_idf_value_sublist not in resultant_dict[doc]:
                    resultant_dict[doc].append(tf_idf_value_sublist)
        return resultant_dict

    """
        resultant_dict = defaultdict(lambda: [])
        for doc_number,each in enumerate(docs):
            for doc in each:
                tf_idf_value = [doc_number,(1+math.log10(each.count(doc)))*(1.*math.log10(len(docs) / doc_freqs[doc]))]
                if tf_idf_value not in resultant_dict[doc]:
                    resultant_dict[doc].append(tf_idf_value)
        return resultant_dict
    """


    def count_doc_frequencies(self, docs):
        """ Return a dict mapping terms to document frequency.
        />>> res = Index().count_doc_frequencies([['a', 'b', 'a'], ['a', 'b', 'c'], ['a']])
        />>> res['a']
        3
        />>> res['b']
        2
        />>> res['c']
        1
        """
        resultant_dict = defaultdict(lambda : [])
        for each_number,each in enumerate(docs):
            for everything in each:
                if each_number not in resultant_dict[everything]:
                    resultant_dict[everything].append(each_number)
        return {key: len(value) for key,value in resultant_dict.items()}


    def count_collection_frequencies(self,docs):
        resultant_dict = defaultdict(lambda: 0)
        for each in docs:
            for everything in each:
                resultant_dict[everything]+=1
        return resultant_dict

    def query_to_vector(self, query_terms):
        """ Convert a list of query terms into a dict mapping term to inverse document frequency.
	using log(N / df(term)), where N is number of documents and df(term) is the number of documents
        that term appears in.
        Parameters:
        query_terms....list of terms
        """
        resultant_dict = defaultdict(float)
        for each in query_terms:
            if each in self.doc_freqs:
                idf_value = math.log10(1.0*len(self.documents)/ self.doc_freqs[each])
                if idf_value != resultant_dict[each]:
                    resultant_dict[each] = idf_value
            else:
                resultant_dict[each]=0
        return resultant_dict

    def search_by_cosine(self, query_vector, index, doc_lengths):
        """
        Return a sorted list of doc_id, score pairs, where the score is the
        cosine similarity between the query_vector and the document. The
        document length should be used in the denominator, but not the query
        length (as discussed in class). You can use the built-in sorted method
        (rather than a priority queue) to sort the results.

        The parameters are:

        query_vector.....dict from term to weight from the query
        index............dict from term to list of doc_id, weight pairs
        doc_lengths......dict from doc_id to length (output of compute_doc_lengths)

        In the example below, the query is the term 'a' with weight
        1. Document 1 has cosine similarity of 2, while document 0 has
        similarity of 1.

        >>> Index().search_by_cosine({'a': 1}, {'a': [[0, 1], [1, 2]]}, {0: 1, 1: 1})
        [(1, 2), (0, 1)]
        """
        scores = defaultdict(lambda: 0)
        # For each search term
        for query_term, query_weight in query_vector.iteritems():
            # For each matching doc
            for doc_id, doc_weight in index[query_term]:
                scores[doc_id] += query_weight * doc_weight
        for doc_id in scores:
            scores[doc_id] /= doc_lengths[doc_id]
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]




    def search(self, query, use_champions=False):
        """ Return the document ids for documents matching the query. Assume that
        query is a single string, possible containing multiple words. Assume
        queries with multiple words are phrase queries. The steps are to:

        1. Tokenize the query (calling self.tokenize)
        2. Stem the query tokens (calling self.stem)
        3. Convert the query into an idf vector (calling self.query_to_vector)
        4. Compute cosine similarity between query vector and each document (calling search_by_cosine).

        Parameters:

        query...........raw query string, possibly containing multiple terms (though boolean operators do not need to be supported)
        use_champions...If True, Step 4 above will use only the champion index to perform the search.
        """
        token = self.tokenize(query)
        stem = self.stem(token)
        idf_vec = self.query_to_vector(stem)
        if use_champions:
            return self.search_by_cosine(idf_vec,self.champion_index,self.doc_lengths)
        else:
            return self.search_by_cosine(idf_vec,self.index,self.doc_lengths)


    def search_by_rsv(self,query):
        scores = defaultdict(lambda: 0)
        stemmed_query = self.stem(self.tokenize(query))
        stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
        number_of_docs = len(self.documents)
        for doc_number,each in enumerate(stemmed_docs):
            for everything in stemmed_query:
                if everything in each:
                    scores[doc_number] += 1.0 * math.log10(1.0* number_of_docs/self.doc_freqs[everything])
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]


    def search_by_bm25(self,var_k,var_b,query):
        scores = defaultdict(lambda: 0)
        stemmed_query = self.stem(self.tokenize(query))
        stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
        number_of_docs = len(self.documents)
        for doc_number,each in enumerate(stemmed_docs):
            for everything in stemmed_query:
                if everything in each:
                    rsv_val = 1.0 * math.log10(1.0* number_of_docs/self.doc_freqs[everything])
                    numerator_val = (var_k +1.0) * each.count(everything)
                    denom_val = (var_k * ((1.0 - var_b) + (var_b * len(each) / self.average_length))) + each.count(everything)
                    if rsv_val != 0 and denom_val!=0 and numerator_val!= 0:
                        scores[doc_number] += 1.0 * rsv_val * numerator_val / denom_val
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]


    def average_length(self,docs_list):
        length_of_doc_list = len(docs_list)
        sum = 0
        for each in docs_list:
            sum += len(each)
        return 1.0 * sum/length_of_doc_list

    def read_lines(self, filename,identifier):
        """ DO NOT MODIFY.
        Read a file to a list of strings. You should not need to modify
        this. """
        file = open(filename,'r')

        document_list = []
        resultant_line =""
        for line in file:
            if "*STOP" not in line:
                if identifier not in line:
                    resultant_line+= line
                else:
                    document_list.append(resultant_line)
                    resultant_line=""
            else:
                document_list.append(resultant_line)
                break
        document_list.pop(0)
        return document_list

    def tokenize(self, document):
        """ DO NOT MODIFY.
        Convert a string representing one document into a list of
        words. Retain hyphens and apostrophes inside words. Remove all other
        punctuation and convert to lowercase.

        >>> Index().tokenize("Hi there. What's going on? first-class")
        ['hi', 'there', "what's", 'going', 'on', 'first-class']
        """
        return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

    def stem(self, tokens):
        """ DO NOT MODIFY.
        Given a list of tokens, collapse 'did' and 'does' into the term 'do'.

        >>> Index().stem(['did', 'does', 'do', "doesn't", 'splendid'])
        ['do', 'do', 'do', "doesn't", 'splendid']
        """
        return [re.sub('^(did|does)$', 'do', t) for t in tokens]


def main():
    """ DO NOT MODIFY.
    Main method. Constructs an Index object and runs a sample query. """
    indexer = Index("TIME.ALL","*TEXT")
    query_list = Index("TIME.QUE","*FIND")
    cosine_resultant_dict = {}
    rsv_resultant_dict = {}
    bm25one_resultant_dict = {}
    bm25two_resultant_dict = {}
    bm25three_resultant_dict = {}
    bm25four_resultant_dict = {}
    for number,each in enumerate(query_list.documents):
        cosine_resultant_dict[number+1] = [x+1 for x,y in indexer.search(each)]
        rsv_resultant_dict[number+1] = [x+1 for x,y in indexer.search_by_rsv(each)]
        bm25one_resultant_dict[number+1] = [x+1 for x,y in indexer.search_by_bm25(1.0,0.5,each)]
        bm25two_resultant_dict[number+1] = [x+1 for x,y in indexer.search_by_bm25(1.0,1.0,each)]
        bm25three_resultant_dict[number+1] = [x+1 for x,y in indexer.search_by_bm25(2.0,0.5,each)]
        bm25four_resultant_dict[number+1] = [x+1 for x,y in indexer.search_by_bm25(2.0,1.0,each)]

    file = open('TIME.REL','r')
    dict_of_relevance = {}
    for line in file:
        if line[0] in "0123456789":
            dict_of_relevance[int(line.split()[0])]=map(int,line.split()[1:])
    print "Precision of Cosine = ", precision(cosine_resultant_dict,dict_of_relevance)
    print "Recall of Cosine = ", recall(cosine_resultant_dict,dict_of_relevance)
    print "F1 of Cosine = ", f1(cosine_resultant_dict,dict_of_relevance)
    print "MAP of Cosine = ", MAP_dict(cosine_resultant_dict,dict_of_relevance)

    print "Precision of RSV = ", precision(rsv_resultant_dict,dict_of_relevance)
    print "Recall of RSV = ", recall(rsv_resultant_dict,dict_of_relevance)
    print "F1 of RSV = ", f1(rsv_resultant_dict,dict_of_relevance)
    print "MAP of RSV = ", MAP_dict(rsv_resultant_dict,dict_of_relevance)

    print "Precision of BM25(1,.5) = ", precision(bm25one_resultant_dict,dict_of_relevance)
    print "Recall of BM25(1,.5) = ", recall(bm25one_resultant_dict,dict_of_relevance)
    print "F1 of BM25(1,.5) = ", f1(bm25one_resultant_dict,dict_of_relevance)
    print "MAP of BM25(1,.5) = ", MAP_dict(bm25one_resultant_dict,dict_of_relevance)

    print "Precision of BM25(1,1) = ", precision(bm25two_resultant_dict,dict_of_relevance)
    print "Recall of BM25(1,1) = ", recall(bm25two_resultant_dict,dict_of_relevance)
    print "F1 of BM25(1,1) = ", f1(bm25two_resultant_dict,dict_of_relevance)
    print "MAP of BM25(1,1) = ", MAP_dict(bm25two_resultant_dict,dict_of_relevance)

    print "Precision of BM25(2,.5) = ", precision(bm25three_resultant_dict,dict_of_relevance)
    print "Recall of BM25(2,.5) = ", recall(bm25three_resultant_dict,dict_of_relevance)
    print "F1 of BM25(2,.5) = ", f1(bm25three_resultant_dict,dict_of_relevance)
    print "MAP of BM25(2,.5) = ", MAP_dict(bm25three_resultant_dict,dict_of_relevance)

    print "Precision of BM25(2,1) = ", precision(bm25four_resultant_dict,dict_of_relevance)
    print "Recall of BM25(2,1) = ", recall(bm25four_resultant_dict,dict_of_relevance)
    print "F1 of BM25(2,1) = ", f1(bm25four_resultant_dict,dict_of_relevance)
    print "MAP of BM25(2,1) = ", MAP_dict(bm25four_resultant_dict,dict_of_relevance)

    """
    precision_vector = []
    recall_vector = []
    for i in range(1,84):
        precision_vector.append(run.prec_for_graph(rsv_resultant_dict[i],dict_of_relevance[i]))
        recall_vector.append(run.rec_for_graph(rsv_resultant_dict[i],dict_of_relevance[i]))


    print len(precision_vector)
    print len(recall_vector)
    average_prec_vector = []
    for number,each in enumerate(precision_vector):
        for i in range(0,len(precision_vector)):
            average_prec_vector[i] += each[i]

    average_recall_vector =[]
    for number2,each2 in enumerate(recall_vector):
        for j in range(0,len(average_recall_vector)):
            average_recall_vector[j] += each2[j]

    for every in average_prec_vector:
        every /= 8300

    for every2 in average_recall_vector:
        every2 /= 8300


    print average_recall_vector
    print average_prec_vector
    """



if __name__ == '__main__':
    main()



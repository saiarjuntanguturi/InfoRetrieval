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


class Index(object):

    def __init__(self, filename=None, champion_threshold=10):
        """ DO NOT MODIFY.
        Create a new index by parsing the given file containing documents,
        one per line. You should not modify this. """
        if filename:  # filename may be None for testing purposes.
            self.documents = self.read_lines(filename)
            stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
            self.doc_freqs = self.count_doc_frequencies(stemmed_docs)
            self.index = self.create_tfidf_index(stemmed_docs, self.doc_freqs)
            self.doc_lengths = self.compute_doc_lengths(self.index)
            self.champion_index = self.create_champion_index(self.index, champion_threshold)

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
        """

        resultant_dict = defaultdict(lambda: [])
        for each in index:
            i = 0
            while i < len(index[each]):
                resultant_dict[index[each][i][0]].append(index[each][i][1])
                i += 1
        return {key: sum(map(lambda x: x**2, value))**0.5 for key, value in resultant_dict.items()}




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
        resultant_dict = defaultdict(lambda: [])
        for doc_number,each in enumerate(docs):
            for doc in each:
                tf_idf_value = [doc_number,(1+math.log10(each.count(doc)))*(math.log10(len(docs) / doc_freqs[doc]))]
                if tf_idf_value not in resultant_dict[doc]:
                    resultant_dict[doc].append(tf_idf_value)
        return resultant_dict


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

    def query_to_vector(self, query_terms):
        """ Convert a list of query terms into a dict mapping term to inverse document frequency.
	using log(N / df(term)), where N is number of documents and df(term) is the number of documents
        that term appears in.
        Parameters:
        query_terms....list of terms
        """
        resultant_dict = defaultdict(float)
        for each in query_terms:
            idf_value = math.log10(float(len(query_terms))/ query_terms.count(each))
            if idf_value != resultant_dict[each]:
                resultant_dict[each] = idf_value
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

        resultant_list = []
        for each in query_vector:
            i = 0
            while i<len(index[each]):
                cosine_sim = (index[each][i][1] * query_vector[each])/(doc_lengths[index[each][i][0]])
                resultant_list.append((index[each][i][0],cosine_sim))
                i+=1
        return sorted(resultant_list, key = lambda (k,v): v, reverse = True)


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




    def read_lines(self, filename):
        """ DO NOT MODIFY.
        Read a file to a list of strings. You should not need to modify
        this. """
        return [l.strip() for l in codecs.open(filename, 'r', 'utf-8').readlines()]

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
    indexer = Index('documents.txt')
    for query in ['pop love song', 'chinese american', 'city']:
        print '\n\nQUERY=', query
        print '\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query)[:10]])
        print '\n\nQUERY=', query, 'Using Champion List'
        print '\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query, True)[:10]])

if __name__ == '__main__':
    main()
Edit this file and push to your private repository to provide answers to the following questions.

1. In `searcher.py`, why do we keep an inverted index instead of simply a list
of document vectors (e.g., dicts)? What is the difference in time and space
complexity between the two approaches?   


    **An index is much smarter that a vector because indexes have O(1) (constant) search time, as compared to O(n) which is linear search time
    for a list of document vectors. In addition, document vectors repeat words many times, especially the most frequent words (articles, personal pronouns)
    . However, inverted indexes use each word as a key, and relate it to a document ID. I'm not familiar with space complexity, but 
     document vectors clearly take more space, as compared to inverted indexes. It's better to have an inverted index with word keys to doc_id values.**
   
2. Consider the query `chinese` with and without using champion lists.  Why is
the top result without champion lists absent from the list that uses champion
lists? How can you alter the algorithm to fix this?   


    **
     Champions List are essentially precomputed lists for each term t in a dictionary. Each list contains r documents which have the highest 
     weights for the term t. The top result for the query 'chinese' with champions lists just looks at the top r documents in terms of tf-idf
     values. However, the query 'chinese' without champions list uses cosine similarity, which also looks at the length of the document, and 
     the similarity between the entire query and each entire document. The top result for 'chinese' without champions lists probably was a small
     document that also had many occurrences of the word chinese. TThe top result for 'chinese' with champions lists, probably just looked at the 
     tf and idf weight which isn't as indicative of the similarity between the two documents. In my opinion, without champions lists is better,
     but with champions list runs faster, and has less time complexity, and returns the top r documents which would are all positives. We could alter 
     the champion list algorithm to take size of each individual document into account, and that would be a little faster then computing the
     cosine similarity.
     **

3. Describe in detail the data structures you would use to implement the
Cluster Pruning approach, as well as how you would use them at query time.   


    **In Cluster Pruning, given N documents, we compute sqrt(N) documents at random from the collection of N documents, and use those documents as leaders. 
    Then for each document that is not a leader, we compute the nearest leader. Then these documents become the follower for that leader.
     After this, when we receive a query, we compute the cosine similarity between the query and the leaders. For the leader with the highest cosine
     similarity, we also compute cosine similarity with that leader's followers, and return the document with the highest cosine similarity.
     As you can see, order is very important for Cluster Pruning. Therefore I would use a Linked-HashMap. HashMap would give us constant search time,
     and LinkedList would give us the order required to implement Cluster Pruning. I would make a LinkedList of the documents with followers
     then leaders then followers then followers. Then I would be able to search in constant time at query time, and compute cosine similarity.**
Edit this file in your private repository to provide answers to the following questions (from MRS).

1. Extend the postings merge algorithm to arbitrary Boolean query formulas. What is
its time complexity? For instance, consider:

  `(Brutus OR Caesar) AND NOT (Antony OR Cleopatra)`

  Can we always merge in linear time? Linear in what? Can we do better than this?

  **For AND NOT, the algorithm could be extended like this(using the syntax in the MRS book): 
  a AND NOT b would result in:  
  INTERSECTNOT (a,b)  
  ANSWER <- []  
  WHILE a != NIL:  
  DO IF docID(a) == docID(b)  
        a <-  next(a)  
        b <-  next(b)  
  ELSE IF docID(a) < docID(b)  
        ADD(ANSWER,docID(a))  
        a <- next(a)  
  ELSE  
        b <- next(b)  
  RETURN ANSWER 
   
  This extension of the merge algorithm would result in a time complexity of O(x + y) where x is the length(a) and y is the length(b).
  However, it should be noted that this is a conservative estimate. Because of the while loop, the algorithm will definitely traverse
  through the entire a list, but if the b list is bigger than a list, then it will not completely traverse through the b list.  
  
  The OR boolean requires that we take the union of the two lists (a.k.a combine them, and delete duplicates). The OR algorithm would take 
  O(x+y) best case where x and y have to be the lengths of the two lists merged via OR. Therefore the algorithm will completely traverse both lists. 
  The OR algorithm would look like this:  
  INTERSECTOR (a,b)  
  ANSWER <- []  
  WHILE a != NIL and b != nil:  
  DO IF docID(a) == docID(b)  
        ADD(ANSWER, docID(a))  
  ELSE IF docID(a) < docID(b)  
        ADD(ANSWER,docID(a))  
        a <- next(a)  
  ELSE  
        ADD(ANSWER,docID(b))
        b <- next(b)  
  RETURN ANSWER  
  
  We can always merge in linear time, where O(n) is the number of documents in the collection. In fact, we merge in O(n1 + n2 + ... + n(x)) where
  n(x) is the last term in the complex boolean query. Therefore we actually save a constant amount of time. This constant will be very large when the
  number of documents being merged is very high, so we will actually be saving a great deal of time. Both algorithms require that the document lists are
  sorted before the algorithm is used.
  **

2. If the query is:

  `friends AND romans AND (NOT countrymen)`

  How could we use the frequency of countrymen in evaluating the best query evaluation order? In particular, propose a way of handling negation in determining the order of query processing.
  
  **The NOT could be handled in two ways. We could run through all the documents, and return only those that do not contain countrymen, and then AND
  the resulting document list with friends AND romans. The frequency of countrymen will determine how large that resulting list is. Since we have to traverse through 
  the entire postings list, an algorithm for NOT would cost O(n) where n is the number of documents.
  However, we could beat linear merge time by processing AND NOT as one function. In order to handle negation, we will evaluate the AND NOT statements at the end. Each AND 
  NOT statement will result in O(x+y) where x is length of the first list, and y is length of the second list. However, as discussed in the previous short answer, we do not 
  need to traverse through the entirety of the second list y. If the first list x is smaller than the second list, than the function will terminate as soon as the first list has
  been traversed through. The second list here would be a list of all the documents. My way of handling negation would work because:  
  1. Using AND on two lists gives us a resulting list that is either lesser than or equal to the length of the smaller of the two lists we used it on.  
  2. Using that resulting list in an AND NOT as a first list would be very useful because it the algorithm for AND NOT only traverses the whole of the first list. 
    Ergo, negation can be handled by evaluating AND NOT as one expression instead of separate ones, and by evaluating all the AND NOT after all the AND functions.**
  
3. For a conjunctive query, is processing postings lists in order of size guaranteed to be
optimal? Explain why it is, or give an example where it isn’t.

  **For a conjunctive query, processing postings lists in order of size will be optimal most of the time. However, there are certain situations where 
  processing postings lists by size will not be optimal. For example, given three postings a = [1], b = [1,2,3], c = [3,4,5,6], and then ordering by size
  we would obtain the postings list [a,b,c]. Using this list, first we would intersect a  and b and obtain [1]. Then we would intersect [1] with c, and obtain
  the empty list []. However, if we had intersected a and c first, we would obtain an empty list [], and the next intersect with b would not even be required.
   Therefore, processing postings lists in order of size is not always guaranteed to be optimal.**

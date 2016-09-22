"""
A rudimentary web interface to the search engine, using Flask. You'll have to
install flask (if you have pip installed, you can do `pip install flask`; for
Windows, see
http://flask.pocoo.org/docs/installation/#pip-and-distribute-on-windows).

Run with `python run.py`. If successful, you should see a message like:
Running on http://127.0.0.1:5000/ . You can then view the page in your web
browser at the specified URL.

You should not need to modify this file.
"""



def precision(dict1,relevance_dict):
    sum = 0.0
    for i in range(1,84):
        sum += 100.0 * len([number for number in dict1[i] if number in relevance_dict[i]])/len(dict1[i])
    return sum/83.0

def recall(dict1,relevance_dict):
    sum =0.0
    for i in range(1,84):
        sum += 100.0 * len([number for number in dict1[i] if number in relevance_dict[i]])/len(relevance_dict[i])
    return sum/83.0

def f1(dict1,relevance_dict):
    sum =0.0
    for i in range(1,84):
        precision = 100.0 * len([number for number in dict1[i] if number in relevance_dict[i]])/len(dict1[i])
        recall = 100.0 * len([number for number in dict1[i] if number in relevance_dict[i]])/len(relevance_dict[i])
        if precision+recall !=0:
            sum += (2.0 * precision * recall)/(precision + recall)
    return sum/83.0

def average_prec(doc_list,relevance_doc_list):
    return 100.0* len([number for number in doc_list if number in relevance_doc_list])/len(doc_list)

def average_rec(doc_list,relevance_doc_list):
    return 100.0* len([number for number in doc_list if number in relevance_doc_list])/len(relevance_doc_list)

def MAP(doc_list,relevance_doc_list):
    resultant_list = []
    for i in range(1,len(doc_list)+1):
        resultant_list.append(average_prec(doc_list[:i],relevance_doc_list))
    alist = zip(doc_list,resultant_list)
    final_list = []
    for each in doc_list:
        if each in relevance_doc_list:
            final_list.append(each)
    return sum([y for x,y in alist if x in final_list])/len(doc_list)

def prec_for_graph(doc_list,relevance_doc_list):
    resultant_list = []
    for i in range(1,len(doc_list)+1):
        resultant_list.append(average_prec(doc_list[:i],relevance_doc_list))
    return resultant_list

def rec_for_graph(doc_list,relevance_doc_list):
    resultant_list = []
    for i in range(1,len(doc_list)+1):
        resultant_list.append(average_rec(doc_list[:i],relevance_doc_list))
    return resultant_list

def MAP_dict(dict1,relevance_dict):
    sum = 0.0
    for i in range(1,84):
        sum += MAP(dict1[i],relevance_dict[i])
    return sum/83.0
import time
import pickle
import re
from nltk.stem import *
import heapq
"""
inverted1_jump_map = {}
with open("inverted1_jump_map.pickle", "rb") as f:
    inverted1_jump_map = pickle.load(f)

with open('serialized_index1.txt', 'r') as file:
    #search for time
    time_pos = inverted1_jump_map['time']
    file.seek(time_pos)
    line = file.readline()
    print(line[0:50])

    #retrieve all postings
"""

serialized_index1 = open('serialized_index1.txt', 'r')
with open("inverted1_jump_map.pickle", "rb") as f:
    inverted1_jump_map = pickle.load(f)
with open("id_url_map1.pickle", "rb") as f:
    id_url_map1 = pickle.load(f)


serialized_index2 = open('serialized_index2.txt', 'r')
with open("inverted2_jump_map.pickle", "rb") as f:
    inverted2_jump_map = pickle.load(f)
with open("id_url_map2.pickle", "rb") as f:
    id_url_map2 = pickle.load(f)


serialized_index3 = open('serialized_index3.txt', 'r')
with open("inverted3_jump_map.pickle", "rb") as f:
    inverted3_jump_map = pickle.load(f)
with open("id_url_map3.pickle", "rb") as f:
    id_url_map3 = pickle.load(f)

files = [serialized_index1, serialized_index2, serialized_index3]

def search(token):
    found_urls = []

    results = []
    all_urls = set()
    file_count = 1
    for file in files:
        if file_count == 1:
            file_pos = inverted1_jump_map[token]
            serialized_index1.seek(file_pos)
            token_line = serialized_index1.readline()
            #get first 10 postings from this list if possible
            posting_ids = []
            #using regular expressions to parse ID's from file
            integer_pattern = re.compile(r'\d+')
            ids = integer_pattern.findall(token_line)
            ids = [float(x) for x in ids]
            #print(ids[0:10])

            pairs = token_line.split(';')
            
            for p in pairs:
                try:
                    docID, tf_idf = p.split(',')
                    #results.append(int(docID),float(tf_idf))

                    heapq.heappush(results, (-1*float(tf_idf), id_url_map1[int(docID)]))
                    all_urls.add(id_url_map1[int(docID)])
                except ValueError:
                    continue

            #print(id_url_map1[ids[0]])
            #found_urls = [id_url_map1[x] for x in ids]
            file_count += 1

        if file_count == 2:
            file_pos = inverted2_jump_map[token]
            serialized_index2.seek(file_pos)
            token_line = serialized_index2.readline()
            #get first 10 postings from this list if possible
            posting_ids = []
            #using regular expressions to parse ID's from file
            integer_pattern = re.compile(r'\d+')
            ids = integer_pattern.findall(token_line)
            ids = [float(x) for x in ids]
            #print(ids[0:10])

            pairs = token_line.split(';')
            
    

            for p in pairs:
                try:
                    docID, tf_idf = p.split(',')
                    
                    #results.append(int(docID),float(tf_idf))
                    heapq.heappush(results, (-1*float(tf_idf), id_url_map2[int(docID)]))
                    all_urls.add(id_url_map2[int(docID)])
                except ValueError:
                    continue

            
            file_count += 1
        

        if file_count == 3:
            file_pos = inverted3_jump_map[token]
            serialized_index3.seek(file_pos)
            token_line = serialized_index3.readline()
            #get first 10 postings from this list if possible
            posting_ids = []
            #using regular expressions to parse ID's from file
            integer_pattern = re.compile(r'\d+')
            ids = integer_pattern.findall(token_line)
            ids = [float(x) for x in ids]
            #print(ids[0:10])

            pairs = token_line.split(';')
            
        
            for p in pairs:
                try:
                    docID, tf_idf = p.split(',')

                    #results.append(int(docID),float(tf_idf))
                    heapq.heappush(results, (-1*float(tf_idf), id_url_map3[int(docID)]))
                    all_urls.add(id_url_map3[int(docID)])
                except ValueError:
                    continue

            
            file_count += 1
    
    return results, all_urls



stemmer = PorterStemmer()
stemmed_token1 = stemmer.stem("machine")
stemmed_token2 = stemmer.stem("learning")
stemmed_token3 = stemmer.stem("computer")

"""
start_time = time.time()

res1, urls1 = search(stemmed_token1)
res2, urls2 = search(stemmed_token2)
res3, urls3 = search(stemmed_token3)


res2 = [x for x in res2 if x[1] in urls1]
urls1 = urls1 & urls2

print(len(res3))
res3 = [x for x in res3 if x[1] in urls1]
print(len(res3))

#pop off first 10 urls of heap that have max tf-idf scores
counter = 10
final_results = []
while res3 and counter > 0:
    _, url = heapq.heappop(res3)
    final_results.append(url)
    counter -= 1

print(final_results)

end_time = time.time()
print("time ellapsed: "+str(end_time - start_time))

"""


while True:
    query = input("Please type a query in and press enter. Or enter q to quit.\n")
    if query == 'q':
        break
    
    print("You queried for: "+query)

    start_time = time.time()
    results = set()
    components = query.split(" ")
    #apply stemmer to each word
    components = [stemmer.stem(x) for x in components]
    print(components)

    final_results = []
    final_urls = []
    first_word = True
    for word in components:
        results, urls = search(word)
        
        if first_word:
            final_results = results
            final_urls = urls
            first_word = False

        results = [x for x in results if x[1] in final_urls]
        final_results = results
        final_urls = final_urls & urls
        
    
    counter = 10
    top_results = []
    while final_results and counter > 0:
        _, url = heapq.heappop(final_results)
        top_results.append(url)
        counter -= 1
    

    print(top_results)

    finish_time = time.time()
    elapsed = finish_time - start_time
    print(f"Took {elapsed} seconds")
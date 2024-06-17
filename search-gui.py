import time
import pickle
import re
from nltk.stem import *
import heapq
import streamlit as st

st.title("Search Engine")


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
                except (ValueError, KeyError):
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
                except (ValueError, KeyError):
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
                except (ValueError, KeyError):
                    continue

            
            file_count += 1
    
    return results, all_urls


stemmer = PorterStemmer()

query = st.text_input('Enter your query')
if query == 'q':
    exit()

if st.button('Search'):
    #st.write(query)
    start_time = time.time()
    results = set()
    components = query.split(" ")
    #apply stemmer to each word
    components = [stemmer.stem(x) for x in components]

    #checking for stopword significance
    small_components = [x for x in components if len(x) < 3]
    small_components_ratio = len(small_components)/len(components)
    if small_components_ratio < 0.7:
        components = [x for x in components if len(x) >  2]
    #print(components)

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
    
    for url in top_results:
        #print(url)
        st.write(url)

    st.write(f"total result count: {len(final_results)}")

    finish_time = time.time()
    elapsed = finish_time - start_time
    elapsed_ms = elapsed * 1000
    st.write(f"Took {elapsed_ms} ms")


import os
import json
from bs4 import BeautifulSoup
from nltk.stem import *
import pickle
import time
import hashlib
import math

start_time = time.time()

content_set = set()
exact_matches = 0

def calc_hash(text):
    hash_obj = hashlib.sha256(html_content.encode())
    hash_hex = hash_obj.hexdigest()
    return hash_hex

def is_duplicate(text):
    hash = calc_hash(text)

    if hash in content_set:
        global exact_matches
        exact_matches += 1
        return True
    else:
        content_set.add(hash)
        return False

class Posting:

    def __init__(self, id):
        self.docID = id
        #count = term frequency
        self.count = 1
        self.tf_idf = 0
        

    def add_count(self):
        self.count += 1
    
    def set_tfidf(self, val):
        self.tf_idf = val
        

def serialize_posting(post):
    #given post, serialize into text to add into 
    str = f'{post.docID};{post.tf_idf}'

#dirs = ['ANALYST/www_cs_uci_edu', 'ANALYST/www_informatics_uci_edu','ANALYST/www-db_ics_uci_edu']

dir = 'DEV'
#JSON: {url:str, content:str, encoding:str}
dirs = os.listdir(dir)

#dirs.remove(".DS_Store")


dirs = dirs[31:50]

inverted = {}
id_counter = 0
id_url_map = {}

no_html_count = 0

stemmer = PorterStemmer()

dump_counter = 1


dirs = ["DEV/"+x for x in dirs]
try:
    for directory in dirs:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                filepath = os.path.join(directory, filename)

                with open(filepath, 'r') as file:
                    json_data = json.load(file)
                    
                    try:
                        #if json_data[""]
                        id_counter += 1
                        id_url_map[id_counter] = json_data["url"]

                        if id_counter % 5000 == 0:
                            print(id_counter)
                        
                        #DUMP TO FILE EVERY 17,000 files
                        
                        if id_counter % 17000 == 0:
                            dump_counter += 1

                            #for each term, and each posting list in term set tf_idf
                            corpus_len = len(id_url_map)

                            for term in inverted:
                                idf = math.log10(corpus_len / len(inverted[term]))

                                for p in inverted[term]:
                                    p.set_tfidf( p.count * idf)



                            print(id_counter)
                            with open(f'inverted_index{dump_counter}.pickle', "wb") as f:
                                pickle.dump(inverted, f)
                                inverted = {}

                            with open(f'id_url_map{dump_counter}.pickle', "wb") as fi:
                                pickle.dump(id_url_map, fi)
                                id_url_map = {}
                        
                        #not going to bother with non html for now
                        
                        #get all tokens from html using bs4, then parse with porter stemmer

                        #read document into string
                        html_content = json_data["content"]

                        soup = BeautifulSoup(html_content, 'html.parser')

                        #check for exact match
                        full_text = soup.get_text()
                        #text_hash = calc_hash(full_text)
                        #if is_duplicate(text_hash):
                        #    continue

                        full_text = (
                            full_text.replace("\n", " ").replace(u'\xa0', u' ').replace("\r", " ")
                            .replace("("," ").replace(")"," ").replace('“', " ").replace(",", " ")
                            .replace(".", " ").replace(";", " ").replace("”"," ").replace(":", " ")
                            .replace("/", " ").replace("/", " ").replace("\t", " ").replace(u'\u200b', u' ')
                            .replace("~", " ").replace("‘", " ").replace("[", " ").replace("]", " ")
                            .replace(u'\u202a', u' ').replace(u'\ufeff', u' ').replace(u'\u200e', u' ')
                            .replace(u'\u3000', u' ').replace("{"," ").replace("}"," ").replace(u'\u200a', u' ')
                            .replace("-", " ").replace("…"," ").replace("?", " ").replace("=", " ")
                        
                        )
                        text_arr = full_text.split(" ")
                        text_arr = [x.lower() for x in text_arr if len(x) > 0]

                        #print(text_arr)

                        #Parse document into tokens
                        for token in text_arr:
                            #get stem of token
                            stemmed_token = stemmer.stem(token)


                            if stemmed_token not in inverted:
                                p = Posting(id_counter)
                                inverted[stemmed_token] = [p]
                            else:
                                #check if posting exists for this document, if not create one
                                in_flag = False
                                postings = inverted[stemmed_token]
                                for p in postings:
                                    if p.docID == id_counter:
                                        in_flag = True

                                if in_flag:
                                    #if this docID already has a posting, then it should be at the end of the list, inc
                                    inverted[stemmed_token][-1].add_count()
                                else:
                                    p = Posting(id_counter)
                                    inverted[stemmed_token].append(p)

                
                        #print(json_data)
                    except KeyError:
                        print("either url or content field does not exist, skipping this document!")
except NotADirectoryError:
    print("not a directory!")
#print(id_counter)


#print(sorted(inverted.keys()))
print("Number of unique keys: "+str(len(inverted.keys())))
print("number of documents: "+(str(id_counter)))


"""
with open("inverted_index.pickle", "wb") as f:
    pickle.dump(inverted, f)

with open("id_url_map.pickle", "wb") as fi:
    pickle.dump(id_url_map, fi)

"""

end_time = time.time()

elapsed_time = end_time - start_time

print("Elapsed time:", elapsed_time, "seconds")

print("NO HTML COUNT: " + str(no_html_count))

print("exact duplicate matches: " + str(exact_matches))




#for each term, and each posting list in term set tf_idf
corpus_len = len(id_url_map)

for term in inverted:
    idf = math.log10(corpus_len / len(inverted[term]))

    for p in inverted[term]:
        p.set_tfidf( p.count * idf)



print(id_counter)
with open(f'inverted_index3.pickle', "wb") as f:
    pickle.dump(inverted, f)
    inverted = {}

with open(f'id_url_map3.pickle', "wb") as fi:
    pickle.dump(id_url_map, fi)
    id_url_map = {}
import pickle

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
    post_str = f'{post.docID};{post.tf_idf}'
    return post_str

inverted = {}
id_url_map = {}
inverted1_jump_map = {}

#load in inverted
with open("inverted_index3.pickle", "rb") as f:
    inverted = pickle.load(f)


with open("id_url_map3.pickle", "rb") as f:
    id_url_map = pickle.load(f)


with open('serialized_index3.txt', 'w') as file:
    for term in inverted:
        postings = inverted[term]

        #get offset
        curr_offset = file.tell()
        
        inverted1_jump_map[term] = curr_offset


        file.write(f'{term}:')

        sorted_postings = sorted(postings,key=lambda posting: posting.tf_idf, reverse=True)
        for p in sorted_postings:
            file.write(f'{p.docID},{p.tf_idf};')

        file.write('\n')

with open(f'inverted3_jump_map.pickle', "wb") as f:
    pickle.dump(inverted1_jump_map, f)
    
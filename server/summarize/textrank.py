import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk.tokenize import sent_tokenize
import numpy as np
import networkx as nx
import re

def clean_text(text):
    sentences =[] # tạo một list rỗng
    sentences = sent_tokenize(text) # tách câu
    for sentence in sentences: # duyệt từng câu trong text
        re.sub(r'[^a-zA-Z0-9]','',sentence) # loại bỏ các ký tự đặc biệt
        re.sub(r'\s+',' ',sentence) # loại bỏ các khoảng trắng thừa

    return sentences # trả về list các câu

def sentence_similarity(sent1,sent2,stopwords=None): # tính độ tương tự giữa 2 câu
    if stopwords is None: # nếu không có stopwords
        stopwords = [] # tạo một list stopword rỗng
    
    sent1 = [w.lower() for w in sent1] # chuyển câu thứ nhất về chữ thường
    sent2 = [w.lower() for w in sent2] # chuyển câu thứ hai về chữ thường
    
    all_words = list(set(sent1 + sent2)) # tạo một list chứa tất cả các từ trong 2 câu
    
    vector1 = [0] * len(all_words) # tạo một list vector1 có độ dài bằng với số từ trong all_words
    vector2 = [0] * len(all_words) # tạo một list vector2 có độ dài bằng với số từ trong all_words
    
    #build the vector for the first sentence
    for w in sent1: # duyệt từng từ trong câu thứ nhất
        if not w in stopwords: # nếu từ đó không nằm trong stopwords
            vector1[all_words.index(w)]+=1 # tăng giá trị của từ đó trong vector1 lên 1
    
    #build the vector for the second sentence
    for w in sent2: # duyệt từng từ trong câu thứ hai
        if not w in stopwords: # nếu từ đó không nằm trong stopwords
            vector2[all_words.index(w)]+=1 # tăng giá trị của từ đó trong vector2 lên 1
            
    return 1-cosine_distance(vector1,vector2) # trả về độ tương tự giữa 2 câu

def build_similarity_matrix(sentences,stop_words): # tạo ma trận độ tương tự
    #create an empty similarity matrix 
    similarity_matrix = np.zeros((len(sentences),len(sentences))) # tạo một ma trận 0 có kích thước bằng với số câu trong text
    
    for idx1 in range(len(sentences)): # duyệt từng câu trong text
        for idx2 in range(len(sentences)): # duyệt từng câu trong text
            if idx1!=idx2: # nếu 2 câu không trùng nhau
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1],sentences[idx2],stop_words) # tính độ tương tự giữa 2 câu và gán vào ma trận
                
    return similarity_matrix # trả về ma trận độ tương tự

def generate_summary(text,top_n):
    
    stop_words = stopwords.words('english') # tạo một list stopwords
    summarize_text = [] # tạo một list rỗng
    
    sentences = clean_text(text) # tách câu
    
    sentence_similarity_matrix = build_similarity_matrix(sentences,stop_words) # tạo ma trận độ tương tự
    
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix) # tạo đồ thị từ ma trận độ tương tự
    scores = nx.pagerank(sentence_similarity_graph) # tính pagerank
    
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)),reverse=True) # sắp xếp các câu theo thứ tự giảm dần của rank
     
    for i in range(top_n): # duyệt từng câu trong top_n câu có hạng cao nhất
        summarize_text.append(ranked_sentences[i][1]) # thêm câu đó vào list summarize_text
    
    return " ".join(summarize_text) # trả về kết quả
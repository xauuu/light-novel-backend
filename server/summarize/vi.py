import nltk
from gensim.models import KeyedVectors 
from pyvi import ViTokenizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
import re

w2v = KeyedVectors.load_word2vec_format("D:\Python\Light Novel\server\summarize\\vi.vec")
vocab = w2v.key_to_index

def summarize(content):
    # Tiền xử lý
    contents_parsed = content.lower() #Biến đổi hết thành chữ thường
    contents_parsed = re.sub(r'\[[0-9]*\]', ' ', contents_parsed) # loại bỏ các số trong ngoặc vuông
    contents_parsed = re.sub(r'\s+', ' ', contents_parsed) # loại bỏ khoảng trắng thừa
    contents_parsed = re.sub(r'<[^>]*>', ' ', contents_parsed) # loại bỏ các thẻ HTML
    contents_parsed = re.sub(r'\s+', ' ', contents_parsed) # loại bỏ khoảng trắng thừa
    # contents_parsed = contents_parsed.replace('\n', '. ') #Đổi các ký tự xuống dòng thành chấm câu
    # contents_parsed = contents_parsed.strip() #Loại bỏ đi các khoảng trắng thừa
    # Tách câu
    sentences = nltk.sent_tokenize(contents_parsed)

    #Chuyển các câu sang vector
    X = []
    for sentence in sentences:
        # Tách từ tiếng việt
        sentence_tokenized = ViTokenizer.tokenize(sentence)
        words = sentence_tokenized.split(" ")
        sentence_vec = np.zeros((100))
        for word in words:
            if word in vocab:
                sentence_vec+=w2v[word]
        X.append(sentence_vec)

    # Phân cụm
    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans = kmeans.fit(X)

    avg = []
    for j in range(n_clusters):
        idx = np.where(kmeans.labels_ == j)[0]
        avg.append(np.mean(idx))
    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
    ordering = sorted(range(n_clusters), key=lambda k: avg[k])
    summary = ' '.join([sentences[closest[idx]] for idx in ordering])
    return summary
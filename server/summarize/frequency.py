import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import re
import heapq

def summarize(text, top_n):
    article_text = re.sub(r'\[[0-9]*\]', ' ', text) # loại bỏ các số trong ngoặc vuông
    article_text = re.sub(r'\s+', ' ', article_text) # loại bỏ khoảng trắng thừa
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text ) # loại bỏ các ký tự đặc biệt
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text) # loại bỏ khoảng trắng thừa
    
    sentence_list = sent_tokenize(article_text) # tách câu
    stopwords = stopwords.words('english') # tạo stopwords

    word_frequencies = {} # tạo dictionary chứa các từ và tần suất xuất hiện
    for word in nltk.word_tokenize(formatted_article_text): # duyệt qua các từ trong văn bản
        if word not in stopwords: # nếu từ đó không nằm trong stopwords
            if word not in word_frequencies.keys(): # nếu từ đó chưa có trong dictionary
                word_frequencies[word] = 1 # thêm từ đó vào dictionary với tần suất là 1
            else: # nếu từ đó đã có trong dictionary
                word_frequencies[word] += 1 # tăng tần suất lên 1

    maximum_frequncy = max(word_frequencies.values()) # tìm tần suất xuất hiện nhiều nhất

    for word in word_frequencies.keys(): # duyệt qua các từ trong dictionary
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy) # tính toán tần suất xuất hiện của từ đó
    
    sentence_scores = {} # tạo dictionary chứa các câu và điểm tương ứng
    for sent in sentence_list: # duyệt qua các câu trong văn bản
        for word in nltk.word_tokenize(sent.lower()): # duyệt qua các từ trong câu
            if word in word_frequencies.keys(): # nếu từ đó có trong dictionary
                if len(sent.split(' ')) < 30: # nếu độ dài câu nhỏ hơn 30 từ
                    if sent not in sentence_scores.keys(): # nếu câu đó chưa có trong dictionary
                        sentence_scores[sent] = word_frequencies[word] # thêm câu đó vào dictionary với điểm tương ứng
                    else: # nếu câu đó đã có trong dictionary
                        sentence_scores[sent] += word_frequencies[word] # cộng điểm tương ứng
    
    summary_sentences = heapq.nlargest(top_n, sentence_scores, key=sentence_scores.get) # lấy top_n câu có điểm cao nhất
    return ' '.join(summary_sentences) # trả về kết quả
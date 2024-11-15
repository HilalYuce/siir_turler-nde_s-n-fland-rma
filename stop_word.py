import pandas as pd

stopwords = set([
    "ve", "bu", "şu", "o", "bir", "ancak", "fakat", "çünkü", "ki", "de", "da", 
    "ile", "mi", "mı", "mu", "mü", "sen", "ben", "biz", "siz", "onlar", "ya", 
    "ne", "her", "birçok", "çok", "az", "biraz", "bile", "hem", "gibi", "ama", 
    "eğer", "ise", "hala", "sadece", "ya", "yine", "için", "kadar", "ile", 
    "dolayı", "dolayısıyla", "aslında", "başka", "herhangi", "bazı", "bazısı"
])

file_path = 'category_zaman.csv'
data = pd.read_csv(file_path)

def remove_stopwords(sentence):
    words = sentence.split()
    meaningful_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(meaningful_words)

data['poem_cleaned'] = data['poem'].apply(lambda x: remove_stopwords(x) if pd.notnull(x) else x)

data[['title', 'poem_cleaned']].to_csv('cleaned_zaman.csv', index=False, encoding='utf-8-sig')

print("Stopword temizleme işlemi tamamlandı. Sonuç 'cleaned_poems.csv' dosyasına kaydedildi.")


# Türkçe Şiir İşleme Projesi

Bu proje, Türkçe şiir metinlerinin web'den çekilmesi, Zemberek kütüphanesi ile morfolojik analiz yapılması ve stopword'lerin temizlenmesi gibi işlemleri içermektedir. Kodlar, şiir verilerini anlamlı bir şekilde düzenlemeyi ve analiz etmeyi amaçlar.
 Verilerin google drive linki:
 - https://drive.google.com/drive/folders/1FWjnqdeP94AbzqF9MgYEJ1kanGnnEj4H?usp=sharing


## Proje İçeriği

### 1. Şiir Toplama (`collect_poems.py`)
- **Amaç**: Web scraping ile şiir verilerinin belirli kategorilerden toplanması ve CSV formatında kaydedilmesi.
- **Kullanılan Teknolojiler**:
  - `Selenium` ve `BeautifulSoup`: Şiir sayfalarını analiz etmek ve verileri çekmek için.
  - `ThreadPoolExecutor`: Paralel işleme ile veri çekme işlemini hızlandırmak için.

### 2. Zemberek ile İşleme (`zemberek_processing.py`)
- **Amaç**: Zemberek kütüphanesi kullanılarak şiirlerin morfolojik analizi yapılır ve kelime kökleri, kelime türleri çıkarılır.
- **Kullanılan Teknolojiler**:
  - `jpype`: Zemberek kütüphanesine Python üzerinden erişmek için.
  - `Pandas`: Şiir verilerini analiz etmek ve işlemek için.

### 3. Stopword Temizleme (`stopwords_cleaning.py`)
- **Amaç**: Şiir metinlerinden anlam taşımayan kelimelerin çıkarılması.
- **Kullanılan Teknolojiler**:
  - `Python set`: Stopword listesinin hızlı kontrolü için.
  - `Pandas`: Temizlenen verilerin düzenlenmesi ve kaydedilmesi.

---

## Kullanım

### Gereksinimler
- Python 3.9 veya üzeri
- Gereken Python kütüphaneleri:
  ```bash
  pip install pandas selenium beautifulsoup4 jpype1
  ```
  Zemberek dosyasının kurulumu ve kullanımı için bu linki ziyaret edin:
  -https://github.com/ozturkberkay/Zemberek-Python-Examples
- [Zemberek JAR dosyası](https://github.com/ahmetaa/zemberek-nlp): `zemberek-full.jar` dosyasını indirin ve uygun bir klasöre yerleştirin.

### Adımlar
1. **Şiir Toplama**:
   ```bash
   python collect_poems.py
   ```
   - Belirtilen kategoriden şiirleri çeker ve `category_agac.csv` dosyasına kaydeder.

2. **Stopword Temizleme**:
   ```bash
   python stopwords_cleaning.py
   ```
   - Şiir metinlerinden stopword'leri temizler ve sonuçları `cleaned_zaman.csv` dosyasına kaydeder.

3. **Zemberek ile İşleme**:
   ```bash
   python zemberek_processing.py
   ```
   - Şiir metinlerini morfolojik analizden geçirir ve sonuçları `simplified_zaman.csv` dosyasına kaydeder.

---

## Dosya Yapısı

- `collect_poems.py`: Şiir toplama işlemleri için kod.
- `zemberek_processing.py`: Zemberek ile morfolojik analiz için kod.
- `stopwords_cleaning.py`: Stopword temizleme işlemi için kod.
- `category_agac.csv`: Web'den çekilen ham veriler.
- `cleaned_zaman.csv`: Stopword'lerden arındırılmış veriler.
- `simplified_zaman.csv`: Zemberek analizinden geçirilmiş veriler.

---



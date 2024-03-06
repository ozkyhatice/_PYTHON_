import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import shelve



class WebScrapper():


    def __init__(self, db_kategori_ismi):
        self.wpage = 'http://books.toscrape.com/index.html'
        self.wpage_soup = self.get_soup(self.wpage)
        self.get_categories()
        self.create_db(db_kategori_ismi)


    def get_soup(self, webpage):
        """Dışarıdan verilen webpage adresine urllib ile istek gönderip, bilgilerin okunacağı ve dışarıya “soup” nesnesini gönderen fonksiyonudur"""
        r = requests.get(webpage)
        if r.status_code == 200:
            print('---Baglanti basarili---')
        elif r.status_code == 404:
            print("---Baglanti Basarisiz---")
        soup=BeautifulSoup(r.content, 'html.parser')
        return soup


    def get_categories(self):
        """Ana sayfada sol taraftaki bulunan kategori listelerini çeker"""
        linkler=self.wpage_soup.find_all(href=re.compile('category'))  #tekrar kullanmak icin degiskene atildi
        tum_sozluk={}
        for link in linkler:
            tum_linkler=urljoin(self.wpage, link.get('href'))
            #print(tum_linkler)
            r_search=re.search(r'(books/)(.+)(/)', tum_linkler)
            if r_search:
                kategori_ismi=r_search.group(2) #kategorileri grupla bulma
                tum_sozluk[kategori_ismi]=tum_linkler
        self.tum_sozluk=tum_sozluk
        #for i,k in self.tum_sozluk.items():
            #print(i)


    def get_prices_stars(self, soup, link):
        """Verilen bir soup nesnesi ve bunun yaratıldığı url adresi ile o sayfadaki kitapların isimlerini, puanlarını, fiyatlarını ve url yi bir sözlük listesi olarak hazırlar"""
        prices_list=[]
        urunler=soup.find_all(class_=re.compile('product_pod'))
        degerler={"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,"Six":6,"Seven":7}
        for urun in urunler:
            h_3=urun.find('h3')
            #print(h_3)
            url=urljoin(link, h_3.a.get('href'))
            kategori_ismi=h_3.string
            price_color=urun.find(class_="price_color").string  #class_ bs4 dan geldi
            price_son=(float(re.sub(r'£', '', price_color)))
            rating=degerler[urun.find(class_=re.compile("rating"))['class'][1]] #hazir degerler kullanildi
            #print(url,kategori_ismi,price_color,price_son,rating)
            prices_list.append({'Name': str(kategori_ismi), 'Rating': rating, 'Price': price_son, 'URL': url})
        return prices_list


    def create_db(self, db_ismi):
        """dışarıdan verilen db_ismi değişkeni ile bir shelve database dosyası açar ve bunu bir sınıf değişkenine atar"""
        self.shelve_db=shelve.open(db_ismi,writeback=True,flag='c')


    def close_db(self):
        self.shelve_db.close()


    def parse(self):
        """Bu fonksiyon ayıklanan her kategori sitesi için sadece ilk sayfalardaki kitapların fiyat ve puanlamalarını bir database nesnesinde tutar"""
        for kategori_ismi, kategori_linki in self.tum_sozluk.items():
            print("Kategori ismi: {} , Kategori linki: {}".format(kategori_ismi, kategori_linki))
            soup=self.get_soup(kategori_linki)
            self.shelve_db[kategori_ismi]=self.get_prices_stars(soup, kategori_linki)
        self.close_db()

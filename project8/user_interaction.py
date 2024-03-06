from model import User, Transaction, Product, DatabaseController
import json

class UserInteraction():

    def __init__(self):

        self.dbi = DatabaseController()
        self.verileri_hazirla()
        print("-----------Veriler Hazirlandi--------------")
        self.print_dbs()
        print("-" *50)

        print("-----------Islemler Basliyor--------------")
        basla = True
        while(basla):
            basla = self.kullaniciya_sor()
            continue

        self.db_sync()
        
        print("-" *50)
        self.print_dbs()
        print("-" *50)

        print("-----------Kullanici harcaamalari raporlaniyor--------------")
        for k in self.dbi.user_db.keys():
            self.harcama_raporla(k)

    def verileri_hazirla(self):
        ''' Bu fonksiyon eger daha once gerekli veri yapilari yaratilmamissa verileri iceri aktarir ve 2 adet dummy kullanici yaratir'''
        if (self.dbi.len(User)) > 0:
            print("Kullanici listesi iceri aktarilmis, DB kullaniliyor")
        else:
            self.dummy_kullanici_yarat()

        if (self.dbi.len(Product)) > 0:
            print("Kullanici listesi iceri aktarilmis, DB kullaniliyor")
        else:
            self.urunleri_oku('urunler_temiz.json')

    def dummy_kullanici_yarat(self):
        self.dbi.add(User('isim1'))
        self.dbi.add(User('isim2'))
    
    def urunleri_oku(self, dosya_ismi):
        file = open(dosya_ismi, 'r')
        urunler = json.load(file)
        for satir in urunler:
            p = Product(satir['isim'], satir['aciklama'], satir['marka'],satir['marka'], float(satir['fiyat']), satir['kategori'], int(satir['stok']))
            self.dbi.add(p)
        file.close()
    
    def kullaniciya_sor(self):
        if input("Yeni bir islem girmek isyor musunuz? [E, H]").lower() !='e':
            return False

        # Birden fazla kullanici tanimli oldugu durum - Sizin yapmaniza gerek yoktu
        u_no = input(" Lutfen Kullanici Numarasi secin [1 veya 2]: ")
        if u_no == '1' or u_no == '2':
            u_secili = 'User-'+u_no
        else:
            print("Dogru bir kullanici secmediniz, programdan cikiliyor")
            return False
        p_no = input("Lutfen bir urun kodu seciniz [1--17]: ")
        
        # Bir baska yontem de direk olarak olusturdugunuz bu anahtar urun_db icerisinde var mi diye bakabilirsiniz
        olasi_urunler = []
        for i in range(1, len(self.dbi.urun_db.keys())+1):
            olasi_urunler.append(str(i))

        if p_no in olasi_urunler:
            p_secili = 'Product-{}'.format(p_no)
        else:
            print("Dogru bur urun numarasi girmediniz, programdan cikiliyor")
            return False

        adet = input("Lutfen satinalma adeti girin: ")
        if not adet.isnumeric():
            print("sayi girmeniz gerekiyor, programdan cikiliyor")
            return False
        
        urun_fiyati = self.dbi.get(p_secili).fiyat

        t = Transaction(u_secili, p_secili, int(adet), urun_fiyati)
        self.dbi.add(t)
        soru = input("Baska bir urun girmek ister misiniz? [E, H]")
        if soru.lower() == 'e':
            print('\n')
            return True
        return False

    def db_sync(self):
        for t_key in self.dbi.satis_db.keys():
            t = self.dbi.get(t_key)
            self.dbi.add(self.dbi.get(t.kullanici).alsat(t))
            self.dbi.add(self.dbi.get(t.urun).alsat(t))

    def harcama_raporla(self, kullanici_kodu):
        u = self.dbi.get(kullanici_kodu)
        print("Kullanici {} toplamda  {} adet siparis vermis ve {} harcamis".format(u.model_id, len(u.siparisler), u.toplam_harcama))


    def print_dbs(self):
        print("Urunler")
        for k in self.dbi.urun_db.keys():
            print(self.dbi.get(k))
        print("Kullanicilar")
        for k in self.dbi.user_db.keys():
            print(self.dbi.get(k))
        print("Islemler")
        for k in self.dbi.satis_db.keys():
            print(self.dbi.get(k))


c = UserInteraction()
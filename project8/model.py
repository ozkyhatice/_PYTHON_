import dbm
import pickle
import json

class BazSinif():
    sinif_sayici = 0
    def __init__(self):
        type(self).sinif_sayici +=1
        self.model_id = '{}-{}'.format(type(self).__name__, type(self).sinif_sayici)

class User(BazSinif):
    def __init__(self, isim):
        super().__init__()
        self.siparisler = []
        self.isim = isim
        self.toplam_harcama = 0.0

    def alsat(self, transaction):
        if transaction.kullanici != self.model_id:
            print('[]', transaction.kullanici, self.model_id)
        else:
            self.siparisler.append({'urun': transaction.urun, 'adet': transaction.adet})
            self.toplam_harcama += transaction.adet * transaction.fiyat
        return self

    def __str__(self):
        return "{} : Kullanici ismi {} ve siparisleri {}".format(self.model_id, self.isim, self.siparisler)

class Transaction(BazSinif):
    def __init__(self, user_id, product_id, adet, fiyat):
        super().__init__()
        self.kullanici = user_id
        self.urun = product_id
        self.fiyat = fiyat
        self.adet = adet

    def __str__(self):
        return "{} : Fatura kullanici ismi {} ve urun {} ve adedi {}".format(self.model_id, self.kullanici, self.urun, self.adet)

class Product(BazSinif):

    def __init__(self, isim, tanim, marka, link, fiyat, kategori, stok):
        super().__init__()
        self.isim = isim
        self.tanim = tanim
        self.link = link
        self.fiyat = fiyat
        self.marka = marka
        self.kategori = kategori
        self.stok = stok

    def fiyat_arttir(self, artis_miktari):
        self.fiyat += artis_miktari
    
    def kampanya(self, yuzde):
        self.fiyat *= (1-yuzde) 
    
    def alsat(self, transaction):
        if self.stok > transaction.adet:
            self.stok -= transaction.adet
        else:
            raise Exception("{} urununden {} adet kalmis, su satinalmayi yapamazsiniz {}".format(self.isim, self.stok, transaction))
        return self

    def __str__(self):
        return "{} : urun ismi {}, kategorisi {}, fiyati {}, kalan adet {}".format(self.model_id, self.isim, self.kategori, self.fiyat, self.stok)

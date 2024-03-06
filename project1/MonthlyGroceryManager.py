class Urun():
    def __init__(self,isim,stok,marka,fiyat,tanim,kategori,link):
        self.isim=isim
        self.stok=int(stok)
        self.marka=marka
        self.fiyat=float(fiyat)
        self.tanim=tanim
        self.kategori=kategori
        self.link=link
    def indirim(self, iskonto_orani,urun):
        self.fiyat=urun*(1-iskonto_orani)
        return self.fiyat
    def zam(self,zam_miktari):
        self.fiyat+=zam_miktari
        return self.fiyat



class Cuzdan():
    def __init__(self,cuzdan_ismi,cuzdan_limiti,urun_sinifi_listesi):
        self.cuzdan_ismi=cuzdan_ismi
        self.cuzdan_limiti=cuzdan_limiti
        self.urun_sinifi_listesi=urun_sinifi_listesi
        

    def urun_listesi(self):
        urun_listem=[]
        for i in self.urun_sinifi_listesi:
            urun_listem+=[i.isim]
        return "satin alinanlar listesi: {}".format(urun_listem)


    def toplam_harcanan_tutar(self,adet):
        toplam_tutar=0
        self.adet=adet
        self.toplam_tutar=toplam_tutar
        for i in range(len(adet)):
            self.toplam_tutar+=self.adet[i]*self.urun_sinifi_listesi[i].fiyat
        return self.toplam_tutar
    

    def harcama_yuzdesi(self):
        harcama_yuzdem=0
        self.harcama_yuzdem=harcama_yuzdem
        self.harcama_yuzdem+=(100*self.toplam_tutar)/self.cuzdan_limiti
        return self.harcama_yuzdem
        
    
    def kalan_para(self):
        kalan_kullanim=self.cuzdan_limiti
        self.kalan_kullanim=kalan_kullanim
        self.kalan_kullanim-=self.toplam_tutar
        return self.kalan_kullanim

    def print_fonk(self):
        return "cuzdan ismi: {}, toplam harcama miktari: {}, kalan para: {}, harcama yüzdesi: {}".format(self.cuzdan_ismi,self.toplam_tutar,self.kalan_kullanim,self.harcama_yuzdem)
urun1=Urun("Duracell İnce","10","Duracell","39.90","4lu",["Ev Yasam","Pil"],"https://cdn.getir.com/product/57ab080887014a03008aaebd_tr_1597245028415.jpeg")
urun2=Urun("semsiye","10","yagmurkovan","94.90","siyah",["ev yasam","semsiye"],"https://cdn.getir.com/product/5d974be3bcb5847fb4d7ba65_tr_1570201391034.jpeg")
urun3=Urun( "Play-Doh Mini Oyun Seti","10", "Play-Doh","69.90","1 Urun",["Ev Yasam", "OyunOyuncak"],"https://cdn.getir.com/product/603fb869648eaa0535fc6088_tr_1614853862147.jpeg")
urun4=Urun("ayakkabi","55","x","449.99","beyaz",["ayakkabi"],"xxxxxxxxx")
urun5=Urun("Monopoly Deal","200","hasbro","79.90","110 kart",["Ev Yasam","Oyun & Oyuncak"],"qqqqqqqqq")

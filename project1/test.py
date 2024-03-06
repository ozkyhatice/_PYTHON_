from MonthlyGroceryManager import Cuzdan
from MonthlyGroceryManager import Urun
urun6=Urun("aa","34","aaa","299.99","aaaaaa",["axaxa"],"xaxaxaxxax")
urun7=Urun("bb","60","bbbb","89.90","abababbb",["skksfh","ksjdkd"],"asmcsmc")
cuzdan_nesnesi=Cuzdan("Deneme2Butcesi",1000,[urun6,urun7])
cuzdan_nesnesi.toplam_harcanan_tutar([1,1])
cuzdan_nesnesi.harcama_yuzdesi()
cuzdan_nesnesi.kalan_para()
print(cuzdan_nesnesi.print_fonk())
import os
suankikonum=os.getcwd()
path=os.path.join(suankikonum,"u.item.txt")
sozluk=dict()

sozluk2=dict()
genres = ["Unknown", "Action", "Adventure", "Animation", "Children's",
"Comedy", "Crime", "Documentary", "Drama",
"Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
"Romance", "Sci-Fi", "Thriller", "War", "Western"]
with open("u.item.txt","r",encoding="ISO-8859-1") as file:
    liste=[]
    deger_list=[]
    for line in file:
        liste+=[line.split('|')]
    for i in liste:
        bos_sozluk=dict()
        if i[5]=="1":
            
            bos_sozluk[genres[0]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[6]=="1":
            
            bos_sozluk[genres[1]]="1"
            sozluk2[i[1]]=bos_sozluk 
        if i[7]=="1":
            
            bos_sozluk[genres[2]]="1"
            sozluk2[i[1]]=bos_sozluk      
        if i[8]=="1":
            
            bos_sozluk[genres[3]]="1"
            sozluk2[i[1]]=bos_sozluk        
        if i[9]=="1":
            
            bos_sozluk[genres[4]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[10]=="1":
            
            bos_sozluk[genres[5]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[11]=="1":
            
            bos_sozluk[genres[6]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[12]=="1":
            
            bos_sozluk[genres[7]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[13]=="1":
            
            bos_sozluk[genres[8]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[14]=="1":
            
            bos_sozluk[genres[9]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[15]=="1":
            
            bos_sozluk[genres[10]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[16]=="1":
            
            bos_sozluk[genres[11]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[17]=="1":
            
            bos_sozluk[genres[12]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[18]=="1":
            
            bos_sozluk[genres[13]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[19]=="1":
            
            bos_sozluk[genres[14]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[20]=="1":
            
            bos_sozluk[genres[15]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[21]=="1":
            
            bos_sozluk[genres[16]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[22]=="1":
            
            bos_sozluk[genres[17]]="1"
            sozluk2[i[1]]=bos_sozluk
        if i[23]=="1":
            
            bos_sozluk[genres[18]]="1"
            sozluk2[i[1]]=bos_sozluk


            
sozluk["filmler"]=sozluk2

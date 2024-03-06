import pandas as pd

data = pd.read_csv("/Users/hatice/Desktop/mlodev/StressLevelDataset.csv")
#data sayısı(rows)
print("There are", len(data), "students in the dataset.")

# Her sütunun benzersiz değerlerini gösterme
for column in data.columns:
    unique_values = data[column].unique()
    print("Sütun {}: {}".format(column, unique_values))
    
# column analysis
# ciktilari txt dosyasina yazdirma
output_file = "sutun_istatistikleri.txt"
with open(output_file, "w") as f:
    for column in data.columns:
        f.write("\n\n**********Sutun Adi: {} ****************\n".format(column))

        # Genel İstatistikler
        gen = data[column].describe()
        f.write("\nGenel İstatistikler:\n")
        f.write(str(gen))

        # Yüzdelik Değerler
        count = data[column].value_counts()
        percentages = (count / count.sum()) * 100
        value_counts_with_percentages = pd.concat([count, percentages], axis=1, keys=["Value Counts", "Percentage"])
        f.write("\n\nYüzdelik Değerler:\n")
        f.write(str(value_counts_with_percentages))
        

#sütun adlarının çıktısı
print(data.columns)
#sütunlarda eksik data yok
null_values = data.isnull().sum()
print("\nnull values\n",null_values)
#tekarlanmış feature yok
duplicated_rows = data.duplicated().sum()
print(duplicated_rows)
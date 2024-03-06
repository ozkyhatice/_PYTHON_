import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from d_tree import decisiontree


def knn_onisleme(df):
    # Veri setinin ilk birkaç satırını gösterir
    print(df.head())
    # Veri setinin satır ve sütun sayısını göster
    print(df.shape)
    # Her sütunun veri türünü göster
    print(df.dtypes)
    # Her sütundaki eksik değerlerin sayısını gösterir
    print(df.isnull().sum())
    
    # Temizleme işlemi yapılacak sütunlar şunlardır
    clean_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Pedigree']
    
    for i in clean_cols:
        # 0 değerlerini sütunun ortalaması ile değiştiriyoruz
        df[i].replace(to_replace=0, value=np.nan, inplace=True)
        # Eksik değerleri sütunun yuvarlanmış ortalaması ile dolduruyoruz
        df[i].fillna(round(df[i].mean(skipna=True)), inplace=True)
    
    # Temizlenmiş veri setinin ilk 10 satırını gösterir
    print(df.head(10))
    # Temizlenmiş veri setinin istatistiklerini gösterir
    print(df.describe().T)

    # Kategorik ve sayısal değişkenler ne olduğu belirleniyor
    categorical_val = ['Outcome']
    numerical_val = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Pedigree', 'Age']

    y = df['Outcome']
    X = df.drop('Outcome', axis=1)

    # Sayısal değişkenler için quantile değerlerini hesaplar
    Q1 = X[numerical_val].quantile(0.25)
    Q3 = X[numerical_val].quantile(0.75)
    IQR = Q3 - Q1
    print(IQR)
    
    # Aykırı değer temizleme işlemi
    # Bu kod, sayısal değişkenlerde (numerical_val) Aykırı Değerleri (outliers) tespit etmek için 
    # İnterkartil Aralık (IQR) yöntemini kullanıyor.
    
    # Bu satırlar, her bir öğenin sayısal değişken numerical_val içinde,
    # Q1 - 1.5 * IQR'den küçük olup olmadığını ve Q3 + 1.5 * IQR'den büyük olup olmadığını kontrol eder.
    (X[numerical_val] < (Q1 - 1.5 * IQR))
    (X[numerical_val] > (Q3 + 1.5 * IQR))
    # Bu satır, her bir öğe için yukarıdaki iki şarttan herhangi birinin doğru olup olmadığını kontrol eder. 
    # Yani, öğe aykırı bir değerse, bu ifade True değerini alır.
    ((X[numerical_val] < (Q1 - 1.5 * IQR)) | (X[numerical_val] > (Q3 + 1.5 * IQR)))
    # Bu satır, her satır için en az bir aykırı değer içerip içermediğini kontrol eder. any(axis=1) ifadesi, 
    # her satırdaki en az bir True değeri varsa genel sonucun True olacağını belirtir.
    ((X[numerical_val] < (Q1 - 1.5 * IQR)) | (X[numerical_val] > (Q3 + 1.5 * IQR))).any(axis=1)
    # Bu satır, aykırı değer içermeyen satırları seçer. ~ operatörü, 
    # True değerleri False'e, False değerleri True'a dönüştürür.
    ~((X[numerical_val] < (Q1 - 1.5 * IQR)) | (X[numerical_val] > (Q3 + 1.5 * IQR))).any(axis=1)
    # Bu satırlar, aykırı değer içermeyen satırları ve bunların hedef değerlerini seçilmiş satırlarla günceller. 
    # X veri çerçevesi ve y hedef değişkeni bu güncellenmiş verilere karşılık gelir.
    X = X[~((X[numerical_val] < (Q1 - 1.5 * IQR)) | (X[numerical_val] > (Q3 + 1.5 * IQR))).any(axis=1)]
    y = y[X.index]
    print(X.shape)
    print(y.shape)
    
    # Sayısal değişkenlerin korelasyon matrisinin ısı haritasını göster
    plt.figure(figsize=(10, 5))
    sns.heatmap(X[numerical_val].corr(), annot=True, fmt='.2f', cmap='coolwarm')
    plt.show()
    knn_train(X, y, numerical_val)


def knn_train(X, y, numerical_val):
    # Veriyi eğitim ve test setlerine bölelim
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    # Veriyi standartlaştıralım
    scaler = StandardScaler()
    # Eğitim verisinin sayısal değişkenlerinin ortalamasını ve varyansını bulup dönüştürelim
    X_train[numerical_val] = scaler.fit_transform(X_train[numerical_val]) 
    # Test verisinde ise önceden bulunan ortalamayı ve varyansı kullanarak dönüştürelim
    X_test[numerical_val] = scaler.transform(X_test[numerical_val]) 
    # Knn modelini n_neighbors = 4 olarak oluşturalım
    knn = KNeighborsClassifier(n_neighbors=4) 
    knn.fit(X_train, y_train) 
    y_pred = knn.predict(X_test) 
    knn_accuracy(X_train, X_test, y_train, y_test, y_pred)
    decisiontree(X, y, X_train, X_test, y_train, y_test)

def knn_accuracy(X_train, X_test, y_train, y_test, y_pred):
    # accuracy hesaplar
    ac = accuracy_score(y_test, y_pred)

    # 1'den 30'a kadar tüm k değerleri için bu değerlere karşılık gelen accuracy değerlerini hesaplıyoruz
    train_accuracies = []
    test_accuracies = []
    neighbors = range(1, 30)
    for neighbor in neighbors:
        knn = KNeighborsClassifier(n_neighbors=neighbor)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        train_accuracies.append(knn.score(X_train, y_train))
        test_accuracies.append(knn.score(X_test, y_test))
    print("Train Score:", train_accuracies)
    print("Test Score:", test_accuracies)
    
    # Farklı k değerleri için doğruluk skorlarını gösteren bir grafik çiz
    plt.figure(figsize=(12, 5))
    plt.plot(neighbors, train_accuracies, label='Eğitim Doğruluğu')
    plt.plot(neighbors, test_accuracies, label='Test Doğruluğu')
    plt.title("KNN: Farklı k değerleri için grafik")
    plt.legend()
    plt.xlabel('k sayısı')
    plt.ylabel('Eğitim ve Test Doğruluğu')
    plt.show()

    # Test doğruluğunu maksimize eden k değerini bul
    max(test_accuracies)
    test_accuracies.index(max(test_accuracies))

    k_opt = neighbors[test_accuracies.index(max(test_accuracies))]
    print('Optimum k değeri: ', k_opt)
    # Precision, recall ve f1-score hesapla
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-Score:", f1)

    # Confusion matrix'i görselleştir
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Outcome', 'Outcome'], yticklabels=['Not Outcome', 'Outcome'])
    plt.xlabel('Tahmin Edilen')
    plt.ylabel('Gerçek Değer')
    plt.title('Confusion Matrix')
    plt.show()

def knn_algo(df):
    # Veri ön işleme adımlarını uygula
    knn_onisleme(df)

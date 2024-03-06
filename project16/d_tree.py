import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

def decisiontree(X, y, X_train, X_test, y_train, y_test):
    # Karar Ağacı modelini oluştur
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    y_pred = dt_model.predict(X_test)
    accuracy_score(y_test, y_pred)
    
    # Karar ağacını görselleştir
    plt.figure(figsize=(10, 10))
    plot_tree(dt_model, filled=True, feature_names=X.columns, class_names=['not churn', 'churn'])
    plt.show()
    
    # Görüldüğü üzere kök düğüm Glucose olarak belirlenmiştir.
    # Max_depth ile karar ağacının derinliği belirtilmiştir.
    # Min_samples_split ile karar ağacı oluşturulurken kullanılan örnek sayısı belirtilmiştir.
    
    dt_model = DecisionTreeClassifier(max_depth=6, min_samples_split=200, random_state=42)
    dt_model.fit(X_train, y_train)
    y_pred = dt_model.predict(X_test)
    accuracy_score(y_test, y_pred)
    
    # Optimum max_depth ve optimum min_samples_split değerlerini belirle
    params = {'max_depth': np.arange(2, 16), 'min_samples_split': np.arange(2, 16)}
    dt_model = DecisionTreeClassifier(random_state=42)
    grid_cv = GridSearchCV(dt_model, param_grid=params, cv=10)
    grid_cv.fit(X_train, y_train)
    print(grid_cv.best_params_)
    print(grid_cv.best_score_)
    
    # Optimum değerlere göre karar ağacını oluştur
    dt_model = DecisionTreeClassifier(max_depth=4, min_samples_split=2, random_state=42)
    dt_model.fit(X_train, y_train)
    y_pred = dt_model.predict(X_test)
    accuracy_score(y_test, y_pred)
    
    # Optimum karar ağacını görselleştir
    plt.figure(figsize=(10, 10))
    plot_tree(dt_model, filled=True, feature_names=X.columns, class_names=['Not Outcome', 'Outcome'])
    plt.show()
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

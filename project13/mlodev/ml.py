from matplotlib import pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error, pair_confusion_matrix
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
import seaborn as sns


data = pd.read_csv("StressLevelDataset.csv")
#on isleme adimlari
data.drop('blood_pressure', axis=1, inplace=True)
sutunlar = ["self_esteem", "depression", "anxiety_level"]
subset = data[sutunlar]
scaler = MinMaxScaler(feature_range=(0, 5))
data[sutunlar] = scaler.fit_transform(data[sutunlar])
normalize = pd.DataFrame(data, columns=sutunlar)
print(normalize.head())

def lin_regression(X_train, y_train, X_test, y_test):
    model_linear = LinearRegression()
    model_linear.fit(X_train, y_train)
    y_train_pred = model_linear.predict(X_train)
    y_test_pred = model_linear.predict(X_test)
    train_rmse = mean_squared_error(y_train, y_train_pred, squared=False)
    test_rmse = mean_squared_error(y_test, y_test_pred, squared=False)
    r2_train_linear = r2_score(y_train, y_train_pred)
    r2_test_linear = r2_score(y_test, y_test_pred)
    print("Linear Regression Results:")
    print(f"Train RMSE: {train_rmse}")
    print(f"Test RMSE: {test_rmse}")
    print(f"Train R^2: {r2_train_linear}")
    print(f"Test R^2: {r2_test_linear}")
    gorsel_lin(train_rmse, test_rmse, r2_train_linear, r2_test_linear)


def gorsel_lin(train_rmse, test_rmse, r2_train, r2_test):
    # RMSE
    plt.figure(figsize=(11, 5))
    sns.barplot(x=['Train RMSE', 'Test RMSE'], y=[train_rmse, test_rmse])
    plt.title('Linear Regression - RMSE')
    plt.show()
    # R^2 Görselleştirme
    plt.figure(figsize=(11, 5))
    sns.barplot(x=['Train R^2', 'Test R^2'], y=[r2_train, r2_test])
    plt.title('Linear Regression - R^2')
    plt.ylim(0, 1)
    plt.show()

def log_regression(X_train, y_train, X_test, y_test):
    # Lojistik regresyon modelini oluşturma
    model = LogisticRegression()
    # Modeli eğitme
    model.fit(X_train, y_train)
    # Test seti üzerinde tahminler yapma
    y_pred = model.predict(X_test)
    # Model performansını değerlendirme
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
    print(f"Confusion Matrix:\n{conf_matrix}")
    print(f"Classification Report:\n{classification_rep}")
    gorsel_log(model,conf_matrix, y_test, y_pred)

def gorsel_log(model, conf_matrix, y_test, y_pred):
    # Confusion Matrix
    plt.figure(figsize=(10, 6))
    sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title('Logistic Reg- Confusion Matrix')
    plt.show()
    # Classification Report
    report_str = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report_str).transpose()
    plt.figure(figsize=(11, 5))
    sns.heatmap(report_df[['precision', 'recall', 'f1-score', 'support']], annot=True)
    plt.title('Logistic Reg-Classification Report')
    plt.show()
#linear regression
X = data[['anxiety_level','self_esteem','mental_health_history','depression','headache','blood_pressure','sleep_quality','breathing_problem','noise_level','living_conditions','safety','basic_needs','academic_performance','study_load','teacher_student_relationship','future_career_concerns','social_support','peer_pressure','extracurricular_activities','bullying']]
y = data["stress_level"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
lin_regression(X_train, y_train, X_test, y_test)

#logistic regression
X = data[['sleep_quality']]
y = data['stress_level']
# Veri setini eğitim ve test setlerine bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
log_regression(X_train, y_train, X_test, y_test)


#PCA YONTEMI
pca = PCA(n_components=5)  
X_pca = pca.fit_transform(data.drop("stress_level", axis=1))
X_pca_df = pd.DataFrame(X_pca, columns=[f"PC{i}" for i in range(1, X_pca.shape[1] + 1)])
data_pca = pd.concat([X_pca_df, data["stress_level"]], axis=1)
X = data_pca.drop("stress_level", axis=1)
y = data_pca["stress_level"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
lin_regression(X_train, y_train, X_test, y_test)
log_regression(X_train, y_train, X_test, y_test)

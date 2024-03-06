from matplotlib import pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.metrics import r2_score
from sklearn.calibration import LabelEncoder
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("./jobs_in_data.csv")

#---------------------------------ANALİZ-----------------------------------------------------------

print(data.shape)

print(data.columns)
print(data.isnull().sum())

with open('uniqval.txt', 'w') as f:
    for column in data.columns:
        uniq_values = data[column].unique()
        print("Sütun {}: {}".format(column, uniq_values), file=f)

output_file = "sutun_istatistikleri.txt"
with open(output_file, "w") as file:
    for column in data.columns:
        file.write("\n\n**********Sutun Adi: {} ****************\n".format(column))
        
        # Genel İstatistikler
        gen = data[column].describe()
        file.write("\nGenel İstatistikler:\n")
        file.write(str(gen))
        
        # Yüzdelik Değerler
        count = data[column].value_counts()
        percentages = (count / count.sum()) * 100
        value_counts_with_percentages = pd.concat([count, percentages], axis=1, keys=["Value Counts", "Percentage"])
        file.write("\n\nYüzdelik Değerler:\n")
        file.write(str(value_counts_with_percentages))

# ---------------------------------------------ON ISLEME---------------------------------------------------------------
tot_col = data.columns
To_Encoder = [ 'work_year', 'salary_currency', 'experience_level', 'employment_type', 'work_setting', 'company_size', 'company_location']
enconder_columns = LabelEncoder()

for columns in To_Encoder:
    if columns in tot_col:
        data[columns] = enconder_columns.fit_transform(data[columns])

df = data.drop(columns = 'salary',axis=1)
df.info()

#------------------------------------------------------K-MEANS-------------------------------------------------------------

# Sayısal özellikleri seçmeliyiz
numeric_features = df[['work_year', 'salary_in_usd', 'experience_level', 'employment_type', 'work_setting', 'company_size']]

# Sayısal özellikleri standartlaştırmalıyız
scaler = StandardScaler()
numeric_features_scaled = scaler.fit_transform(numeric_features)

# küme sayısını belirlemeliyiz ->elbow methodu
sum_of_squared_distances = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(numeric_features_scaled)
    sum_of_squared_distances.append(kmeans.inertia_)

# Elbow Method grafiği:
plt.plot(range(1, 11), sum_of_squared_distances, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

optimal_clusters = 3
# K-Means modelinin uygulanması
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(numeric_features_scaled)

# Sonuçlar:
print(df[['work_year', 'salary_in_usd', 'experience_level', 'employment_type', 'work_setting', 'company_size', 'cluster']])

# Kümeleri görselleştime
fig = px.scatter_3d(df, x='work_year', y='salary_in_usd', z='experience_level', color='cluster', symbol='cluster',
                    size_max=18, opacity=0.7, title='K-Means Clustering Results')
fig.show()
sns.scatterplot(x='salary_in_usd', y='experience_level', hue='cluster', data=df, palette='viridis')
plt.title('K-Means Clustering Results in 2D')
plt.show()


# --------------------------------------------GMM KUMELEME-----------------------------------------------
# Sayısal özellikleri seçme
numeric_features_gmm = df[['work_year', 'salary_in_usd', 'experience_level', 'employment_type', 'work_setting', 'company_size']]

# Sayısal özellikleri standartlaştırma
scaler = StandardScaler()
numeric_features_scaled_gmm = scaler.fit_transform(numeric_features_gmm)

# Elbow Method ile optimal küme sayısını bulma
inertia_values = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(numeric_features_scaled_gmm)
    inertia_values.append(kmeans.inertia_)

# Elbow Method
plt.plot(range(1, 11), inertia_values, marker='o')
plt.title('Elbow Method for GMM')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

# Optimal küme sayısını belirleme
optimal_clusters = 5

# GMM modelini uygulama
gmm = GaussianMixture(n_components=optimal_clusters, random_state=42)
df['gmm_cluster'] = gmm.fit_predict(numeric_features_scaled_gmm)

# GMM kümeleme sonuçlarını görselleştirme
sns.scatterplot(x='salary_in_usd', y='experience_level', hue='gmm_cluster', data=df, palette='viridis')
plt.title(f'GMM Clustering Results in 2D (Clusters: {optimal_clusters})')
plt.show()

#---------------------------------------XGB ALGORİTMASI--------------------------------------------------
features = df[['work_year', 'experience_level', 'work_setting', 'company_size', 'company_location']]
target = df['salary_in_usd']
# Eğitim ve test setlerini oluşturma
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
# XGBoost Regressor modelini oluşturma
xgb_model = XGBRegressor(
    max_depth=3,
    learning_rate=0.05,
    n_estimators=100,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=0.1,
    random_state=42
)
# Modeli eğitme
xgb_model.fit(X_train, y_train)
# Test seti üzerinde tahmin yapma
y_pred = xgb_model.predict(X_test)

# Hata ölçümleri
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Sonuçları yazdırma
print("Mean Squared Error (MSE):", mse)
print("R-squared Score (R2):", r2)

plt.scatter(y_test, y_pred)
plt.xlabel('Gerçek Değerler')
plt.ylabel('Tahmin Edilen Değerler')
plt.title('Gerçek vs Tahmin Edilen Değerler')
plt.show()

#--------------------------------------YAPAY SİNİR AĞI---------------------------------------

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Veri setini ve hedef değişkenini belirleme
features = data[['work_year', 'experience_level', 'employment_type', 'work_setting', 'company_size']]
target = data['salary_in_usd']

# Eğitim ve test setlerini oluşturma
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Sayısal özellikleri standartlaştırma
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Yapay Sinir Ağı modelini oluşturma
model = Sequential()

# Giriş katmanı
model.add(Dense(units=128, activation='relu', input_dim=X_train.shape[1]))

# Gizli katmanlar
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.2))  # Dropout katmanı ekledik (overfitting'i önlemek için)
model.add(Dense(units=32, activation='relu'))

# Çıkış katmanı
model.add(Dense(units=1, activation='linear'))

# Modeli derleme
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mean_squared_error')

# Modeli eğitme
history = model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_scaled, y_test))

# Modelin test verisi üzerinde değerlendirilmesi
y_pred = model.predict(X_test_scaled)

# Hata ölçümleri
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Sonuçları yazdırma
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("R-squared Score (R2):", r2)

# Eğitim sürecinin görselleştirilmesi
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# -*- coding: utf-8 -*-
"""Crime_Incidents_in_2024.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vg6pvWz47tc2CH2KHuLQtEQBS04pydoA
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.utils import shuffle
from sklearn.model_selection import GridSearchCV
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv("/content/Crime_Incidents_in_2024.csv")

df

df.head()

df.tail()

df.info()

df.describe()

df.isnull().sum()

# Drop columns with all null values (OCTO_RECORD_ID) and those with a high percentage of null values (BID)
df = df.drop(columns=['OCTO_RECORD_ID', 'BID'])

# Filling missing values with appropriate strategies:
# - For numerical columns, we'll use the median to handle any skewed data.
# - For categorical columns, we'll use the mode (most frequent value).

# Fill numerical columns with the median
numerical_columns = ['WARD', 'DISTRICT', 'PSA', 'CENSUS_TRACT']
for col in numerical_columns:
    df[col] = df[col].fillna(df[col].median())

# Fill categorical columns with the mode
categorical_columns = ['ANC', 'NEIGHBORHOOD_CLUSTER', 'BLOCK_GROUP', 'VOTING_PRECINCT', 'START_DATE', 'END_DATE']
for col in categorical_columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# Display basic information about the cleaned dataset to verify
df.info()
df.head()

df.isnull().sum()

df.duplicated().sum()

pd.DataFrame(df.dtypes)

# Convert date columns to datetime
df["START_DATE"] = pd.to_datetime(df["START_DATE"], errors='coerce')
df["END_DATE"] = pd.to_datetime(df["END_DATE"], errors='coerce')
df["REPORT_DAT"] = pd.to_datetime(df["REPORT_DAT"], errors='coerce')

# Convert useful categoricals
cat_cols = ["SHIFT", "METHOD", "ANC", "NEIGHBORHOOD_CLUSTER", "BLOCK_GROUP", "VOTING_PRECINCT"]
for col in cat_cols:
    df[col] = df[col].astype("category")
pd.DataFrame(df.dtypes).T

pd.DataFrame(df.columns.tolist())

for col in df.select_dtypes("number").columns:
    plt.figure(figsize = ( 3, 3))
    sns.boxplot(df[col])
    plt.show()

for col in df.select_dtypes("number").columns:
    Q1 = np.quantile(df[col] , .25)
    Q3 = np.quantile(df[col] , .75)
    IQR = Q3 - Q1
    upper = Q3 +(1.5 * IQR)
    lower = Q1 -(1.5 * IQR)


    upper_outliers = df[df[col] > upper][col].values
    df[col].replace(upper_outliers, upper, inplace = True)
    lower_outliers = df[df[col] < lower][col].values
    df[col].replace(lower_outliers, lower, inplace = True)

# Assuming df is your cleaned DataFrame, we'll adjust it for readability
# Define the number of rows and columns for the subplot grid
num_cols = len(df.select_dtypes("number").columns)
rows = (num_cols // 4) + 1  # Creating a dynamic number of rows
cols = 4  # Fixed number of columns

# Create the subplots
fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 3), constrained_layout=True)

# Flatten the axes array to easily index them in the loop
axes = axes.flatten()

# Plot boxplots for each numerical column
for i, col in enumerate(df.select_dtypes("number").columns):
    sns.boxplot(data=df[col], ax=axes[i])
    axes[i].set_title(col)

# Hide any remaining empty subplots
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.show()

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Step 1: Visualize data distributions using a pair plot for numerical features
# Using a sample to avoid overplotting
df = df.sample(500, random_state=42)  # Random sample for clarity in plots

sns.pairplot(df.select_dtypes(include='number'))
plt.suptitle('Pairwise Scatter Plot of Numerical Features', y=1.02)
plt.show()

# Step 2: Visualize correlations using a heatmap for numerical features only
plt.figure(figsize=(12, 8))

# Use only the numeric columns for correlation
numeric_df = df.select_dtypes(include='number')

# Plotting the correlation heatmap
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Numerical Features')
plt.show()

# Step 3: Standardize the numerical data for K-means clustering
scaler = StandardScaler()
numerical_data = df.select_dtypes(include='number')
scaled_data = scaler.fit_transform(numerical_data)

# Step 4: Apply K-means clustering with an optimal number of clusters
# Using the Elbow method to determine the optimal number of clusters
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Plot the Elbow method result
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o', linestyle='-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.grid(True)
plt.show()

# Step 5: Fit K-means using the chosen number of clusters (let's assume k=4 based on the elbow plot)
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Add cluster labels to the original data for visualization
df['Cluster'] = clusters

# Step 6: Visualize the clustering results using PCA for dimensionality reduction
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(scaled_data)

plt.figure(figsize=(10, 8))
sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=df['Cluster'], palette='viridis', s=50)
plt.title('K-means Clustering Visualization with PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.show()

# === Clean Data ===

# Drop only columns that exist
cols_to_drop = ['OCTO_RECORD_ID', 'BID']
df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)

# Define numerical and categorical columns
num_cols = ['WARD', 'DISTRICT', 'PSA', 'CENSUS_TRACT']
cat_cols = ['ANC', 'NEIGHBORHOOD_CLUSTER', 'BLOCK_GROUP', 'VOTING_PRECINCT', 'START_DATE', 'END_DATE']

# Fill missing values for numerical columns
for col in num_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Fill missing values for categorical/date columns
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

# === Encode Features ===
df['METHOD'] = LabelEncoder().fit_transform(df['METHOD'])
df['OFFENSE'] = LabelEncoder().fit_transform(df['OFFENSE'])  # Target

features = ['WARD', 'DISTRICT', 'PSA', 'CENSUS_TRACT', 'METHOD']
target = 'OFFENSE'

X = df[features]
y = df[target]

# === Split & Scale ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# === Handle Imbalanced Dataset with SMOTE ===
# Ensure X_train and y_train are aligned
X_train = pd.DataFrame(X_train).reset_index(drop=True)
y_train = pd.Series(y_train).reset_index(drop=True)

# Filter out very rare classes (those with fewer than 2 samples)
class_counts = y_train.value_counts()
valid_classes = class_counts[class_counts >= 2].index

# Build mask and filter
mask = y_train.isin(valid_classes)
X_train = X_train[mask].reset_index(drop=True)
y_train = y_train[mask].reset_index(drop=True)

# Check class balance
print("Before SMOTE:", y_train.value_counts())

from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42, k_neighbors=1)  # Use k=1 since have a class with only 2 samples
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Check new distribution
print("After SMOTE:", pd.Series(y_train_resampled).value_counts())

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

# === Setup Preprocessing ===
categorical_cols = X_train.select_dtypes(include='category').columns.tolist()
numerical_cols = X_train.select_dtypes(include='number').columns.tolist()

preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ('num', SimpleImputer(strategy='median'), numerical_cols)
])

# === Define Models ===
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Neural Network": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
}

# === Train and Evaluate Each Model with Pipeline ===
for name, model in models.items():
    pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    print(f"\nTraining {name}...")
    pipe.fit(X_train_resampled, y_train_resampled)
    y_pred = pipe.predict(X_test)
    print(f"{name} Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

print("Unique labels in y_train_resampled:", sorted(y_train_resampled.unique()))

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline

# Encode labels into 0 to n_classes-1
le = LabelEncoder()
y_train_encoded = le.fit_transform(y_train_resampled)

# Confirm correct number of classes
print("Encoded class labels:", list(le.classes_))
print("Encoded y_train values:", np.unique(y_train_encoded))

# Define Stratified CV
stratified_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

# Define pipeline
xgb_pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(
        use_label_encoder=False,
        eval_metric='mlogloss',
        objective='multi:softprob',
        num_class=len(np.unique(y_train_encoded))  # Safe class count
    ))
])

# Define parameter grid
param_grid = {
    'classifier__n_estimators': [100, 300],
    'classifier__learning_rate': [0.01, 0.1],
    'classifier__max_depth': [3, 6],
    'classifier__min_child_weight': [1, 3]
}

# Grid search
grid_search = GridSearchCV(
    estimator=xgb_pipe,
    param_grid=param_grid,
    scoring='accuracy',
    cv=stratified_cv,
    n_jobs=-1,
    error_score='raise'
)

# Fit with encoded y
grid_search.fit(X_train_resampled, y_train_encoded)

# Best parameters
print("✅ Best XGBoost Parameters:", grid_search.best_params_)

# Final XGBoost Evaluation
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\nFinal XGBoost Model Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

missing_classes = set(y_test) - set(y_train_resampled)
if missing_classes:
    print("⚠️ Missing classes in training:", missing_classes)

import pandas as pd
print(pd.Series(y).value_counts())

# Get counts of each class
class_counts = y.value_counts()

# Filter to classes with at least 5 samples
valid_classes = class_counts[class_counts >= 5].index

# Filter both X and y
X_filtered = X[y.isin(valid_classes)]
y_filtered = y[y.isin(valid_classes)]

# Now you can split safely with stratify
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_filtered, y_filtered, test_size=0.2, stratify=y_filtered, random_state=42)

print(y_filtered.value_counts())

from sklearn.preprocessing import LabelEncoder

# Relabel to 0, 1, ..., N-1
label_encoder = LabelEncoder()
y_filtered = label_encoder.fit_transform(y_filtered)

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

from sklearn.preprocessing import LabelEncoder

# Remove rare classes (like 2 and 5)
valid_classes = y.value_counts()[y.value_counts() >= 5].index
X_filtered = X[y.isin(valid_classes)]
y_filtered = y[y.isin(valid_classes)]

# Relabel classes to be 0...N-1 for XGBoost compatibility
label_encoder = LabelEncoder()
y_filtered_encoded = label_encoder.fit_transform(y_filtered)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_filtered, y_filtered_encoded, test_size=0.2, stratify=y_filtered_encoded, random_state=42
)

# Apply SMOTE
smote = SMOTE(random_state=42, k_neighbors=1)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)


# === Preprocessing ===
# Assume you have numeric and categorical features
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

# === XGBoost Pipeline ===
xgb_pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'))
])

# === Grid Search Parameters ===
param_grid = {
    'classifier__n_estimators': [100, 300],
    'classifier__learning_rate': [0.01, 0.1],
    'classifier__max_depth': [3, 6],
    'classifier__min_child_weight': [1, 3]
}

# === Grid Search ===
grid_search = GridSearchCV(xgb_pipe, param_grid, scoring='accuracy', cv=3, n_jobs=-1)
grid_search.fit(X_train_resampled, y_train_resampled)

print("✅ Best XGBoost Parameters:", grid_search.best_params_)

# === Final Evaluation ===
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\n✅ Final XGBoost Model Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

from sklearn.preprocessing import LabelEncoder
import numpy as np

# === 1. Label Encode y ===
le = LabelEncoder()
y_encoded = le.fit_transform(y)
X = X.reset_index(drop=True)
y = pd.Series(y_encoded)

# === 2. Remove rare classes before split ===
value_counts = y.value_counts()
valid_classes = value_counts[value_counts >= 3].index
X = X[y.isin(valid_classes)]
y = y[y.isin(valid_classes)]

# === 3. Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === 4. Filter rare classes from train set ===
train_counts = y_train.value_counts()
valid_train_classes = train_counts[train_counts >= 2].index
X_train = X_train[y_train.isin(valid_train_classes)]
y_train = y_train[y_train.isin(valid_train_classes)]

# === 5. SMOTETomek ===
smote_tomek = SMOTETomek(random_state=42, smote=SMOTE(k_neighbors=1))
X_train_resampled, y_train_resampled = smote_tomek.fit_resample(X_train, y_train)

# === 6. Fit XGBoost ===
xgb_final = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    min_child_weight=2,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=1.0,
    use_label_encoder=False,
    eval_metric="mlogloss",
    num_class=len(np.unique(y_train_resampled))  # explicitly set number of classes
)

xgb_final.fit(X_train_resampled, y_train_resampled)

# === 7. Evaluate ===
y_pred = xgb_final.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Final XGBoost Model Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred, target_names=le.classes_.astype(str)))


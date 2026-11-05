import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

print("--- Training Linear Regression (Time Estimator) ---")

# 1. Dataset Load 
df = pd.read_csv('taskforge_large_dataset.csv')

# Features engineering (Category code + Text length)
df['Category_Num'] = df['Category'].astype('category').cat.codes
df['Text_Length'] = df['Task_Text'].apply(len)

X_time = df[['Text_Length', 'Category_Num']]
y_time = df['Time_Hours']

# 2. Model Training
lr_model = LinearRegression()
lr_model.fit(X_time, y_time)

# 3. Save Model
with open('linear_model.pkl', 'wb') as f:
    pickle.dump(lr_model, f)

print("Saved: linear_model.pkl\n")
print("--- All Three Models Trained & Saved Separately Successfully! ---")
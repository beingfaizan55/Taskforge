import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
import pickle

print("--- Training ID3 Decision Tree (Priority Predictor) ---")

# 1. Dataset Load Karein
df = pd.read_csv('taskforge_large_dataset.csv')

# Category ko numeric codes mein convert karna
df['Category_Num'] = df['Category'].astype('category').cat.codes
X_tree = df[['Category_Num']]
y_priority = df['Priority']

# 2. ID3 Model Training (criterion='entropy' is the core of ID3)
id3_model = DecisionTreeClassifier(criterion='entropy', random_state=42)
id3_model.fit(X_tree, y_priority)

# 3. Decision Tree Rules ko Terminal par Print Karna
tree_rules = export_text(id3_model, feature_names=['Category_Num'])
print("\n--- ID3 Decision Tree Structure (Rules) ---")
print(tree_rules)

# 4. Save Model
with open('id3_model.pkl', 'wb') as f:
    pickle.dump(id3_model, f)

print("\nSaved: id3_model.pkl")
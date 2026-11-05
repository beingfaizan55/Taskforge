import os
import pickle

# 1. Apni Master Class Define Karein
class TaskMasterPipeline:
    def __init__(self, vectorizer, nb_model, id3_model, linear_model):
        self.vectorizer = vectorizer
        self.nb_model = nb_model
        self.id3_model = id3_model
        self.linear_model = linear_model
        self.category_map = {'Design': 0, 'Finance': 1, 'Health': 2, 'Personal': 3, 'Study': 4, 'Work': 5}
        
    def predict_all(self, task_text):
        # Naive Bayes
        vec = self.vectorizer.transform([task_text])
        category = self.nb_model.predict(vec)[0]
        cat_num = self.category_map.get(category, 0)
        
        # ID3
        priority = self.id3_model.predict([[cat_num]])[0]
        
        # Linear Regression
        time = self.linear_model.predict([[len(task_text), cat_num]])[0]
        
        return {
            "category": category,
            "priority": priority,
            "estimated_hours": round(max(0.5, float(time)), 1)
        }

# 2. Pehle se trained teeno models load karein
base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, 'nb_model.pkl'), 'rb') as f:
    nb_data = pickle.load(f)
    
with open(os.path.join(base_dir, 'id3_model.pkl'), 'rb') as f:
    id3_model = pickle.load(f)
    
with open(os.path.join(base_dir, 'linear_model.pkl'), 'rb') as f:
    linear_model = pickle.load(f)

# 3. Teeno ko ek Class mein combine karein
master_pipeline = TaskMasterPipeline(
    vectorizer=nb_data['vectorizer'],
    nb_model=nb_data['model'],
    id3_model=id3_model,
    linear_model=linear_model
)

# 4. Final 'master_model.pkl' save kar dein
output_path = os.path.join(base_dir, 'master_model.pkl')
with open(output_path, 'wb') as f:
    pickle.dump(master_pipeline, f)

print(f"Success! Master Model saved at: {output_path}")
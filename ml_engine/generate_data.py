import pandas as pd
import random

# Har category ke liye mukhtalif verbs aur nouns define kiye hain
categories = {
    'Work': {
        'verbs': ['Fix', 'Design', 'Develop', 'Review', 'Deploy', 'Test', 'Present', 'Analyze'],
        'nouns': ['frontend bug', 'API endpoint', 'database schema', 'server logs', 'client presentation', 'sales report', 'UI/UX mockups'],
        'priorities': ['Medium', 'High']
    },
    'Personal': {
        'verbs': ['Buy', 'Clean', 'Organize', 'Call', 'Plan', 'Visit'],
        'nouns': ['groceries', 'garage', 'wardrobe', 'family', 'weekend trip', 'friend'],
        'priorities': ['Low', 'Medium']
    },
    'Finance': {
        'verbs': ['Pay', 'Calculate', 'Review', 'File', 'Clear'],
        'nouns': ['electricity bill', 'monthly taxes', 'bank statement', 'credit card dues', 'freelance invoice'],
        'priorities': ['High']
    },
    'Study': {
        'verbs': ['Read', 'Complete', 'Research', 'Write', 'Revise'],
        'nouns': ['chapter 4', 'machine learning assignment', 'OS project', 'thesis paper', 'notes'],
        'priorities': ['Medium', 'High']
    },
    'Health': {
        'verbs': ['Go to', 'Schedule', 'Buy', 'Do', 'Attend'],
        'nouns': ['gym', 'dentist appointment', 'vitamins', 'yoga session', 'therapy'],
        'priorities': ['Medium']
    }
}

data_list = []
total_rows = 50000  # 50,000 tasks ka dataset generate hoga

print(f"Generating {total_rows} diverse tasks...")

for _ in range(total_rows):
    cat = random.choice(list(categories.keys()))
    verb = random.choice(categories[cat]['verbs'])
    noun = random.choice(categories[cat]['nouns'])
    task_text = f"{verb} {noun}"
    priority = random.choice(categories[cat]['priorities'])
    
    base_time = random.uniform(0.5, 4.0)
    if priority == 'High':
        time_hours = round(base_time + random.uniform(1.0, 3.0), 1)
    else:
        time_hours = round(base_time, 1)

    data_list.append([task_text, cat, priority, time_hours])

# DataFrame bana kar CSV mein save karna
df = pd.DataFrame(data_list, columns=['Task_Text', 'Category', 'Priority', 'Time_Hours'])
df.to_csv('taskforge_large_dataset.csv', index=False)

print("Data generation complete! File saved as 'taskforge_large_dataset.csv'")
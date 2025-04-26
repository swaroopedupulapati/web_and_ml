from flask import Flask,render_template,redirect,request
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd

# Load the dataset
file_path ="salary_Data.csv"
df = pd.read_csv(file_path)
# Drop rows with missing salary values since it's the target variable
df_cleaned = df.dropna(subset=['Salary'])

# Define features and target variable
X = df_cleaned.drop(columns=['Salary'])
y = df_cleaned['Salary']

# Identify categorical and numerical features
categorical_features = ['Gender', 'Education Level', 'Jobrole']
numerical_features = ['YearsExperience']

# Preprocessing pipelines
categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean'))  # Handle missing numerical values
])
# Combine transformations
preprocessor = ColumnTransformer(transformers=[
    ('num', numerical_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])

# Create regression model pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model_pipeline.fit(X_train, y_train)

# Function to predict salary based on user input
def predict_salary(input_data):
    input_df = pd.DataFrame(input_data)
    # Use the trained model pipeline to predict the salary
    predicted_salary = model_pipeline.predict(input_df)
    print(f"Predicted Salary: {predicted_salary[0]:.2f}")
    return round(predicted_salary[0]/1000 , 2)

global a
data=(df_cleaned.drop(['YearsExperience','Salary'],axis="columns"))
a={}
for i in data:
    j=list(set(df[i]))
    a[i]=j

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    global a
    if request.method=='POST':
        data={}
        for i in a.keys():
            data[i]=[request.form[i]]
        data["YearsExperience"]=[request.form["exp"]]
        print(data)
        salary=predict_salary(data)
        return render_template("index.html",data=a,salary=f"Your predicted salary is = {salary} K per month")
    return render_template("index.html",data=a)

            
if __name__ == '__main__':
    app.run(debug=True)


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

# Display basic information and first few rows
df.info(), df.head()

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

# Make predictions
y_pred = model_pipeline.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

mae, r2


# Function to predict salary based on user input
def predict_salary():
    # Collect input data from the user
    gender = input("Enter Gender (Male/Female): ")
    education_level = input("Enter Education Level (e.g., Bachelor's, Master's, PhD): ")
    jobrole = input("Enter Job Role (e.g., Software Engineer, Data Analyst, etc.): ")
    years_experience = float(input("Enter YearsExperience: "))

    # Create a dataframe with the input data
    input_data = {
        'Gender': [gender],
        'Education Level': [education_level],
        'Jobrole': [jobrole],
        'YearsExperience': [years_experience]
    }
    
    import pandas as pd
    input_df = pd.DataFrame(input_data)
    
    # Use the trained model pipeline to predict the salary
    predicted_salary = model_pipeline.predict(input_df)
    
    print(f"Predicted Salary: {predicted_salary[0]:.2f}")

# Run the prediction function
predict_salary()

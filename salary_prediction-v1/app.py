from flask import Flask,redirect,render_template,request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error


df=pd.read_csv('D:Salary_Data.csv')
data=(df.drop(['YearsExperience','Salary'],axis="columns"))
global a
a={}
for i in data:
    j=list(set(df[i]))
    a[i]=j

label_encoder = LabelEncoder()
df['Jobrole'] = label_encoder.fit_transform(df['Jobrole'])
X = df[['YearsExperience', 'Jobrole']]
y = df['Salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
def mode(years_exp,job_role):
    job_role_encoded = label_encoder.transform([job_role])
    input_data = pd.DataFrame({'YearsExperience': [years_exp], 'Jobrole': job_role_encoded})
    predicted_salary = model.predict(input_data)
    return predicted_salary[0]

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    global a
    if request.method == 'POST':
        exp=request.form['exp']
        jobrole=request.form['Jobrole']
        salary=round(mode(exp, jobrole)/1000 ,1)
        return render_template("index.html",data=a,salary=f"Your predicted salary is = {salary} K per month")
    
    return render_template("index.html",data=a)

if __name__ == '__main__':
    app.run(debug=True)
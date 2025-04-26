import numpy as np 
import cv2
import joblib 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder 
from sklearn.ensemble import RandomForestClassifier
from skimage.feature import hog 
from glob import glob
import os
def load_data(img_size=(128,128)):
    dataset_path="flower_images"
    images=[]
    labels=[]
    class_names=os.listdir(dataset_path)
    for class_name in class_names:
        class_path=os.path.join(dataset_path,class_name)
        for img_path in glob(os.path.join(class_path,"*.jpg")):
            img=cv2.imread(img_path)
            if img is None:
                continue
            img=cv2.resize(img,img_size)
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            feature=hog(gray,pixels_per_cell=(8,8),cells_per_block=(2,2),feature_vector=True)
            images.append(feature)
            labels.append(class_name)
    return np.array(images), np.array(labels)
def train(x,y):
    le=LabelEncoder()
    y=le.fit_transform(y)
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=55)
    model=RandomForestClassifier(n_estimators=100,random_state=45)
    model.fit(x_train,y_train)
    prediction=model.predict(x_test)
    acc=accuracy_score(y_test,prediction)
    joblib.dump((model,le), "flower_classifier.pkl")
    print(f"model trained with {acc*100: .2f}% accuracy")
x,y=load_data()
train(x,y)
# helper libraries
import pandas as pd
import numpy as np
from tqdm import tqdm
from joblib import dump, load

# inner files
from models.KNN.knn import knn_classify
from models.NaiveBayes.naive_bayes import naive_bayes_classify
from models.LogisticRegression.logistic_regression import logistic_regression_classifier
from models.RandomForest.random_forest import random_forest_classify
from models.SVM.svm import svm_classify
from scripts.config import DATAFRAME_PATH, PATH_TO_BINARY_MODELS, PATH_TO_LAST_STEP_MODELS
from .logictic_regression_predict import train_logistic_regression
from scripts.extract_features import extract_audio_features

# skitlearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, recall_score, precision_score

# RUN AS MODULE python -m predict.logictic_regression_predict

class Pipeline:

    
#, 'blues', 'hip-hop', 'rock', 'classical', 'reggae', 'country', 'metal', 'techno', 'jazz'
# , naive_bayes_classify, logistic_regression_classifier, random_forest_classify, svm_classify
    def __init__(self, df_music):
        self.CATEGORIES = ['rock']
        self.MODELS_FUN = [knn_classify]
        
        self.df_music = df_music
        # dictionary of models
        self.models = {}
        # dictionary for regression
        self.logistic_regressions = {}

        self.train_pipeline()
    
    def train_pipeline(self):
        for category in tqdm(self.CATEGORIES):
            # for each category we train a model, 
            # create matrix of probabilities and create a vector of true labels
            X, y = self.train_all_models_for_category(category)

            self.models[category] = {
                'feature_matrix': X,
                'labels': y
            }
            
            # for each category, based on vectors from models
            # we train logistic regression
            # category is passed solely for organising
            train_logistic_regression(X, y, category)
     


    """returns trained models, matrix with probabilities form each model and true labels"""
    def train_all_models_for_category(self, category: str):
        # matrix [test_size]x[#models]
        # for each of 200 songs (songs from test set for each model)
        # we gather probabilities for it being from 'category'
        # resulting matrix is 200x[#models] -> 200 samples with #models features
        songs_probs_matrix = []
        trained_models = []

        # here we run models for each category and save them to reuse
        for model_fun in self.MODELS_FUN:
            
            _, probabilities, y = model_fun(self.df_music, category)
            # build vector of probabilities
            songs_probs_matrix.append(probabilities)
        # each model uses the same sample to calcualte test, so y labels are the same
        return np.column_stack(songs_probs_matrix), y.values


    def classify_song(self, song_path: str):
        
        # make sure values are in the same order as in trained CSV
        # creates a vector (1,37) that can be fed to the model
        features = np.array([float(num) for num in extract_audio_features(song_path).values()]).reshape(1, -1)
       
        
        # print(features.shape)

        # print(extract_audio_features(song_path).values())

        for category in self.CATEGORIES:

            logistic = load(f'{PATH_TO_LAST_STEP_MODELS}/categorized_regression/{category}.joblib')

            # Load saved components
            knn = load(f'{PATH_TO_BINARY_MODELS}/knn/knn_model_{category}.joblib')
            scaler = load(f'{PATH_TO_BINARY_MODELS}/knn/scaler_{category}.joblib')
            pca = load(f'{PATH_TO_BINARY_MODELS}/knn/pca_{category}.joblib')
            
            # Transform features
            X_scaled = scaler.transform(features)
            # X_pca = pca.transform(X_scaled)
            
            # biorę PPB na 1 z każdego modelu, w kolejnych kategoriach
            probs_knn = knn.predict_proba(X_scaled)[:, 1]

            logistic_prob = logistic.predict_proba(np.array([probs_knn]))[:, 1]
            
            print(f"Probability for {category}: {probs_knn}")
            print(f"probability according to logistic regression", logistic_prob)





if __name__ == "__main__":
    DF = pd.read_csv(DATAFRAME_PATH)
    pipeline = Pipeline(DF)

    song_path = "/Users/szymon/Documents/projekciki/Music-Genre-Classifier/Guns N' Roses - Sweet Child O' Mine (Official Music Video).mp3"

    pipeline.classify_song("/Users/szymon/Documents/projekciki/Music-Genre-Classifier/ABBA - Gimme! Gimme! Gimme! (A Man After Midnight).mp3")
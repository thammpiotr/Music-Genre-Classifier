import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def naive_bayes_classify(df_music:pd.DataFrame, category:str, verbose=0):
    df = df_music.drop(columns=["title"])
    df = df[df[category].isin([0, 1])]

    feature_cols = df.select_dtypes(include=[np.number]).columns
    X = df[feature_cols]
    y = df[category]

    # Scaler - standardizes each column to have a mean of 0 and a standard deviation of 1
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=36) 
    X_pca = pca.fit_transform(X_scaled)

    X_train, X_test, y_train, y_test = train_test_split(X_pca, y, random_state=42, test_size=0.2, stratify=y)

    model = GaussianNB()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    precision = precision_score(y_test, y_pred, average='macro')

    if verbose:
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nModel Performance:")
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    return model, y_prob, y_test

if __name__ == "__main__":
    df = pd.read_csv('../../data/processed/music_features.csv')
    accuracy, probabilities = naive_bayes_classify(df, "rock")
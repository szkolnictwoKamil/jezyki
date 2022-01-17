#!/usr/bin/env python
# coding: utf-8

import itertools
import logging
import os
import re
import sys
from collections import Counter
from string import ascii_lowercase

import numpy as np
import pandas as pd
import unidecode
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearnex import patch_sklearn
from tqdm import tqdm

patch_sklearn()

log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
logger = logging.getLogger(__name__)

COLNAMES = ['model', 'dataset', 'accuracy', 'precision', 'recall', 'F1 score']


def clean_text(line):
    line = re.sub(r"[^\w]", " ", line)
    line = re.sub(r"[0-9]", " ", line)
    line = re.sub(r"\s\s+", " ", line)
    line = unidecode.unidecode(line)
    line = line.lower()

    return line


def get_ngrams(string, n=2):
    max_len = len(string) - n + 2
    return (string[i:i + n] for i in range(max_len))


def process_input(line, keywords, n=2):
    counter = Counter(get_ngrams(line, n=n))

    return np.array([counter[keyword] for keyword in keywords])


def get_keywords(filenames, n=2, max_keywords=500):
    logger.info(f'Get all possible {n}-grams')
    
    keywords = Counter()
    for filename in filenames:
        country = filename.split(".")[0]
        filepath = f"dane/{country}.txt"

        with open(filepath, "r", encoding="iso-8859-1") as input_file:
            my_file = input_file.read()
            my_file = clean_text(my_file)
            
            max_len = len(my_file) - n + 2
            counter = Counter((my_file[i:i+n] for i in range(max_len)))
            
            keywords.update(counter)
            
    logger.info(f'No. all possible {n}-grams: {len(keywords)}, at most {max_keywords} is taken')
    keywords = keywords.most_common(max_keywords)
    
    return [keyword[0] for keyword in keywords]


def load_datasets(filenames, N, chunk_size):
    logger.info('Loading consecutive files')
    
    keywords = get_keywords(filenames, n=N)

    for filename in tqdm(filenames):
        country = filename.split(".")[0]
        filepath = f"dane/{country}.txt"

        with open(filepath, "r", encoding="iso-8859-1") as input_file:
            my_file = input_file.read()
            my_file = clean_text(my_file)
            lines = [my_file[i:i + chunk_size] for i in range(0, len(my_file), chunk_size)]
            rows = [process_input(line, keywords=keywords, n=N) for line in lines]
            try:
                X = np.concatenate([X, rows])
                y = np.append(y, [country] * len(rows))
            except NameError:
                X = rows
                y = [country] * len(X)

    return X, y


def get_train_test_sets(filenames, N=2, chunk_size=50):
    X, y = load_datasets(filenames=filenames, N=N, chunk_size=chunk_size)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.1, test_size=0.1, random_state=0, shuffle=True, stratify=y
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test


def train_test_svm(X_train, X_test, y_train, y_test):
    logger.info('Train SVM classifier')

    results = []

    classifier1 = LinearSVC()
    classifier1.fit(X_train, y_train)

    logger.info('Test SVM classifier')

    y_pred = classifier1.predict(X_train)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_train, y_pred, average='weighted')
    results.append(["SVM", 'train', accuracy_score(y_train, y_pred), precision, recall, fscore])

    y_pred = classifier1.predict(X_test)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    results.append(["SVM", 'test', accuracy_score(y_test, y_pred), precision, recall, fscore])

    return pd.DataFrame(results, columns=COLNAMES)


def train_test_knn(X_train, X_test, y_train, y_test):
    logger.info('Train kNN classifier')

    results = []

    classifier2 = KNeighborsClassifier(n_jobs=-1)
    classifier2.fit(X_train, y_train)

    logger.info('Test kNN classifier')

    y_pred = classifier2.predict(X_train)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_train, y_pred, average='weighted')
    results.append(["kNN", 'train', accuracy_score(y_train, y_pred), precision, recall, fscore])

    y_pred = classifier2.predict(X_test)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    results.append(["kNN", 'test', accuracy_score(y_test, y_pred), precision, recall, fscore])

    return pd.DataFrame(results, columns=COLNAMES)


def train_test_decision_tree(X_train, X_test, y_train, y_test):
    logger.info('Train decision tree classifier')

    results = []

    classifier3 = DecisionTreeClassifier(random_state=0)
    classifier3.fit(X_train, y_train)

    logger.info('Test decision tree classifier')

    y_pred = classifier3.predict(X_train)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_train, y_pred, average='weighted')
    results.append(['decision tree', 'train', accuracy_score(y_train, y_pred), precision, recall, fscore])

    y_pred = classifier3.predict(X_test)
    precision, recall, fscore, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    results.append(['decision tree', 'test', accuracy_score(y_test, y_pred), precision, recall, fscore])

    return pd.DataFrame(results, columns=COLNAMES)


if __name__ == "__main__":
    dirpath = os.path.dirname(os.path.realpath(__file__))
    dirpath = os.path.join(dirpath, 'dane')
    filenames = list(os.walk(dirpath))[0][2]

    results_df = pd.DataFrame()

    for N in [1, 2, 3]:
        logger.info(f'Train model based on {N}-grams')
        for chunk_size in [10, 20, 50]:
            logger.info(f'Use texts with {chunk_size} characters')
            X_train, X_test, y_train, y_test = get_train_test_sets(filenames=filenames, N=N, chunk_size=chunk_size)

            results_svm = train_test_svm(X_train, X_test, y_train, y_test)
            results_knn = train_test_knn(X_train, X_test, y_train, y_test)
            results_decision_tree = train_test_decision_tree(X_train, X_test, y_train, y_test)

            results_df_ = pd.concat([results_svm, results_knn, results_decision_tree])
            results_df_['N'], results_df_['chunk_size'] = N, chunk_size

            results_df = pd.concat([results_df, results_df_])

    print(results_df)
    results_df.to_csv(os.path.join(dirpath, '../results.csv'))

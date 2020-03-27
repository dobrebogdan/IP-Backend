#!/usr/bin/python3

import numpy as np
import re
import os.path
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split





class TextClassifier(object):
    
    @staticmethod
    def getNorm():
        return 'l1'
    
    nltk.download('wordnet')
    __lemmatizer = WordNetLemmatizer()
    @staticmethod
    def cleanText(document):
        document = str(document)

        # Remove things like r'\n' r'\t'
        document = re.sub(r'\\\w', ' ', document)

        # Remove all the special characters
        document = re.sub(r'\W', ' ', document)


        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Converting to Lowercase
        document = document.lower()

        # Lemmatization
        document = document.split()

        document = [TextClassifier.__lemmatizer.lemmatize(word) for word in document]
        document = ' '.join(document)

        return document
    
    @staticmethod
    def getBagsOfWords(text_data):
        max_df = 0.80
        min_df = 0.02

        vectorizer = CountVectorizer(strip_accents='ascii', min_df=min_df, max_df=max_df, max_features=1000)
        bow_data = vectorizer.fit_transform(text_data).toarray()

        return bow_data, vectorizer

    @staticmethod
    def normalizeData(feature_data):
        return normalize(feature_data, norm=TextClassifier.getNorm())

    @staticmethod
    def get_tf_idf(feature_data):
        tfidfconverter = TfidfTransformer(smooth_idf=False, norm=TextClassifier.getNorm(), use_idf=True)
        tfidfdata = tfidfconverter.fit_transform(feature_data).toarray()

        return tfidfdata, tfidfconverter

    

    @staticmethod
    def getPickleFilePath(path):
        return os.path.join(path, 'pickle_data.bin')
    
    @staticmethod
    def saveWithPickle(class_object):
        with open(TextClassifier.getPickleFilePath(class_object.data_set_path), 'wb') as pickle_file:
            pickle.dump(class_object, pickle_file)

    @staticmethod
    def loadWithPickle(path):
        with open(path, 'rb') as pickle_file:
            return pickle.load(pickle_file)


    def __getInnerClassifier(self):
        classifier = RandomForestClassifier(n_estimators=1500, random_state=0)
        # classifier = SVC()
        # classifier = LinearSVC()
        
        return classifier

    def __init__(self, data_set_path):
        self.data_set_path = data_set_path

        self.news_data = load_files(data_set_path)
        self.unprocessed_text_data = self.news_data.data
        self.labels = self.news_data.target
        self.labelNames = self.news_data.target_names
        
        self.trainData, self.testData, self.trainLabels, self.testLabels = train_test_split(
            self.unprocessed_text_data, 
            self.labels, 
            test_size=0.15, 
            shuffle=True, 
            random_state=2
        )
        
        self.clean_text_data = []
        for idx in range(0, len(self.trainData)):
            self.clean_text_data.append( TextClassifier.cleanText(self.trainData[idx]) )
            
        self.bow_data, self.countVectorizer = TextClassifier.getBagsOfWords(self.clean_text_data)
        self.tf_idf_data, self.tfidfconverter = TextClassifier.get_tf_idf(self.bow_data)
        
        self.innerClassifier = self.__getInnerClassifier()

        self.innerClassifier.fit(self.tf_idf_data, self.trainLabels)

        junk, predictedLabels = self.predictTexts(self.testData)
        self.testAccuracy = np.average(self.testLabels == predictedLabels)
        print("Created classifier which gave a", self.testAccuracy, "accuracy on the test data")
        
        # clean
        self.news_data = None
        self.unprocessed_text_data = None
        self.labels = None
        self.clean_text_data = None
        self.bow_data = None
        self.tf_idf_data = None
        self.countVectorizer.stop_words_ = None
        
        self.trainData = None
        self.testData = None
        self.trainLabels = None
        self.testLabels = None
    

    @staticmethod
    def getTextClassifier(data_set_path, forceRecompute=False):
        picklePath = TextClassifier.getPickleFilePath(data_set_path)
        if (forceRecompute or os.path.isfile(picklePath) == False):
            tc = TextClassifier(data_set_path)
            TextClassifier.saveWithPickle(tc)
            return tc
        else:
            tc = TextClassifier.loadWithPickle(picklePath)
            print("Loaded a classifier which gave a", tc.testAccuracy, "accuracy on the test data")
            return tc

        
    
    
    # return a list of predictions for the given texts in name and number form. E.g.:
    # ['business', 'tech', 'tech', 'sport'], 
    def predictTexts(self, listOfTexts):
        listOfTexts = listOfTexts.copy()
        for idx in range(0, len(listOfTexts)):
            listOfTexts[idx] = TextClassifier.cleanText(listOfTexts[idx])

        data = self.countVectorizer.transform(listOfTexts)
        data = self.tfidfconverter.transform(data)
        
        predictedLabels = self.innerClassifier.predict(data)
        predictedLabelNames = []
        for idx in range(len(predictedLabels)):
            predictedLabelNames.append( self.labelNames[predictedLabels[idx]].capitalize() )
        
        return predictedLabelNames, predictedLabels

import pandas as pd
import string
import re
import pickle
from pathlib import Path
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB
'''
The Complement Naive Bayes classifier described in Rennie et al. (2003). It was designed
to correct the “severe assumptions” made by the standard Multinomial Naive Bayes classifier.
It is particularly suited for imbalanced data sets. 
https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.ComplementNB.html
'''

from creassessment.controler.constants import DF_COL_PARSER_TOPIC_IDENTIFICATION, DF_COL_PARSER_TOPIC_PROBABILITY, DF_COL_TEXTUAL_CONTENT, NOT_IDENTIFIED

class Topic_Detector:
    topic: dict
    count_vectorizer: CountVectorizer
    classifier: ComplementNB()
    target_category = ['Education', 'Environment and botany', 'Healthy life and sport',
                    'Communication', 'Medicine and health',
                    'Tourism, geography, weather and meteorology', 'Food and drinks',
                    'Finance and work', 'Citizenship and social issues',
                    'Engineering, physics and construction',
                    'Cars, vehicles and transport', 'Productivity',
                    'Animals and pets', 'Entertainment', 'Music', 'Math',
                    'Beauty and fashion', 'Design, painting and photography',
                    'Spirituality, belief and fortune telling', 'Mobile tools',
                    'Robotics, physical computing and automation']

    def __init__(self):
        self.topic = {}
        path_topic_classificator = Path(__file__).parent
        with open(str(path_topic_classificator) + os.sep + 'topic_classificator.pkl', "rb") as dump_file:
            self.count_vectorizer, self.classifier = pickle.load(dump_file)

    def detect_topic(self, df_textual_content_by_component_type: pd.DataFrame) -> dict:
        '''
        Detects the topic of an app and its probability using MultinomialNB
        '''
        try:
            text_to_process = str(df_textual_content_by_component_type[DF_COL_TEXTUAL_CONTENT].values)
            processed_text = self.preprocessing_text(text_to_process)
            text_vect = self.count_vectorizer.transform([processed_text])
            prediction = self.classifier.predict(text_vect)
            topic_pred = self.target_category[prediction[0]]
            proba_pred = self.classifier.predict_proba(text_vect)[0][prediction[0]]
            return {DF_COL_PARSER_TOPIC_IDENTIFICATION: topic_pred, DF_COL_PARSER_TOPIC_PROBABILITY: proba_pred}
        except:
            return {DF_COL_PARSER_TOPIC_IDENTIFICATION: NOT_IDENTIFIED, DF_COL_PARSER_TOPIC_PROBABILITY: 1}

    def preprocessing_text(self, text_to_process) -> str:
        '''
        Remove numbers, \n and punctuation from text_to_process
        '''
        try:
            processed_text = re.sub(r'[0-9]', " ", text_to_process)
            processed_text = re.sub(r'\\n', " ", processed_text)
            processed_text = re.sub(r"[{}]".format(string.punctuation), " ", processed_text) 
            processed_text = processed_text.lower()
            return processed_text
        except:
            return ''
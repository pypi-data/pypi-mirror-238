import pandas as pd
import string
import re
import pickle
from pathlib import Path
import os

#import nltk
#from nltk.tokenize import word_tokenize

#import spacy
#import spacy.cli
#spacy.cli.download("pt_core_news_lg")
#import pt_core_news_lg

import yake

from creassessment.controler.constants import DF_COL_TEXTUAL_CONTENT, DF_COL_PARSER_TAGS, NOT_IDENTIFIED
from creassessment.parser.stop_words import stop_words_apps_pt, stop_words_gen

class Tags_Extractor:
    tags: list
    LANG_GENERIC: str = 'generic'
    LANG_PT: str = 'pt'

    def __init__(self):
        self.tags = ''
#        self.nlp = pt_core_news_lg.load()
        self.nouns = {}
        path_nouns = Path(__file__).parent
        with open(str(path_nouns) + os.sep + 'nouns_set.pickle', "rb") as dump_file:
            self.nouns = pickle.load(dump_file)

    def get_keywords(self, df_textual_content_by_component_type: pd.DataFrame) -> dict:
        '''
        Extracts the tags of an app
        '''
        try:
            text_to_process = str(df_textual_content_by_component_type[DF_COL_TEXTUAL_CONTENT].values)
            processed_text = self.preprocessing_text(text_to_process)
            tags = self.extract_tag(processed_text, lang=self.LANG_GENERIC)
            tags_pos_processed = self.pos_process(tags, lang=self.LANG_GENERIC)
            if len(tags_pos_processed):
                return {DF_COL_PARSER_TAGS: tags_pos_processed}
            else:
                return {DF_COL_PARSER_TAGS: [NOT_IDENTIFIED]}
        except Exception as e:
            print(e)
            return {DF_COL_PARSER_TAGS: [NOT_IDENTIFIED]}

    def preprocessing_text(self, text_to_process: str) -> str:
        '''
        Remove numbers, \n and punctuation from text_to_process
        '''
        try:
            processed_text = re.sub(r'[0-9]', " ", text_to_process)
            processed_text = re.sub(r'\\n', " ", processed_text)
            processed_text = re.sub(r"[{}]".format(string.punctuation), " ", processed_text) 
            tokens = processed_text.split(' ')
            #tokens = nltk.word_tokenize(processed_text, language='portuguese') 
            lower_tokens = [t.lower() for t in tokens]
            alpha_only = [t for t in lower_tokens if t.isalpha()]  #eliminate all non alfabetic tokens (list of strings)
            no_stops = [t for t in alpha_only if t not in stop_words_apps_pt]
            #lemmatization with spacy
            #no_stops_string = ' '.join(no_stops)  #spacy needs string text
            #nlp_no_stops_string = self.nlp(no_stops_string) #preparing input for spacy nlp
            #lemmatized = [t.lemma_.lower() for t in nlp_no_stops_string] #lemma might be Uppercase
            return ' '.join(no_stops)
        except Exception as e:
            print(e)
            return ''
    
    def extract_tag(self, processed_text: str, lang: str) -> list:
        max_ngram_size = 1
        num_of_keywords = 20
        keywords = []
        try:
            if lang == self.LANG_PT:
                custom_kw_extractor = yake.KeywordExtractor(lan=self.LANG_PT, n=max_ngram_size, top=num_of_keywords, stopwords=stop_words_apps_pt)
            if lang == self.LANG_GENERIC:
                custom_kw_extractor = yake.KeywordExtractor(n=max_ngram_size, top=num_of_keywords, stopwords=stop_words_gen)
            keywords = custom_kw_extractor.extract_keywords(processed_text)
            return keywords
        except Exception as e:
            print(e)
            keywords

    def pos_process(self, tags: list, lang: str) -> list:
        keywords_nouns = []
        for tag in tags:
            if lang == self.LANG_PT:
                if tag[0] in self.nouns:
                    keywords_nouns.append((tag[0]))
            if lang == self.LANG_GENERIC:
                keywords_nouns.append((tag[0]))
        if len(keywords_nouns) > 10:
            keywords_nouns = keywords_nouns[:10]
        return keywords_nouns
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 12:46:32 2020

@author: Paras
"""
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import spacy
from tqdm import tqdm
from spacy.matcher import Matcher
import pandas as pd




nlp=spacy.load('en_core_web_sm')



def scrape_text_data():
    url = 'https://thehimalayantimes.com/education/nepali-students-to-get-full-scholarship-in-buddhist-universities-in-myanmar/'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    containers = soup.findAll('div','postDetail mainPost','p')
    for container in containers:
       return (container.text)


def process_for_sentences(scraped_text):
    about_doc = nlp(scraped_text)
    sentences = list(about_doc.sents)
    
    '''for sentence in sentences:
         print(sentence)'''
    return sentences


def export_to_csv(x=process_for_sentences(scrape_text_data())):
    dict={'Sentence':x}
    df=pd.DataFrame(dict)
    df.to_csv('Sentences.csv', index=False)

def improt_data():
    sentences_lists = pd.read_csv('Sentences.csv')
    sentences_lists.shape
    return sentences_lists


def get_entities(sentence):
    entities1=''
    entities2=''
    
    previous_token_dependencies=''
    previous_token_text=''
    
    prefix=''
    modifier=''
    
    for tok in nlp(sentence):
        if tok.dep_!='punct':
            if tok.dep_=='compound':
                prefix=tok.text
                if previous_token_dependencies=='compound':
                    prefix=previous_token_text+ ' '+ tok.text
        
        
        if tok.dep_.endswith('mod')==True:
            modifier=tok.text
            if previous_token_dependencies=='compound':
                modifier=previous_token_text+ ' '+ tok.text
        
        
        if tok.dep_.find('subj')==True:
            entities1= modifier+ ' '+ prefix+ ' '+ tok.text
            prefix=''
            modifier=''
            previous_token_dependencies=''
            previous_token_text=''
            
            
        if tok.dep_.find('obj')==True:
            entities2=modifier+ ' '+ prefix+ ' '+ tok.text
            
        
        previous_token_dependencies=tok.dep_
        previous_token_text=tok.text
        
        
    return([entities1.strip(), entities2.strip()])


def get_relations(sentence):
    doc=nlp(sentence)
    matcher=Matcher(nlp.vocab)
    
    pattern=[
            {'DEP':'ROOT'},
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':'?'},
            {'POS':'ADJ','OP':'?'}
             ]
    
    matcher.add('matching_1',None,pattern)
    
    matches= matcher(doc)
    k=len(matches)-1
    
    span= doc[matches[k][1]:matches[k][2]]
    return(span.text)
    
export_to_csv()
collected_data= improt_data()


entity_pairs=[]
for i in tqdm(collected_data['Sentence'][4:12]):
    entity_pairs.append(get_entities(i))
    
 
relations=[get_relations(x) for x in tqdm(collected_data['Sentence'][4:12])]

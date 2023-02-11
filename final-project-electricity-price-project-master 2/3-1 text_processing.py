from typing import List , Dict , Union
import requests
import pandas as pd
import re
from GoogleNews import GoogleNews
import os


#####  Using Regular Expression & Keywords  & WordCountVector  NLP   ########
us_state_to_abbrev = {
    "Alabama": "AL" ,
    "Alaska": "AK" ,
    "Arizona": "AZ" ,
    "Arkansas": "AR" ,
    "California": "CA" ,
    "Colorado": "CO" ,
    "Connecticut": "CT" ,
    "Delaware": "DE" ,
    "Florida": "FL" ,
    "Georgia": "GA" ,
    "Hawaii": "HI" ,
    "Idaho": "ID" ,
    "Illinois": "IL" ,
    "Indiana": "IN" ,
    "Iowa": "IA" ,
    "Kansas": "KS" ,
    "Kentucky": "KY" ,
    "Louisiana": "LA" ,
    "Maine": "ME" ,
    "Maryland": "MD" ,
    "Massachusetts": "MA" ,
    "Michigan": "MI" ,
    "Minnesota": "MN" ,
    "Mississippi": "MS" ,
    "Missouri": "MO" ,
    "Montana": "MT" ,
    "Nebraska": "NE" ,
    "Nevada": "NV" ,
    "New Hampshire": "NH" ,
    "New Jersey": "NJ" ,
    "New Mexico": "NM" ,
    "New York": "NY" ,
    "North Carolina": "NC" ,
    "North Dakota": "ND" ,
    "Ohio": "OH" ,
    "Oklahoma": "OK" ,
    "Oregon": "OR" ,
    "Pennsylvania": "PA" ,
    "Rhode Island": "RI" ,
    "South Carolina": "SC" ,
    "South Dakota": "SD" ,
    "Tennessee": "TN" ,
    "Texas": "TX" ,
    "Utah": "UT" ,
    "Vermont": "VT" ,
    "Virginia": "VA" ,
    "Washington": "WA" ,
    "West Virginia": "WV" ,
    "Wisconsin": "WI" ,
    "Wyoming": "WY" ,
    "District of Columbia": "DC" ,
    "American Samoa": "AS" ,
    "Guam": "GU" ,
    "Northern Mariana Islands": "MP" ,
    "Puerto Rico": "PR" ,
    "United States Minor Outlying Islands": "UM" ,
    "U.S. Virgin Islands": "VI" ,
    "The U.S": "US" ,
    "U.S.": "US" ,
    "the United states": "US" ,
    "us market": "US" ,
    "us energy market": "US"
}


def get_us_state_expression():
    """
    to get the only US related articles from the google news.
    """

    us_state = list(us_state_to_abbrev.keys())
    us_state.extend(list(us_state_to_abbrev.values()))
    us_state = list(set(us_state))
    us_state = [state.replace(" " , "[ ]?") for state in us_state]
    return rf"[ ]?({'|'.join(us_state)})[ ]?"


def get_keywordset_expression(keyword_set: List[str]):
    
    k_set = [keyword.replace(" " , "[ ]?") for keyword in keyword_set]
    return rf"[ ]?({'|'.join(k_set)})[ ]?"


def chg_lowercase(item_list: List[str]):
    return [item.lower() for item in item_list]


def get_google_news(start_date: str , end_date: str) -> Dict:
    gn: GoogleNews = GoogleNews(lang='en' , region='US' , start='01/01/2011',end='12/31/2021')
    gn.get_news(key='coal OR natural gas OR electricity price')
    result = gn.result()

    # save google news as original
    data = pd.DataFrame(data=result , columns=['title' , 'desc' , 'date' , 'datetime' , 'link' , 'media' , 'site'])
    data.to_csv(path_or_buf='news.csv' , encoding='utf-8' , index=True)

    return result


def crawling_in_news_content(article: Dict) -> str:
    article_in_content: str = ""
    title_search: List[str] = re.findall(pattern=get_us_state_expression() , string=article['title'])  # regular expression case sentive
    if title_search is not None and len(title_search) > 0:  # if the title contains coal, price, gas, increase then get that entile articles
        if article['link'] not in ['https://' , 'http://']:
            article['link'] = f"https://{article['link']}"

        #  get the article from google (page using redirect so we need to use allow_redirects=True )
        try:
            response: requests.models.Response = requests.get(url=article['link'] , allow_redirects=True , timeout=15)
            if response.status_code == 200:
                article_in_content = response.text.strip()

        except requests.exceptions.ReadTimeout:
            pass

    return article_in_content


def article_prediction_score(article_in_content: str):
    """
	making the function which can tell how many aritlces contain the keywords.
	"""
    ret: bool = False

    ############################ 1. text processing using set keywords ################################
    # creating the 3 sets to get the articles 
    keyword_set: Dict[str , List[str]] = {
        "set1": ["Coal" , "electricity" , "price"] ,
        "set2": ["natural gas" , "electricity" , "price"] ,
        "set3": ["coal" , "natural gas" , "electricity" , "price"]
    }

    # there are so many articles so we want to get the articles which used sets key word아래 코드는 기사 본문 내용을 키워드 세트로 사용할 때 쓰는 코드에요
    for i , (keyword_name , keyword_list) in enumerate(keyword_set.items()):
        keyword_set_expression: str = get_keywordset_expression(keyword_set=keyword_list)
        try:
            keyword_set: List[str] = re.findall(pattern=keyword_set_expression , string=article_in_content , flags=re.I)  # regular expression case insentive
            if keyword_set is not None and len(keyword_set) > 0:  # coal, price, gas, increase와 관련된 단어가 기사 제목 내 존재하면, 기사 본문 내용을 크롤링 해온다.
                keyword_set: List[str] = chg_lowercase(item_list=keyword_set)
                keyword_set: List[str] = list(set(keyword_set))

                if len(keyword_set) == len(keyword_list):
                    ret = True
                    return ret

        except ValueError as ex:
            print("substring not found")
    ############################ 1. end of using keywords ################################



def parse_news_item(article_list: List[Dict]) -> Dict[str , Union[List , int]]:
    """
	making a nlp fuciontion for the each aricles from get_google_news 
   nlp_article_score_structure will give the aricles which fall into our keywords   
	"""
    # save each articles  based one the  WordCountVector 
    nlp_article_score_structure: Dict[str , Union[List , int]] = {
        'article_count': 0 ,
        'items': [] ,
        'total_site': len(article_list) ,
    }

    for (i , article) in enumerate(article_list):
        article_in_content: str = crawling_in_news_content(article=article)

        if article_in_content != '':  # and len(article_in_content) > 0 and not article_in_content.startswith(''):
            significant_article: bool = article_prediction_score(article_in_content=article_in_content)

            if significant_article:
                # word counts 
                nlp_article_score_structure['items'].append(article)
                nlp_article_score_structure['article_count'] += 1

    print(nlp_article_score_structure)
    return nlp_article_score_structure


def output_verify_article(nlp_article_score_structure: Dict[str , Union[List , int]] , filename: str):
    """
    save as csv file 
    """
    ret: bool = False
    output = pd.DataFrame(data=nlp_article_score_structure['items'] , columns=['title' , 'desc' , 'date' , 'datetime' , 'link' , 'media' , 'site'])
    if output.size > 0:
        output.to_csv(path_or_buf=filename , encoding='utf-8' , index=True)
        ret = True

    return ret

####### this is main function that we used. get the news  from google 
## using  a function called : parse_news_item . Get the article and body using text processing
	
if __name__ == '__main__':
    news_list: List[Dict] = get_google_news(start_date="01/01/2011" , end_date="12/31/2021")
    nlp_article_score_structure: Dict[str , Union[List , int]] = parse_news_item(article_list=news_list)
    if output_verify_article(nlp_article_score_structure=nlp_article_score_structure , filename='news_classification.csv'):
        print("sucussfully print the all the article ")

    else:
        print("fail to print csv file ")
        
        
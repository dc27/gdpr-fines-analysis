from os import name
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

def scrape_url(url, user_agent_path='data/user_agent.json'):
    """
    Scrapes a given url using BeautifulSoup
        
        Parameters:
            url (str): web url
            user_agent_path (str): local path to user agent information
    
        Returns:
            soup
    """

    with open(user_agent_path) as json_file:
        header = json.load(json_file)

    response = requests.get(url, headers=header)

    soup = BeautifulSoup(response.text, features='html.parser')
    return soup

def scrape_fines():
    """
    Scrapes https://www.privacyaffairs.com/ for latest info on GDPR violations
    
        Returns:
            None
    """

    base = 'https://www.privacyaffairs.com/'
    route = 'gdpr-fines/'
    full_url =  base + route

    soup = scrape_url(full_url)

    # get all script tags
    all_scripts = soup.find_all('script')

    # script with req info is in position 7 (I don't know why, that's just where it is apparently)
        
    info_script = all_scripts[5]

    # start of each list is location of [
    # end of each list is location of ]
    starts = [m.start() for m in re.finditer(r'\[', info_script.text)]
    ends = [m.end() for m in re.finditer(r'\]', info_script.text)]

    formatted_info = []
    # loop through each group of start and end points.
    # check the lengths of start points and end points. If they are unequal
    # use the shorter for the range of the loop. 
    if len(starts) <= len(ends):
        for i in range(len(starts)):
            formatted_info.append(
                json.loads(info_script.text[starts[i]:ends[i]])
                )
    else:
        for i in range(len(ends)):
            formatted_info.append(
                json.loads(info_script.text[starts[i]:ends[i]])
                )

    # pattern to extract everything in between html tags:
    pat = r'(?<=\>)(.+?)(?=\<)'

    # apply pattern to each string in each list.
    for i in range(len(formatted_info)):
        for j in range(len(formatted_info[i])):
            s = formatted_info[i][j]['summary']
            match = re.search(pat, s)
            formatted_info[i][j]['summary'] = match.group(1)

    # data = {
    #     'allItems':formatted_info[0],
    #     'allItemsPriceGrouped':formatted_info[1]
    # }
    
    return formatted_info[0]

    # with open('data/scraped_fines.json', 'w', encoding='utf-8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

def save_fines_data(fines_json, filepath, file_format='csv'):
    """
    Writes scraped data to file.

            Parameters:
                    fines_json (dict): A json-style dictionary
                    filepath (str): Path to save the file to
                    file_format (str): Desired file format to write to. Either 'csv' or 'json'

            Returns:
                    None
    """

    match file_format:
        case 'csv':
            pd.json_normalize(fines_json).to_csv(filepath, index=False)
        case 'json':
            with open(filepath, 'r', encoding='utf-8') as f:
                json.dump(fines_json, f, ensure_ascii=False, indent=4)
        case _:
            raise ValueError(f"{file_format} not supported. Use 'csv' or 'json'")
            
    pass
    
    
    
def scrape_article_text():

    url = 'https://gdpr-info.eu/'

    soup = scrape_url(url)

    links = soup.find_all(name='table')

    anchors = [table.find_all('a') for table in soup.find_all('table')][0]
    

    all_articles = {}
    # loop through anchors
    
    for anchor in anchors:
        if len(anchor.get_text()) > 8:
            current_chap = anchor.get_text()
            all_articles[current_chap] = {}
            all_articles[current_chap]['title'] = anchor.get('data-title')
            all_articles[current_chap]['link'] = anchor.get('href')
            all_articles[current_chap]['articles'] = {}
        elif len(anchor.get_text()) < 4:
            current_art = anchor.get_text()
            all_articles[current_chap]['articles'][current_art] = {}
            all_articles[current_chap]['articles'][current_art]['title'] = anchor.get('data-title')
            link = anchor.get('href')
            art_soup = scrape_url(link)
            try:
                art_text = art_soup.find('div', {'class': 'entry-content'}).find('ol').get_text()
            except:
                art_text = art_soup.find('div', {'class': 'entry-content'}).find('p').get_text()
            all_articles[current_chap]['articles'][current_art]['link'] = link
            all_articles[current_chap]['articles'][current_art]['text'] = art_text

    all_articles

    with open('data/scraped_art_text.json', 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    pass

def get_gdpr_article_text():
    """
    get's article text from tidytuesday github.
    
    Downloads tsv file, which tidytuesday created after scraping gdpr website.
    Saves as csv
    """
    # no need to scrape individual articles; it has already been done:
    # visit: https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-04-21

    url='https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-04-21/gdpr_text.tsv'

    article_text = pd.read_csv(url, sep='\t')

    article_text.to_csv('data/gdpr_article_text.csv', index=False)
    
    pass

def main():
    # uncomment to update article text:
    scraped_fines = scrape_fines()
    save_fines_data(scraped_fines, 'data/scraped_fines.csv', file_format='csv')
    # scrape_article_text()
    

if __name__ == '__main__':
    main()
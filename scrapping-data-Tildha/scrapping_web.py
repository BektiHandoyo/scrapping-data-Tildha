from bs4 import BeautifulSoup
import lxml

def get_content_from_page(webpage) :
    soup = BeautifulSoup(webpage, 'lxml')

    targetted_element = ''

    halosehat_element = soup.select('div[data-url]')
    # print(halosehat_element) 
    if len(halosehat_element) != 0 :
        for item in halosehat_element :
            targetted_element += item.text + "\n"
    else :
        text_element = soup.find_all('p')
        if len(text_element) == 0 :
            raise ValueError("Cannot read information from the page")
        for item in soup.find_all('p') :
            targetted_element += item.text + "\n" 
        
    return targetted_element

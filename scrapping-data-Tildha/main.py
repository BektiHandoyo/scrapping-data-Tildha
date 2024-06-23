import requests, random, json
import google.generativeai as genai
from scrapping_web import *
from scrapping_pdf import *

genai.configure(api_key="AIzaSyBJ6Sql-WBSfEtxA9UN8Wc4OicqGLnlNxg")
model = genai.GenerativeModel('gemini-1.5-flash')

def download_page_from_url(webpage_url) :
    
    user_agent_list = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:127.0) Gecko/20100101 Firefox/127.0',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    ]

    try :
        response = requests.get(webpage_url, stream=True, headers={'User-Agent' : random.choice(user_agent_list)})
        if 'pdf' in response.headers.get('Content-Type') :
            with open('downloaded.pdf', 'wb') as download_file :
                for chunck in response.iter_content(2000) :
                    download_file.write(chunck)
            return "pdf"
        
        if 'html' in response.headers.get('Content-Type') :
            with open('downloaded.html', 'wb') as download_file :
                for chunck in response.iter_content(2000) :
                    download_file.write(chunck)
            return "html"
    except Exception as e:
        print(e)
        return "error"
    
def format_information_to_json(text) :
    prompt = """
                Read the following text. Then, create json from it with this following format (Attention ! ignore all commercial and offers aspects from a particular product, company or agency)
                [
                    {
                        request : "{question that may be answered by important information in the text}", 
                        response : "{important information contained in the text that can answer the question (No Formatting Plase!!!)}"
                    } 
                ] :\n
            """
    try :
        response = model.generate_content(prompt + text)
        print("successfully format the information ")
        return response.text.replace('```json\n', "").replace('\n```', "")
    except ValueError as ve:
        print('Something Went wrong, error : ' + str(ve) )
        print(response)
        return "error"

if __name__ == "__main__" :
    with open('list_url', 'r', encoding="utf-8") as f :
        webpages = [url.replace(" ", "") for url in f.read().strip().split("\n")]

    datasets = []

    for webpage_url in webpages :
        content = ''
        webpage = download_page_from_url(webpage_url)
        if(webpage == 'html') :
            with open('downloaded.html', 'r', encoding='utf-8') as f : 
                content = get_content_from_page(f.read())
        elif(webpage == "pdf") :
            convert_pdf_to_image()
            content = get_pdf_content()
            summarized_content = summarize_pdf_content(content)

        json_data = json.loads(format_information_to_json(content))
        for data in json_data :
            datasets.append(data)
        
    with open('dataset.json', 'w', encoding="utf-8") as f :
        json.dump(datasets, indent=4, fp=f)
    
    os.remove('downloaded.html')
    os.remove('downloaded.pdf')
    
    for filename in os.listdir('tmp-pdf') :
        os.remove(f"tmp-pdf/{filename}")
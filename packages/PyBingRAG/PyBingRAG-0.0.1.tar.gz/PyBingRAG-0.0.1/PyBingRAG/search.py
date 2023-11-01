# The BingSearch class is used to perform web scraping on Bing search results.
import os
import requests
from bs4 import BeautifulSoup
from langchain.llms import HuggingFaceEndpoint, HuggingFaceHub, HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

class BingSearch:

    def __init__(self, query):
        """
        The function initializes an object with a query parameter.
        
        :param query: The query parameter is a string that represents a query or question that the code
        is trying to address or answer
        """
        self.query = query
    
    def get_results(self, num, max_lines):
        """
        The function `get_results` retrieves search results from Bing based on a given query and returns
        the content of the web pages up to a specified maximum number of lines.
        
        :param num: The `num` parameter is the number of search results you want to retrieve. It
        determines how many search results will be returned in the `content_list`
        :param max_lines: The `max_lines` parameter specifies the maximum number of lines of content to
        retrieve from each URL
        :return: a list of content.
        """
        
        self.num = num
        self.max_lines = max_lines
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        
        try:
            bing_url = "https://www.bing.com/search?&q=" + self.query.lower()
            result = requests.get(url=bing_url, headers=headers)
            soup = BeautifulSoup(result.text, 'html.parser')
            a_tags = soup.find_all('a', {"class": "b_widePag sb_bp"})
            a_pages = [bing_url] + ["https://www.bing.com" + a['href'] for a in a_tags]
            pg_url_list = []
            content_list = []

            for pg in a_pages:
                res = requests.get(url=pg, headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                a_url_tags = soup.find_all('a', {"class": "tilk"})
                a_url_tags = [a['href'] for a in a_url_tags]
                for u in a_url_tags:
                    pg_url_list.append(u)
            i = 0
            for url_ in a_url_tags:
                content_list.append(self.get_content(url_, self.max_lines))
                if i == self.num:
                    break
                i = i + 1
            return content_list
        
        except Exception as e:
            return str(e)
    
    def get_content(self, url, max_lines):
        """
        The function `get_content` takes a URL and a maximum number of lines as input, retrieves the
        content from the URL, and returns a dictionary containing the URL, title, and a truncated
        version of the content.
        
        :param url: The URL of the webpage you want to scrape the content from
        :param max_lines: The `max_lines` parameter is the maximum number of lines of content that you
        want to retrieve from the webpage
        :return: a dictionary object `u_dict` containing the following keys:
        - 'url': the input URL
        - 'title': the title of the webpage
        - 'content': a string containing the concatenated text of the first `max_lines` paragraphs on
        the webpage, separated by periods ('.')
        """
        
        self.url = url    
        self.max_lines = max_lines
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        
        try:
            u_dict = {}
            r = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            p_tags = soup.find_all('p')
            p_text = []
            for p in p_tags:
                if len(p.text) > 20:
                    p_text.append(p.text)
            
            u_dict['url'] = self.url
            u_dict['title'] = soup.title.text
            u_dict['content'] = ('.').join(p_text[:self.max_lines])

            return u_dict
        
        except Exception as e:
            return str(e)
    
    def rag_output(self, promptquery, n_lines, hf_key):
        """
        The `rag_output` function takes a prompt query, number of lines, and Hugging Face API key as inputs,
        and generates a response using a language model from the Hugging Face model hub.
        
        :param promptquery: The `promptquery` parameter is a string that represents the additional query or
        prompt that you want to add to the original question. It will be appended to the `question` variable
        before generating the output
        :param n_lines: The `n_lines` parameter represents the number of lines of text you want to generate
        as output. It determines how many times the loop will run to generate additional text
        :param hf_key: The `hf_key` parameter is the Hugging Face API token. It is used to authenticate and
        access the Hugging Face models and resources. You need to provide a valid API token in order to use
        the Hugging Face models in your code
        :return: The function `rag_output` returns a string that consists of the question followed by the
        generated text from the language model.
        """
        
        self.promptquery = promptquery
        self.n_lines = n_lines
        self.hf_key = hf_key
        
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = self.hf_key
        question = self.query + " " + self.promptquery
        
        try:
            template = """{question}"""
            prompt = PromptTemplate(template=template, input_variables=["question"])
            repo_id = "tiiuae/falcon-7b"
            llm = HuggingFaceHub(
                repo_id=repo_id, model_kwargs={"temperature": 0.7, "top-k": 50, "top-p":.85, "min_new_tokens": 1024, "max_len": 64}
            )
            llm_chain = LLMChain(prompt=prompt, llm=llm)

            for i in range(self.n_lines):
                prompt = PromptTemplate(template=template, input_variables=["question"])
                llm_chain = LLMChain(prompt=prompt, llm=llm)
                text = llm_chain.run(question)
                template = str(template) + str(text)
                
            return question + '.' + template
        
        except Exception as e:
            return str(e)
            

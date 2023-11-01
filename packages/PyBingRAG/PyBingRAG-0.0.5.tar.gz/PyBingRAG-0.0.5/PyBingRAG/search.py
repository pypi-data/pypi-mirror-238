# The BingSearch class is used to perform web scraping on Bing search results.
import os
import requests
import numpy as np
from bs4 import BeautifulSoup
from langchain.llms import HuggingFaceEndpoint, HuggingFaceHub, HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings import HuggingFaceEmbeddings

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
    
    def rag_init(self, query, bingresults):
        """
        The `rag_init` function takes a query and a list of Bing search results, calculates embeddings for
        the text results and the query using HuggingFaceEmbeddings, computes the cosine similarity between
        each text result and the query, and returns the text result with the highest cosine similarity.
        
        :param query: The query parameter is a string that represents the search query or question for which
        you want to find the most relevant result
        :param bingresults: The `bingresults` parameter is a list of dictionaries. Each dictionary
        represents a search result from Bing and contains information about the search result, such as the
        title, URL, and content of the search result
        :return: The function `rag_init` returns the text result from `bingresults` that has the highest
        cosine similarity with the embedded query.
        """
        
        self.query = query
        self.bingresults = bingresults
        embeddings = HuggingFaceEmbeddings()
        

        text_results = [x['content'] for x in self.bingresults]
        text_embeds = np.array(embeddings.embed_documents(text_results))
        q_embed = np.array(embeddings.embed_documents([self.query]))
        q_cosine = []
        for t in text_embeds:
            q_cosine.append(cosine_similarity(t.reshape(1, q_embed.shape[1]), q_embed))

        return text_results[q_cosine.index(max(q_cosine))]
    
    def rag_output(self, promptquery, n_iters, bingresults, hf_key):
        """
        The `rag_output` function takes in a prompt query, number of iterations, Bing search results,
        and Hugging Face API key. It initializes the RAG model, generates a question based on the prompt
        query and Bing search results, and uses the RAG model to generate a response. It repeats this
        process for the specified number of iterations and returns the final question and response.
        
        :param promptquery: The promptquery parameter is a string that represents the initial query or
        prompt for the model. It is the input that the model will use to generate the desired output
        :param n_iters: The `n_iters` parameter specifies the number of iterations or loops to run the
        RAG model. Each iteration generates additional text based on the previous output, allowing the
        model to provide more detailed and comprehensive responses
        :param bingresults: The `bingresults` parameter is used to pass the search results obtained from
        the Bing search engine. It is likely used as input to the `rag_init` function, which initializes
        the RAG (Retrieval-Augmented Generation) model. The specific implementation of `rag_init` is not
        provided
        :param hf_key: The `hf_key` parameter is the Hugging Face API key. It is used to authenticate
        and access the Hugging Face models and resources
        :return: The function `rag_output` returns a string that consists of the original question
        followed by the generated text from the language model.
        """
        
        self.promptquery = promptquery
        self.bingresults = bingresults
        self.n_iters = n_iters
        self.hf_key = hf_key
        
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = self.hf_key
        
        rag_input = self.rag_init(self.promptquery, self.bingresults)
        question = self.promptquery + " Here is the requested information: " + rag_input
        
        try:
            template = """{question}"""
            prompt = PromptTemplate(template=template, input_variables=["question"])
            repo_id = "tiiuae/falcon-7b"
            llm = HuggingFaceHub(
                repo_id=repo_id, model_kwargs={"temperature": 0.7, "top-k": 50, "top-p":.85, "min_new_tokens": 1024, "max_len": 64}
            )
            llm_chain = LLMChain(prompt=prompt, llm=llm)

            for i in range(self.n_iters):
                prompt = PromptTemplate(template=template, input_variables=["question"])
                llm_chain = LLMChain(prompt=prompt, llm=llm)
                text = llm_chain.run(question)
                template = str(template) + str(text)
                
            return question + ' . ' + template
        
        except Exception as e:
            return str(e)

from langchain.tools import Tool, DuckDuckGoSearchResults
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import requests
from bs4 import BeautifulSoup
from model import llm

def web_search(topic: str) -> str:
    headers = {"Ocp-Apim-Subscription-Key": "13835b8353af4f31959388f1494c29eb"}
    params = {"q": topic, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    ans = ""
    if 'webPages' in search_results and 'value' in search_results['webPages']:
        for i in search_results['webPages']['value']:
            ans = ans + i['snippet'] + "\n"
    return ans

w_search = Tool(
        name="Search",
        func=web_search,
        description="useful for when you need to search about latest information about an entity"
    )

ddg=DuckDuckGoSearchResults()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
}

def parse_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    text_content_with_links = soup.get_text()
    return text_content_with_links

def fetch_web_page(url):
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)

web_fetch_tool = Tool.from_function(
    func=fetch_web_page,
    name="WebFetcher",
    description="Fetches the content of a web page"
)

prompt_template = "Summarize the following content: {content}"

llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

summarize_tool = Tool.from_function(
    func=llm_chain.run,
    name="Summarizer",
    description="Summarizes a web page"
)

tools = [w_search, web_fetch_tool, summarize_tool]
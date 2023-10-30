# modified fetch function with semaphore
import asyncio
from aiohttp import ClientSession
import aiohttp
import requests
from datetime import datetime


uva_news_database_api_url = 'https://api-us1.cludo.com/api/v3/10000068/10001442/search'
batch_size = 250

header = {
  "Accept": "application/json",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "en-US,en;q=0.9",
  "Authorization": "SiteKey MTAwMDAwNjg6MTAwMDE0NDI6U2VhcmNoS2V5",
  "Cache-Control": "no-cache",
  "Origin": "https://news.virginia.edu",
  "Pragma": "no-cache",
  "Referer": "https://news.virginia.edu/",
  "Sec-Fetch-Dest": "empty",
  "Sec-Fetch-Mode": "cors",
  "Sec-Fetch-Site": "cross-site",
  "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\""
}

def request_body_generator_config(**kwargs):
  def generator(page, perPage):
    request_body = {
     "ResponseType":"JsonObject", 
     "Template":"SearchContent",
     "facets": {},
     "filters":{},
     "page": 1,
     "sort": {
          "Date": "desc"
     },
     "query": '*',
     "text":"",
     "perPage": batch_size,
     "traits":[],
     "rangeFacets":{},
     "enableRelatedSearches": "false",
     "applyMultiLevelFacets": "false"
    }
    for key, item in kwargs.items():
      request_body[key] = item
    request_body['page'] = page
    request_body['perPage'] = perPage
    return request_body
  return generator



def get_num_documents_in_query(request_body_creator):
   request_body = request_body_creator(1,1)
   response = requests.post(url=uva_news_database_api_url, json=request_body,headers=header)
   response_as_dict = response.json()
   return int(response_as_dict['TotalDocument'])

async def post_requests(num_articles, request_body_creator):
  request_bodies = __generate_request_bodies(num_articles,request_body_creator)

  #redundancy
  sem = asyncio.Semaphore(1000)

  async with ClientSession(connector=aiohttp.TCPConnector(limit=1000),trust_env=True) as session:
    tasks = [asyncio.ensure_future(__post(session, sem,request_body)) for request_body in request_bodies]
    responses = await asyncio.gather(*tasks)
  
  #flatten
  responses = [article for response in responses for article in response]
  built_articles = []

  for count, article in enumerate(responses):
     if count >= num_articles:
        break
     built_articles.append(__parse_document(article))
  
  return built_articles
        
async def __post(session, semaphore, request_body):
   async with semaphore, session.post(url=uva_news_database_api_url, json=request_body,headers=header) as response:
        response = await response.json()
        return response["TypedDocuments"]
   
#generates batches for async requests
def __generate_request_bodies(num_articles, request_body_creator):
  #there is a bug in cludo's api where trying to get more than 10,000 items from a query leads to a bug
  if num_articles > 10000:
    current_year = int(datetime.now().year)
    request_bodies = []
    for year in range(current_year+1,2006,-1):
       request_body = request_body_creator(1,5000)
       request_body['facets'] = {"NewsCategory":[],"Year":[f'{year}']}
       request_bodies.append(request_body)
  else:
    num_partitions = num_articles // batch_size if num_articles % batch_size == 0 else num_articles // batch_size + 1
    request_bodies = [request_body_creator(page+1, batch_size)for page in range(num_partitions)]
  return request_bodies

#author either in author field or in description/values[3]
def __parse_document(document):
  doc_fields = document['Fields']
  parsed_document = {}
  try:
    parsed_document['title'] = doc_fields['Title']['Value']
  except:
    parsed_document['title'] = 'n/a'
  if 'Author' in doc_fields:
    parsed_document['author'] = doc_fields['Author']['Value']
  else:
    parsed_document['author'] = 'n/a'
    """try:
      string_containing_author = doc_fields['Description']['Values'][3]
      string_containing_author.replace('\n',)
      last_author_character = string_containing_author.index(',')
      author = string_containing_author[30:last_author_character]
      
    except:
       author = 'n/a'"""
  try:
    parsed_document['date'] = doc_fields['Updated_date']['Value']
  except:
    parsed_document['date'] = 'n/a'
  try:
    parsed_document['url'] = doc_fields['Url']['Value']
  except:
    parsed_document['url'] = 'n/a'
  try:
    parsed_document['text'] = doc_fields['Description']['Value']
  except:
    parsed_document['text'] = 'n/a'
  try:
    parsed_document['category'] = doc_fields['NewsCategory']['Value']
  except:
    parsed_document['category'] = 'n/a'
  try:
    parsed_document['description'] = doc_fields['MetaDescription']['Value']
  except:
    parsed_document['description'] = 'n/a'

  return parsed_document

def convert_to_iso8601(input_string):
    input_format = "%m/%d/%Y %I:%M:%S %p"
    dt_object = datetime.strptime(input_string, input_format)
    iso8601_string = dt_object.isoformat()
    return iso8601_string

def format_api_output(list_of_articles):
  formatted_output = {
    "apiResults": list_of_articles
  }
  return formatted_output


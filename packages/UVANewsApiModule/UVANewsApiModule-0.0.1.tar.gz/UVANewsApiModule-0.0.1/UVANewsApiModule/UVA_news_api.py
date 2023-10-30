import api_utility as u

async def get_query(query):
  request_body_generator = u.request_body_generator_config(query=query)
  num_docs = u.get_num_documents_in_query(request_body_generator)
  articles =  await u.post_requests(num_docs,request_body_generator)
  return u.format_api_output(articles)
 
async def get_recent(num_articles):
   request_body_generator = u.request_body_generator_config(query='*')
   articles =  await u.post_requests(num_articles,request_body_generator)
   return u.format_api_output(articles)

#returns every article up until the one with the given url
async def update(url):
  api_response = await get_by_url(url)
  date = api_response["apiResults"][0]['date']
  iso_date = u.convert_to_iso8601(date)
  config = {
     "query": '*',
     'filters': {
       'date': ['Updated_date',iso_date,""]
    }
  }
  request_body_generator = u.request_body_generator_config(**config)
  num_docs = u.get_num_documents_in_query(request_body_generator)
  articles = await u.post_requests(num_docs,request_body_generator)
  return u.format_api_output(articles[:-1])

#returns multiple
async def get_by_author(author):
  config = {
    'query': author,
    "operator": "and"
  }
  request_body_generator = u.request_body_generator_config(**config)
  num_docs = u.get_num_documents_in_query(request_body_generator)
  articles =  await u.post_requests(num_docs,request_body_generator)
  return u.format_api_output(articles)
   
#returns article with the corresponding url
async def get_by_url(url):
  config = {
     'query': '*',
     'filters': {
      'Url': [url]
    }
  }
  request_body_generator = u.request_body_generator_config(**config)
  built_articles = await u.post_requests(1,request_body_generator)
  return u.format_api_output(built_articles)

#gets best matching based on name
async def get_by_name(name):
   request_body_generator = u.request_body_generator_config(query=name)
   articles =  await u.post_requests(1,request_body_generator)
   return u.format_api_output(articles)
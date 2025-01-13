from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

#import sys
#sys.path.append('..')


from Index_Query_Text import createIndex, IndexQuery, IndexText
from FlagEmbedding import FlagModel
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

model = None
client = None
index_search = None
index_text = None

# executes the code before the yield at startup, 
# and the code after the yield at shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):

	global model, client, index_search, index_text

	# load the embedding model
	model = FlagModel('BAAI/bge-small-zh-v1.5', use_fp16 = True)

	# load Elasticsearch client
	client = AsyncElasticsearch("http://elasticsearch:9200")

	# instantiate IndexText and IndexQuery objects
	index_text = IndexText(client, model)
	index_search = IndexQuery(client, model)

	yield

	model = None
	await client.close()


app = FastAPI(lifespan = lifespan)


#declaring data models
class IndexQueryRequest(BaseModel):

	index_name : str
	query : list[str]
	text_path : str

	# chunk parameters
	sentence_limit : int
	chunk_limit : int
	min_characters : int

class Hit(BaseModel):

	score: float
	chunk : str

class IndexQueryResponse(BaseModel):

	knn_res : list[Hit]

@app.get("/status", response_model = dict[str, str])
async def health_check():

	return {"working" : "yes"}

# creates the index and indexes the text
@app.post("/index", response_model = dict[str, str])
async def create_index(request: IndexQueryRequest):

	name = request.index_name
	path_to_text = request.text_path

	sentence_limit = request.sentence_limit
	chunk_limit = request.chunk_limit
	min_characters = request.min_characters

	createIndex(client, name)

	res = await index_text.chunkEmbedIndex(path_to_text, name, sentence_limit, chunk_limit, min_characters)

	# return {"index_exists": "True"}

# answers queries
@app.post("/search", response_model = IndexQueryResponse)
async def answer_query(request: IndexQueryRequest):

	query = request.query
	index = request.index_name

	res = await index_search.knnSearch(index, query)

	return {"knn_res": res}

# curl -X POST "http://0.0.0.0:80/search" -d '{"query" : ["how old is the bishop when he dies?"], "index_name" : "les_miserables_index"}' -H "content-type:application/json" | python3 -m json.tool















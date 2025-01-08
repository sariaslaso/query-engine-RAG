from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

#import sys
#sys.path.append('..')


from Index_Query_Text import IndexQuery
from FlagEmbedding import FlagModel
from elasticsearch import AsyncElasticsearch

model = None
client = None

# executes the code before the yield at startup, 
# and the code after the yield at shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
	# load the embedding model
	model = FlagModel('BAAI/bge-small-zh-v1.5', use_fp16 = True)
	# load Elasticsearch client
	client = AsyncElasticsearch("http://elasticsearch:9200")
	yield
	model = None
	await client.close()


app = FastAPI(lifespan = lifespan)

index_search = IndexQuery(client)

#declaring data models
class IndexQueryRequest(BaseModel):

	index_name : str
	query : list[str]

class Hit(BaseModel):

	score: float
	chunk : str

class IndexQueryResponse(BaseModel):

	knn_res : list[Hit]

@app.get("/status", response_model = dict[str, str])
async def health_check():

	return {"working" : "yes"}

@app.post("/index_post", response_model = IndexQueryResponse)
async def answer_query(request: IndexQueryRequest):

	query = request.query
	index = request.index_name

	res = index_search.knnSearch(index, query)

	return {"knn_search": res}














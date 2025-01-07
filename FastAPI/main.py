from fastapi import FastAPI
from pydantic import BaseModel

#import sys
#sys.path.append('..')

from Index_Query_Text import IndexQuery

from FlagEmbedding import FlagModel
model = FlagModel('BAAI/bge-small-zh-v1.5', use_fp16 = True)

from elasticsearch import Elasticsearch
client = Elasticsearch("http://elasticsearch:9200")

app = FastAPI()


text_queries = IndexQuery(client)

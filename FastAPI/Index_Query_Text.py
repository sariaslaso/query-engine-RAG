import spacy
from FlagEmbedding import FlagModel
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from tqdm import tqdm

# helper functions

def remove_newline(text):
# removes newline characters, "\n", from text
# text: list of paragraphs in the text
    
    for i in range(len(text)):
        text[i] = " ".join(text[i].split())

    return text

def embed_index_text(text_chunks, client, model):
    # chunks: list of m elements that contain n sentences each
    # client: instance of Elasticsearch client used to create the index

    # embed chunks
    chunk_embeddings = model.encode(text_chunks).tolist()

    # define the format of the data to be indexed as pairs (chunk of text, chunk embeddings)
    docs = [
        {
            '_op_type': 'index',
            '_index': 'les_miserables_index',
            '_source': {
                "chunk" : t, 
                "embedding_vector" : v
            }
        } for t, v in zip(text_chunks, chunk_embeddings)
    ]
    
    # index in bulk
    res = helpers.bulk(client, docs)
    # print(res)

def createIndex(client, index_name):
    # client: instance of Elasticsearch client
    # index_name (str): index name

    # ensure that there is no previously defined index under the index_name
    if (client.indices.exists(index = index_name)):
        client.indices.delete(index = index_name)

    # define the format of index: chunk of text and embedding vectors
    # custom mapping that defines the expected types of indices features
    # define mapping parameters for the "chunk" and "embedding_vector" fields
    # define "vector_dim"
    mappings = {
        "properties": {
            "chunk": {
                "type": "text"
            }, 
            "embedding_vector": {
                "index": True, 
                "type": "dense_vector", 
                "dims": 512, 
                "similarity": "cosine",
            }
        }
    }
        
    # create index
    client.indices.create(index = index_name, mappings = mappings)



class IndexText:
# class methods: 
    # __preProcessInput: reads a text from a file_path, and splits the text into paragraphs eliminating newline characters
    # chunkEmbedIndex: splits the pre-processed text into chunks and indexes the chunks using Elasticsearch
    
    def __init__(self, client, model):
        # instance variables defined below
        
        # elastic search client
        self.client = client
        # embedding model
        self.model = model

    def __preProcessInput(self, file_path):
        # text: text file

        with(open(file_path, "r")) as text_file:
            text = text_file.read()

        # split text in paragraphs
        text = text.split("\n\n")

        # using the helper function "remove_newline" to eliminate "\n" characters from the text
        text = remove_newline(text)

        return text

    def chunkEmbedIndex(self, file_path, sentence_limit, chunk_limit, min_characters):
        text = self.__preProcessInput(file_path)
        
        # Load pretrained English Language Model to separate the text into sentences
        nlp = spacy.load('en_core_web_sm') 

        chunks = []
        sentences = []

        # generate doc pipeline with nlp
        # allows to process the data as a stream and buffer the paragraphs in batches instead of one by one
        doc_pipeline = nlp.pipe(text, batch_size = 5, n_process = 1)

        # split the doc into sentences and create chunks that contain at least n = "sentence_limit" sentences
        # once m = "chunk_limit" chunks have been collected, create chunk embeddings and index them
        for doc in tqdm(doc_pipeline):
            for sent in doc.sents:
                sentences.append(sent.text)

                if len(sentences) >= sentence_limit:
                    chunk = " ".join(sentences)

                    # if the number of characters in the current chunk is less than the minimum required, 
                    # then add another sentence and count again before embedding the text
                    if len(chunk) < min_characters:
                        continue

                    # once the chunk has the minimum length, append it to chunks
                    chunks.append(chunk)
                    # remove the first sentence and keep the other two to overlap with the following sentence
                    sentences = sentences[1:]

                if len(chunks) == chunk_limit:
                    # embed and index
                    embed_index_text(chunks, self.client, self.model)

                    # clear list of chunks
                    chunks = []

        # if there are sentences/chunks that haven't been embedded and indexed, do so
        if len(sentences) != 0:
            # append sentences to remaining chunks
            chunks.append(" ".join(sentences))

            embed_index_text(chunks, self.client)

            sentences = []
            chunks = []
            

class IndexQuery:

    def __init__(self, client, model):
        # Python client for Elasticsearch
        self.client = client
        self.model = model

    def __embedQueries(self, queries):
        # queries: list of text queries
        # returns a list of vector embeddings for each query 
        q_embeddings = self.model.encode_queries(queries)

        return q_embeddings.tolist()[0]

    async def knnSearch(self, index_name, queries):
        # index_name: str
        # queries: list of text queries
        
        query_vector = self.__embedQueries(queries)
        score_chunk = []
        
        resp_knn = await self.client.search(
            index = index_name,
            # size = 3,  # number of top global results after combining shard results
            query = {
                "knn": {
                    "field": "embedding_vector",
                    "query_vector": query_vector,
                    "k": 10,  # nearest neighbours to return from each shard
                    "num_candidates": 100,  # number of nearest neighbor candidates to consider per shard while doing knn search
                }
            },
        )

        # return scores and chunks as tuples in a list
        
        for hit in resp_knn["hits"]["hits"]:
            score_chunk.append({"score": hit["_score"], "chunk": hit["_source"]["chunk"]})
            # score_chunk.append((hit["_score"], hit["_source"]["chunk"]))
            # print(hit["_score"], hit["_source"]["chunk"])
            # print()

        return score_chunk

# query-engine-RAG

A query engine that uses Retrieval Augmented Generation (RAG) to assist LLMs in answering questions about a text. The RAG approach improves the performance of a LLMs by providing relevant context to a user query. This is achieved by retrieving content from a database that satisfies some similarity threshold with the query.

## How the app works

The user provides an input text and a query about this text to the user interface (UI). The text is read, processed, and split into sentences using the spaCy trained pipeline [en_core_web_sm](https://spacy.io/models/en), an English pipeline trained on written web text, in order to preserve the semantics. The spaCy pipeline allows to process the text as a stream and buffer the paragraphs in batches. A [FlagEmbedding model](https://huggingface.co/BAAI/bge-small-zh-v1.5) is used to create vector embeddings of the text in batches of n text chunks that contain a preset number of sentences each. The vector embeddings are indexed and stored in a vector database in pairs along with the corresponding chunks of text using the Python client for Elasticsearch. Similarly, the user query is embedded and indexed in the vector database alongside with vector embeddings of the text.

A k-nearest neighbour (kNN) search is implemented in Elasticsearch in order to retrieve the top-k relevant content results from the vector database by computing the cosine-similarity between the query and the text embeddings. The retrieved relevant content and query are passed as a prompt to an LLM in order to answer the user's question.


```mermaid
flowchart LR
	User -- InputText --> InputData 
	User -- Query --> InputData

	subgraph UI
		direction TB
		InputData
	end
	InputData -- Text --> id1(Split in chunks)
	InputData -- Query --> id2([Embedding Model])
	InputData -- Query --> id9
	
	subgraph RAG
		direction TB
		subgraph Text
			direction TB
			id1 --> id3([Embedding Model])
			id3 --> id5@{shape: hex, label: "Vector embedding (text)"}
		end

		id5 -- index --> id7[(Vector_DB)]
		id7 -- knn_Elasticsearch <br/> fetch relevant content --> id9@{shape: docs, label: "Query + Content"}

		subgraph Query
			direction TB
			id2 --> id4@{shape: hex, label: "Vector embedding (query)"}
		end

		id4 -- index --> id7
	end

	id9 --> id10((LLM))
	id10 --> id11(Response)
	id11 --> User

```









Extended description coming soon!

# query-engine-RAG

A query engine that uses Retrieval Augmented Generation (RAG) to answer questions about a text.

```mermaid
flowchart LR
	id1(Text document) --> id2([Embedding Model]);
	id2 --> id3@{ shape: hex, label: "Text Embeddings"};
	id3 --> id4[(Vector DB)];
	id5(Query) --> id6([Embedding Model]);
	id6 --> id7@{ shape: hex, label: "Query Embeddings"};
	id7 --> id4;
	id4 -- knn search --> id8@{ shape: docs, label: "Query + Context"};
	id8 --> id9@{ shape: circle, label: "LLM"};
	id9 --> id10(Response);
```


```mermaid
flowchart LR
	User -- InputText --> InputData 
	User -- Query --> InputData
	subgraph UI
		InputData
	end
	InputData -- Text --> Split
	InputData -- Query --> Embed_query

	subgraph RAG
		direction TB
		subgraph Text
			direction TB
			Split --> Embed_chunks --> Index
		end
		subgraph Query
			direction TB
			Embed_query --> Search
		end
	end
```

Extended description coming soon!

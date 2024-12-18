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

	id9 --> id10@{shape: circle, label: "LLM"}
	id10 --> id11(Response)
	id11 --> User

```

Extended description coming soon!

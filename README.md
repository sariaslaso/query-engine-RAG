# query-engine-RAG

A query engine that uses Retrieval Augmented Generation (RAG) to answer questions about a text.

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

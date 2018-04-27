# InfoRetProject

####################################################################

Topic: Query-biased Multi-Document Abstractive Summarisation

Authors: Amrit Singhal and Akshat Jindal

####################################################################

This is the implementation of all parts of the pipeline that we have proposed in our report for the project, which can be found in the repo.

## Pre-requisites

1. PyLucene
2. NLTK
3. Tensorflow
## Creating Data Required

1. Download the CNN news dataset from [here](https://cs.nyu.edu/%7Ekcho/DMQA/).Only the stories are required. Keep it in some directory which will act as your < data_directory >.
2. For generating query strings, run the following commands :
```
	python QueryLDA/CreateQueries.py
```
In the code for CreateQueries.py, set the the `directory` variable on
line 73 as your <data_directory>. This creates a `Queries.txt` file in
the `QueryLDA` directory.
```
	python QueryLDA/TopicGen.py
```
This creates `LDA_500.pickle` in the `QueryLDA` directory. We have
provided the file already for direct use. This file has 50 queries, each
representing a different topic.
## Usage

1. Build the index for the corpus. 
```
	./buildIndex <data_directory>
```

2. Run the extractive summarisation process:
```
	./QueryMultiDocSummarisation <Query_string> <paragraph_extraction_type> 
```

#### Paragraph_extraction_type

| Parameter_Type | Extraction_Process | 
|---|---|
| 1 | TextTiling |
| 2 | Vector Space Method |
| 3 | TfIdf Method |
| 4 | Luhn Clusters |
| 5 | Query Biased LSA |

3. This will create a file `RelevantDoc.txt` in the main directory of the repo. This is the SuperDoc mentioned in the report. 

4. Following this, we need to perform abstractive summarisation on this SuperDoc. The model we chose was the pointer-generator networks, the implementation for which can be found [here](https://github.com/abisee/pointer-generator).

## Samples
The `Samples` directory has a sample input query, the `SuperDoc` for it
and the final Abstractive summary for it.

## Future Works

We aim to improve upon the abstractive part also, by adding a query bias to it. 

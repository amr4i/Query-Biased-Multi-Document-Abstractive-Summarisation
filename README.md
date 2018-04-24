# InfoRetProject

####################################################################

Topic: Query-biased Multi-Document Abstractive Summarisation
Authors: Amrit Singhal and Akshat Jindal

####################################################################

This is the implementation of all parts of the pipeline that we have proposed in our report for the project, which can be found [here](http://home.iitk.ac.in/~amrits/InfoRet_Report.pdf).

## Pre-requisites

1. PyLucene
2. NLTK
3. Tensorflow

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

## Future Works

We aim to improve upon the abstractive part also, by adding a query bias to it. 
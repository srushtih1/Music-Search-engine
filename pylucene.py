import logging, sys
logging.disable(sys.maxsize)

import lucene
import time
import os
import json
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity

f = open('scraped_songs.json')
sample_doc = json.load(f)

def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    artistType = FieldType()
    artistType.setStored(True)
    artistType.setTokenized(False)

    lyricsType = FieldType()
    lyricsType.setStored(True)
    lyricsType.setTokenized(True)
    lyricsType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    for sample in sample_doc:
        artist = sample['artist']
        lyrics = sample['lyrics_by']

        doc = Document()
        doc.add(Field('Artist', str(artist), artistType))
        doc.add(Field('Lyrics', str(lyrics), lyricsType))
        writer.addDocument(doc)
    writer.close()

    #for calculation of runtime of lucene index creation process
    # start_time = time.time()
    # i = 0
    # for sample in sample_doc:
    #     #do something
    #     doc = Document()
    #     i+=1
    #     if(i%100==0):
    #         t = time.time() - start_time
    #         print("%s seconds",(t))

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    
    parser = QueryParser('Lyrics', StandardAnalyzer())
    parsed_query = parser.parse(query)
    print(parsed_query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "Artist": doc.get("Artist"),
            "lyrics": doc.get("Lyrics")
        })
    
    print(topkdocs)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index('sample_lucene_index/')
u_input = input("Enter a query: ")
retrieve('sample_lucene_index/', u_input)







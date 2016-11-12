import whoosh.index as index
from whoosh.fields import Schema, ID, TEXT
from whoosh.index import create_in, open_dir
from whoosh.query import Term, SpanNear

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')



def create_index(texts, indexPath = "index"):
    schema = Schema(content=TEXT(stored=True),nid=ID(stored=True))

    if not os.path.exists(indexPath):
        os.mkdir(indexPath)

    index = create_in(indexPath, schema)

    writer = index.writer()

    for i in range(len(texts)):
        writer.add_document(content=texts[i],nid=unicode(i))
    writer.commit()
#create_index(texts)
 

# PMI
def pmi(searcher, w1, w2,epsilon=0.1, window=10):
    doc_count=float(searcher.doc_count())
    t1 = query.Term("content", term1)
    t2 = query.Term("content", term2)  
    
    
    pw1=float(len(searcher.search(t1)))/doc_count
    pw2=float(len(searcher.search(t2)))/doc_count    

    pocc= float(len(searcher.search(SpanNear(t1, t2, slop=window))))/doc_count 
    
    return math.log((pocc+epsilon)/pw1*pw2,2)
    
#NPMI
def npmi(searcher, w1, w2,epsilon=0.1, window=10):
    doc_count=float(searcher.doc_count())
    t1 = query.Term("content", term1)
    t2 = query.Term("content", term2) 
    pocc= float(len(searcher.search(SpanNear(t1, t2, slop=window))))/doc_count 
    pmi_w1w2=pmi(searcher, w1, w2,epsilon, window)
    return pmi_w1w2 / (- math.log(pocc+epsilon))
    
#UCI
def coherence_uci(searcher, topic_words,epsilon=0.1, window=10):
    somme=0
    N=len(topic_words)
    for i in range(N):
        for j in range(i+1,N):
            somme+=pmi(search,topic_words[i], topic_words[j],epsilon, window)
    return (somme*3)/(N*(N-1))
            
#U_NPMI
def coherence_npmi(searcher, topic_words,epsilon=0.1, window=10):
    somme=0
    N=len(topic_words)
    for i in range(N):
        for j in range(i+1,N):
            somme+=npmi(search,topic_words[i], topic_words[j],epsilon, window)
    return (somme*3)/(N*(N-1))

#UMASS
def coherence_umass(searcher,topic_words,epsilon=0.1):
    somme=0
    N=len(topic_words)
    doc_count=float(searcher.doc_count())
    
    for i in range(1,N):
        for j in range(0,i-1):
    
            t1 = query.Term("content", topic_words[i])
            t2 = query.Term("content", topic_words[j]) 
            pocc= float(len(searcher.search(And(t1,t2))))/doc_count 
                        
            pwj=float(len(searcher.search(t2)))/doc_count
            
            somme+=math.log((pocc+epsilon)/pwj,2)
    return (somme*2)/(N*(N-1))

#compute p(k|w)
def marginal_k_w(doc_dist_topic_k,infolength,word_proba_topic_k):
    return word_proba_topic_k*sum([a*b for a,b in zip(doc_dist_topic_k,infolength)])

#compute entropy en w
def entropy(topic_doc_dist,infolength,topic_dist_word_w)
    #compute entropy for word w
    entropy_w=0
    for k in range(len(topic_doc_dist)):
        entropy_w+=marginal_k_w(topic_doc_dist[k],infolength,topic_dist_word_w[k])  
    return entropy_w

# Relevance
def relevance(word,topic_id,topic_doc_dist,infolength, topic_dist_word_w):
    # divide p(w|k) by entropy
    entropy_w=entropy(topic_doc_dist,infolength,topic_dist_word_w)
    return topic_dist_word_w(topic_id)/entropy_w
    
# PMI average
def pmi_average(searcher,topic_words)
    pmi_average=[]
    for i in range(len(topic_words)):
        w1=topic_words[i]
        avg=0
        for j in range(len(topic_words)):
            if i!=j:
                w2=topic_words[j]
                avg+=pmi(searcher, w1, w2,epsilon=0.1, window=10)
        pmi_average.append(avg/(len(topic_words)-1))
    return pmi_average
                

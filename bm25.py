# BM25Index implementation
import math
from collections import Counter
from typing import Callable, Optional, Any, List, Dict, Tuple
import re

# BM25Index class
class BM25Index:
    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        tokenizer: Optional[Callable[[str], List[str]]] = None,
    ):
        self.documents: List[Dict[str, Any]] = []
        self._corpus_tokens: List[List[str]] = []
        self._doc_len: List[int] = []
        self._doc_freqs: Dict[str, int] = {}
        self._avg_doc_len: float = 0.0
        self._idf: Dict[str, float] = {}
        self._index_built: bool = False

        self.k1 = k1
        self.b = b
        self._tokenizer = tokenizer if tokenizer else self._default_tokenizer

    # default tokenizer
    def _default_tokenizer(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.split(r"\W+", text)
        return [token for token in tokens if token]
    

    # update the statistics of the corpus
    def _update_stats_add(self, doc_tokens: List[str]):
        # update the document length
        self._doc_len.append(len(doc_tokens))

        # update the document frequency of the tokens
        seen_in_doc = set()

        for token in doc_tokens:
            if token not in seen_in_doc:
                self._doc_freqs[token] = self._doc_freqs.get(token, 0) + 1
                seen_in_doc.add(token)

        self._index_built = False

    # add a document to the index
    def add_document(self, document: Dict[str, Any]):
        # check if the document is a dictionary
        if not isinstance(document, dict):
            raise TypeError("Document must be a dictionary.")

        # check if the document contains a 'content' key
        if "content" not in document:
            raise ValueError(
                "Document dictionary must contain a 'content' key."
            )

        # get the content of the document
        content = document.get("content", "")

        # check if the content is a string
        if not isinstance(content, str):
            raise TypeError("Document 'content' must be a string.")

        # tokenize the content
        doc_tokens = self._tokenizer(content)

        # add the document to the index 
        self.documents.append(document)

        # add the tokens to the corpus
        self._corpus_tokens.append(doc_tokens)

        # update the statistics of the corpus
        self._update_stats_add(doc_tokens)

     # calculate the idf
    def _calculate_idf(self):
        # get the number of documents
        N = len(self.documents)

        # initialize the idf dictionary
        self._idf = {}

        for term, freq in self._doc_freqs.items():
            idf_score = math.log(
                ((N - freq + 0.5) / (freq + 0.5)) + 1
            )

            self._idf[term] = idf_score

    # build the index
    def _build_index(self):
        if not self.documents:
            self._avg_doc_len = 0
            self._idf = {}
            self._index_built = True
            return
        
        self._avg_doc_len = sum(self._doc_len) / len(self._doc_len)
        self._calculate_idf()
        self._index_built = True

    def _compute_bm25_score(self, query_tokens:List[str], doc_index: int) -> float:
        score = 0.0

        doc_term_counts = Counter(self._corpus_tokens[doc_index])

        doc_length = self._doc_len[doc_index]

        for token in query_tokens:
            if token not in self._idf:
                continue

            idf = self._idf[token]
            term_freq = doc_term_counts.get(token, 0)

            numerator = idf * (self.k1 + 1) * term_freq

            denominator = term_freq + self.k1 * (1 - self.b + self.b * doc_length / self._avg_doc_len)
            score += numerator / (denominator + 1e-9)

        return score


# store = BM25Index()

# print(store._default_tokenizer("INC-2023-Q4-011"))

# store = BM25Index()

# store._update_stats_add(["database", "database", "timeout"])

# print(store._doc_len)
# print(store._doc_freqs)


# store = BM25Index()

# store.add_document({
#     "content": "database database timeout"
# })

# store.add_document({
#     "content": "database error"
# })

# print(store.documents)
# print(store._corpus_tokens)
# print(store._doc_len)
# print(store._doc_freqs)


store = BM25Index()

store.add_document({
    "content": "database database timeout"
})

store.add_document({
    "content": "security incident"
})

store._build_index()

query_tokens = ["database"]

# score = store._compute_bm25_score(query_tokens, 0)

# print(score)


# score = store._compute_bm25_score(query_tokens, 1)

# print(score)
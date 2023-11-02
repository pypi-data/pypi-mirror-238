
class QueryRequest(BaseModel):
    collection_name: str
    queries: List[QueryWithEmbedding]


class QueryResponse(BaseModel):
    # The results are sorted by the score in the descending order
    results: List[QueryResult]


class Query(BaseModel):
    # where supports SQL =, <, >, <=, >=, !=, and, or, etc.
    where: Optional[str] = None
    return_metas: Optional[List[str]] = None
    return_embedding: Optional[bool] = False
    top_k: Optional[int] = 3


class QueryWithEmbedding(Query):
    embedding: List[float]


class QueryResult(BaseModel):
    vectors: List[VectorWithScore]

class VectorWithScore(Vector):
    score: float

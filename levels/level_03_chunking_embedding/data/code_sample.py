class SearchService:
    def search(self, question: str) -> list[str]:
        return ["chunk_persistent_client_001", "chunk_metadata_filter_001"]

    def rag(self, question: str) -> dict[str, object]:
        chunks = self.search(question)
        return {"answer": "context から回答します", "sources": chunks}


def normalize_query(question: str) -> str:
    return question.strip().lower()

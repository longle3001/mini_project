from qdrant_client import QdrantClient

from .settings import settings

CLIENT_QRANT = None


def init_qrant_connection():
    global CLIENT_QRANT
    CLIENT_QRANT = QdrantUtils.init_qrandt()


class QdrantUtils:
    @staticmethod
    def init_qrandt() -> QdrantClient:
        try:
            client = QdrantClient(
                url=f"http://{settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
            )
            client.set_model(settings.QDRANT_MODEL)
        except Exception as exc:
            print(f"Error: {exc}")
        return client

    @staticmethod
    def add_to_collection(collection_name, document, meta):
        result = ""
        if not CLIENT_QRANT:
            init_qrant_connection()
        if CLIENT_QRANT:
            ids = CLIENT_QRANT.add(
                collection_name=collection_name,
                documents=document,
                metadata=meta,
            )
            result = ids[0]
        return result

    @staticmethod
    def query_qdrant(collection_name, text):
        result = None
        if not CLIENT_QRANT:
            init_qrant_connection()
        if CLIENT_QRANT:
            result = CLIENT_QRANT.query(
                collection_name=collection_name,
                query_text=text,
                score_threshold=settings.SCORE_THRESHOLD,
            )
            if result:
                result = _get_filename_and_score(result)
        return result


def _get_filename_and_score(records):
    result = []
    for record in records:
        result.append({"filename": record.metadata["filename"], "score": record.score})
    return result

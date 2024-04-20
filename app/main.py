from fastapi import FastAPI, HTTPException, UploadFile
from utils.pg_integrate import add_record, search_organisation_id, setup_database
from utils.qrant_integrate import QdrantUtils, init_qrant_connection
from utils.response_model import (
    Document,
    DocumentList,
    EmbeddingSearchResponse,
    EmbeddingSearchResponseList,
)

app = FastAPI(
    on_startup=[
        init_qrant_connection,
        setup_database,
    ],
)


@app.post("/embeddings/")
async def create_embeddings(file: UploadFile, project: str, organisation_id: str):
    try:
        if not file.filename.endswith(".txt"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only .txt files are accepted.",
            )

        content = await file.read()  # Read the file content
        content = content.decode("utf-8")  # Assuming the file content is in UTF-8
        meta = [
            {
                "filename": file.filename,
                "content": content,
                "type": ".txt",
                "project": project,
                "organisation_id": organisation_id,
            }
        ]
        embedding_id = QdrantUtils.add_to_collection(
            collection_name="demo-1", document=[content], meta=meta
        )
        if embedding_id:
            add_record(
                filename=file.filename,
                content=content,
                type="txt",
                project=project,
                organisation_id=organisation_id,
                embedding_id=embedding_id,
            )
        else:
            return {"status_code": 500, "reason": "cannot add to qrantdb"}
        return {"status_code": 200}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error \n{exc}")


@app.get("/embeddings/by-organisation-id/{organisation_id}")
async def get_embeddings(organisation_id: str):
    try:
        document_data = search_organisation_id(organisation_id)
        if document_data:
            fields = [
                "filename",
                "content",
                "type",
                "project",
                "organisation_id",
                "embedding_id",
            ]
            documents_list = DocumentList(
                documents=[Document(**dict(zip(fields, doc))) for doc in document_data]
            )
            return documents_list
        else:
            return {"response": "not found"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error \n{exc}")


@app.post("/embeddings/search")
async def search_embeddings(query: str, type: str = ".txt"):
    if type != ".txt":
        return HTTPException(status_code=500, detail='type must be ".txt"')
    try:
        response = QdrantUtils.query_qdrant("demo-1", query)
        if response:
            documents_list = EmbeddingSearchResponseList(
                documents=[
                    EmbeddingSearchResponse(
                        filename=doc.get("filename"), score=str(doc.get("score"))
                    )
                    for doc in response
                ]
            )
            return documents_list
        else:
            return {"response": "not found"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal server error \n{exc}")
    return {"query": query, "type": type}

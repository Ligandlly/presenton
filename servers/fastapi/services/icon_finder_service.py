import asyncio
import json
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2


class IconFinderService:
    def __init__(self):
        self.collection_name = "icons"
        self.client = chromadb.PersistentClient(
            path="chroma", settings=Settings(anonymized_telemetry=False)
        )
        self._initialized = False
        print("IconFinderService instantiated (lazy init on first use)")

    def _ensure_initialized(self):
        if not self._initialized:
            self._initialize_icons_collection()
            self._initialized = True

    def _initialize_icons_collection(self):
        import os
        # Use pre-downloaded model from /app/chroma/models (built into Docker image)
        # Fall back to runtime download if model doesn't exist (for non-Docker deployments)
        default_model_path = "/app/chroma/models"
        runtime_model_path = "chroma/models"

        # Check if pre-downloaded model exists in Docker image
        if os.path.exists(default_model_path) and os.listdir(default_model_path):
            self.embedding_function = ONNXMiniLM_L6_V2()
            self.embedding_function.DOWNLOAD_PATH = default_model_path
            print(f"Using pre-downloaded ONNX model from {default_model_path}")
        else:
            # Fallback: download at runtime (requires network)
            self.embedding_function = ONNXMiniLM_L6_V2()
            self.embedding_function.DOWNLOAD_PATH = runtime_model_path
            self.embedding_function._download_model_if_not_exists()
            print("ONNX model not found in Docker image, downloading at runtime...")
        try:
            self.collection = self.client.get_collection(
                self.collection_name, embedding_function=self.embedding_function
            )
        except Exception:
            with open("assets/icons.json", "r") as f:
                icons = json.load(f)

            documents = []
            ids = []

            for i, each in enumerate(icons["icons"]):
                if each["name"].split("-")[-1] == "bold":
                    doc_text = f"{each['name']} {each['tags']}"
                    documents.append(doc_text)
                    ids.append(each["name"])

            if documents:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function,
                    metadata={"hnsw:space": "cosine"},
                )
                self.collection.add(documents=documents, ids=ids)

    async def search_icons(self, query: str, k: int = 1):
        self._ensure_initialized()
        result = await asyncio.to_thread(
            self.collection.query,
            query_texts=[query],
            n_results=k,
        )
        return [f"/static/icons/bold/{each}.svg" for each in result["ids"][0]]


ICON_FINDER_SERVICE = IconFinderService()

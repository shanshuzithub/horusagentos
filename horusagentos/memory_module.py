# tech.md: 4.4. Memory Layer
import time
import json  # For serializing complex data if stored as text
# Potential future imports: faiss, sentence_transformers, sqlite3, psycopg2


class MemoryModule:
    def __init__(self, config: dict = None):
        self.config = config if config else {}
        # e.g., sqlite, faiss, weaviate
        self.db_type = self.config.get('db_type', 'mock')
        self.db_path = self.config.get(
            'path', './horus_memory.db')  # For file-based DBs

        self.vector_db = self._initialize_vector_db()
        self.embedding_model = self._initialize_embedding_model()
        self.structured_db = self._initialize_structured_db()
        print(
            f"MemoryModule initialized (type: {self.db_type}, path: {self.db_path})")

    def _initialize_vector_db(self):
        print(
            f"Mock: Vector DB initialized ({self.config.get('vector_db_config', 'default vector config')})")
        # Placeholder for FAISS, Annoy, Pinecone, Weaviate, etc.
        # Example: import faiss; self.index = faiss.IndexFlatL2(embedding_dim); return self.index
        # Mock in-memory vector store
        return {"data": [], "index_type": "mock_flat_L2"}

    def _initialize_embedding_model(self):
        print(
            f"Mock: Embedding model initialized ({self.config.get('embedding_model_name', 'default_sbert')})")
        # Placeholder for Sentence Transformers or other embedding models
        # Example: from sentence_transformers import SentenceTransformer; return SentenceTransformer('all-MiniLM-L6-v2')
        return "MockEmbeddingModel"

    def _get_embedding(self, text: str) -> list:
        # Mock embedding generation
        print(f"Memory: Generating mock embedding for text: '{text[:30]}...'")
        # In a real scenario: return self.embedding_model.encode(text).tolist()
        # Simple mock
        return [hash(word) * 0.00001 for word in text.split()[:5]]

    def _initialize_structured_db(self):
        print(
            f"Mock: Structured DB initialized ({self.db_type} at {self.db_path})")
        # Placeholder for SQLite or PostgreSQL connection
        # Example: import sqlite3; conn = sqlite3.connect(self.db_path); self._create_tables(conn); return conn
        # Mock in-memory structured store
        return {"experiences": [], "errors": []}

    def _create_tables(self, conn):  # Example for SQLite
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            instruction TEXT,
            plan TEXT,       -- JSON string
            results TEXT,    -- JSON string
            reflections TEXT,
            instruction_embedding BLOB -- For vector DBs this might be just an ID
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            instruction TEXT,
            plan TEXT,        -- JSON string
            error_details TEXT -- JSON string
        )
        """)
        conn.commit()

    def record_experience(self, instruction: str, plan: list, execution_results: dict, reflections: str = None, timestamp: float = None):
        """Records a task execution experience."""
        ts = timestamp if timestamp else time.time()
        print(
            f"Memory: Recording experience at {ts} for instruction: '{instruction}'")

        instruction_embedding = self._get_embedding(instruction)

        # For mock structured_db (list of dicts)
        experience_entry = {
            "id": len(self.structured_db["experiences"]) + 1,
            "timestamp": ts,
            "instruction": instruction,
            "plan": json.dumps(plan),  # Serialize plan to JSON string
            # Serialize results to JSON string
            "results": json.dumps(execution_results),
            "reflections": reflections,
            # Store mock embedding directly for simplicity
            "instruction_embedding_mock": instruction_embedding
        }
        self.structured_db["experiences"].append(experience_entry)

        # For mock vector_db (also list of dicts, with ID linking to structured_db)
        # In a real vector DB, you'd add the embedding and its ID.
        self.vector_db["data"].append(
            {"id": experience_entry["id"], "embedding": instruction_embedding})
        print(f"Memory: Experience {experience_entry['id']} recorded.")

    def retrieve_relevant_experience(self, query_instruction: str, top_k: int = 3) -> list:
        """Retrieves relevant past experiences based on similarity."""
        print(
            f"Memory: Retrieving {top_k} relevant experiences for query: '{query_instruction}'")
        query_embedding = self._get_embedding(query_instruction)

        # Mock similarity search (e.g., simple dot product or L2 distance if embeddings were real)
        # For this mock, we'll just return the last few experiences if the query matches anything.
        if not self.vector_db["data"]:
            return []

        # Extremely simplified mock search: finds if any word matches, not actual vector similarity
        relevant_ids = []
        for entry in reversed(self.structured_db["experiences"]):
            if query_instruction.lower().split()[0] in entry["instruction"].lower():
                relevant_ids.append(entry["id"])
            if len(relevant_ids) >= top_k:
                break

        retrieved_experiences = [
            exp for exp in self.structured_db["experiences"] if exp["id"] in relevant_ids]
        print(f"Memory: Retrieved {len(retrieved_experiences)} experiences.")
        return retrieved_experiences

    def summarize_and_generalize_experiences(self, experiences: list):
        """Analyzes experiences to extract generalizable knowledge."""
        print(
            f"Memory: Summarizing/generalizing {len(experiences)} experiences.")
        if not experiences:
            return {"summary": "No experiences to summarize.", "patterns": []}
        # Mock summarization
        return {"summary": f"Mock summary of {len(experiences)} experiences.", "patterns": ["common_action: click_button"]}

    def update_memory_strategy(self):
        """Periodically optimizes and prunes outdated memories."""
        print("Memory: Updating memory strategy (mock: no operation performed).")
        # Placeholder for logic like removing old/unused memories, re-indexing, etc.
        pass

    def record_error(self, instruction: str, plan: list = None, error_details: dict = None, timestamp: float = None):
        """Records errors encountered during task execution."""
        ts = timestamp if timestamp else time.time()
        print(
            f"Memory: Recording error at {ts} for instruction: '{instruction}', details: {error_details}")
        error_entry = {
            "id": len(self.structured_db["errors"]) + 1,
            "timestamp": ts,
            "instruction": instruction,
            "plan": json.dumps(plan) if plan else None,
            "error_details": json.dumps(error_details) if error_details else None
        }
        self.structured_db["errors"].append(error_entry)
        print(f"Memory: Error {error_entry['id']} recorded.")


if __name__ == '__main__':
    print("Testing MemoryModule...")
    config = {'db_type': 'mock_sqlite', 'path': './test_horus_memory.db'}
    memory = MemoryModule(config=config)

    # Record some experiences
    memory.record_experience(
        "Open Chrome and search for HorusAgentOS",
        [{"action": "open_app", "params": {"app_name": "Chrome"}}, {
            "action": "type_text", "params": {"text": "HorusAgentOS"}}],
        {"summary": "Search completed", "results": ["link1", "link2"]},
        reflections="Initial search was successful."
    )
    memory.record_experience(
        "Open Notepad and write a note",
        [{"action": "open_app", "params": {"app_name": "Notepad"}}, {
            "action": "type_text", "params": {"text": "Test note"}}],
        {"summary": "Note written"},
        reflections="Notepad interaction smooth."
    )
    memory.record_error(
        "Failed to open Firefox",
        [{"action": "open_app", "params": {"app_name": "Firefox"}}],
        {"error_code": "APP_NOT_FOUND",
            "message": "Firefox application could not be located."}
    )

    # Retrieve experiences
    relevant_exp = memory.retrieve_relevant_experience(
        "search for something else")
    print(
        f"Retrieved relevant experiences for 'search for something else': {len(relevant_exp)}")
    for exp in relevant_exp:
        print(f"  - ID: {exp['id']}, Instr: {exp['instruction']}")

    relevant_exp_open = memory.retrieve_relevant_experience(
        "Open an application")
    print(
        f"Retrieved relevant experiences for 'Open an application': {len(relevant_exp_open)}")
    for exp in relevant_exp_open:
        print(f"  - ID: {exp['id']}, Instr: {exp['instruction']}")

    print(f"Total experiences: {len(memory.structured_db['experiences'])}")
    print(f"Total errors: {len(memory.structured_db['errors'])}")

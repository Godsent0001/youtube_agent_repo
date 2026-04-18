from app.db.session import (
    users_collection,
    agents_collection,
    videos_collection,
    metrics_collection,
    campaigns_collection
)

# =========================
# BASE DATABASE ACCESS LAYER
# =========================

class BaseRepository:
    """
    Generic MongoDB repository (reusable CRUD layer)
    """

    def __init__(self, collection):
        self.collection = collection

    # CREATE
    def create(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    # READ ONE
    def find_one(self, query: dict):
        return self.collection.find_one(query)

    # READ MANY
    def find_many(self, query: dict):
        return list(self.collection.find(query))

    # UPDATE
    def update(self, query: dict, update_data: dict):
        result = self.collection.update_one(
            query,
            {"$set": update_data}
        )
        return result.modified_count

    # DELETE
    def delete(self, query: dict):
        result = self.collection.delete_one(query)
        return result.deleted_count
# app/Utils/serializer.py
class Serializer:

    @staticmethod
    def serialize(doc) -> dict:
        # mode="json" makes Pydantic serialize ObjectId → str automatically
        data = doc.model_dump(mode="json")
        data["id"] = str(doc.id)
        return data

    @staticmethod
    def serialize_many(docs: list) -> list:
        return [Serializer.serialize(doc) for doc in docs]
from bson.objectid import ObjectId
from server import connect
from server.databases.chapter import *

novel_collection = connect.novel_collection


def novel_helper(novel) -> dict:
    return {
        "id": str(novel["_id"]),
        "title": novel["title"],
        "description": novel["description"] if "description" in novel else "",
        "genres": novel["genres"],
        "image_url": novel["image_url"],
        "banner_url": novel["banner_url"],
        "chapter": novel["chapter"],
        "views": novel["views"],
        "chapter": novel["chapter"],
        "tags": novel["tags"],
        "rating": novel["rating"],
        "year": novel["year"],
        "created_at": novel["created_at"],
        "updated_at": novel["updated_at"],
        "created_by": novel["created_by"],
        "updated_by": novel["updated_by"],
    }

# Retrieve all novels present in the database


async def retrieve_novels():
    novels = []
    async for novel in novel_collection.find():
        novels.append(novel_helper(novel))
    return novels

# Add a new novel into to the database


async def add_novel(novel_data: dict) -> dict:
    novel = await novel_collection.insert_one(novel_data)
    new_novel = await novel_collection.find_one({"_id": novel.inserted_id})
    return novel_helper(new_novel)

# Retrieve a novel with a matching ID

# get novel detail and list chapter


async def retrieve_novel(id: str) -> dict:
    novel = await novel_collection.find_one({"_id": ObjectId(id)})
    if novel:
        novel = novel_helper(novel)
        novel["chapter"] = await get_chapter_by_novel_id(id)
        return novel


# async def retrieve_novel(id: str) -> dict:
#     novel = await novel_collection.find_one({"_id": ObjectId(id)})
#     if novel:
#         return novel_helper(novel)

# Update a novel with a matching ID


async def update_novel(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    novel = await novel_collection.find_one({"_id": ObjectId(id)})
    if novel:
        updated_novel = await novel_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_novel:
            return True
        return False

# Delete a novel from the database


async def delete_novel(id: str):
    novel = await novel_collection.find_one({"_id": ObjectId(id)})
    if novel:
        await novel_collection.delete_one({"_id": ObjectId(id)})
        return True


async def get_top_novel(number: int) -> dict:
    novels = []
    async for novel in novel_collection.find().sort("views", -1).limit(number):
        novels.append(novel_helper(novel))
    return novels

# random novel


async def get_random_novel(number: int) -> dict:
    novels = []
    async for novel in novel_collection.aggregate([{"$sample": {"size": number}}]):
        novels.append(novel_helper(novel))
    return novels

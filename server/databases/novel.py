from bson.objectid import ObjectId
from server import connect
from server.databases.chapter import *
from datetime import datetime
from statistics import mean

novel_collection = connect.novel_collection


def novel_helper(novel) -> dict:
    return {
        "id": str(novel["_id"]),
        "title": novel["title"],
        "description": novel["description"] if "description" in novel else "",
        "genres": novel["genres"],
        "image_url": novel["image_url"],
        "banner_url": novel["banner_url"],
        "chapters": novel["chapter"],
        "views": novel["views"],
        "tags": novel["tags"],
        "rating": round(mean([x["rating"] for x in novel["ratings"]]), 1) if "ratings" in novel else 0,
        "year": novel["year"],
        "status": novel["status"],
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
        await update_novel(id, {"views": novel["views"] + 1})
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
    data["updated_at"] = datetime.now()
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
    async for novel in novel_collection.find({"status": {"$ne": "draft"}}).sort("views", -1).limit(number):
        novels.append(novel_helper(novel))
    return novels

# get random novel where staus != draft

async def get_random_novel(number: int) -> dict:
    novels = []
    async for novel in novel_collection.find({"status": {"$ne": "draft"}}).limit(number):
        novels.append(novel_helper(novel))
    return novels

# get my novel

async def get_my_novel(id: str) -> dict:
    novels = []
    async for novel in novel_collection.find({"account_id": id}).sort("updated_at", -1):
        novels.append(novel_helper(novel))
    return novels

# get novel by genre

async def get_novel_by_genre(genre: str) -> dict:
    novels = []
    async for novel in novel_collection.find({"genres": genre}):
        novels.append(novel_helper(novel))
    return novels

# get novel by status

async def get_novel_by_status(status: str) -> dict:
    novels = []
    async for novel in novel_collection.find({"status": status}).sort("created_at", -1):
        novels.append(novel_helper(novel))
    return novels

# get novel last update

async def get_novel_last_update(number: int) -> dict:
    novels = []
    async for novel in novel_collection.find({"status": {"$ne": "draft"}}).sort("updated_at", -1).limit(number):
        novels.append(novel_helper(novel))
    return novels

# update status novel

async def update_status_novel(id: str, status: str):
    novel = await novel_collection.find_one({"_id": ObjectId(id)})
    if novel:
        updated_novel = await novel_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"status": status}}
        )
        if updated_novel:
            return True
        return False

# push ratings to list in novel 

async def add_rating_novel(id: str, rating: float, user_id: str):
    novel = await novel_collection.find_one({"_id": ObjectId(id)})
    if novel:
        if "ratings" in novel:
            ratings = novel["ratings"]
            if user_id in [x["user_id"] for x in ratings]:
                for x in ratings:
                    if x["user_id"] == user_id:
                        x["rating"] = rating
            else:
                ratings.append({"user_id": user_id, "rating": rating})
            await novel_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"ratings": ratings}}
            )
        else:
            await novel_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": {"ratings": [{"user_id": user_id, "rating": rating}]}}
            )
        return True
    return False

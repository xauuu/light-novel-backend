from bson.objectid import ObjectId
from server import connect

chapter_collection = connect.chapter_collection
novel_collection = connect.novel_collection


def chapter_helper(chapter) -> dict:
    return {
        "chapter_number": chapter["chapter_number"],
        "id": str(chapter["_id"]),
        "title": chapter["title"],
        "description": chapter["description"] if "description" in chapter else "",
        "content": chapter["content"],
        "novel_id": chapter["novel_id"],
        "views": chapter["views"],
        "source_file_url": chapter["source_file_url"],
        "created_at": chapter["created_at"],
        "updated_at": chapter["updated_at"],
        "created_by": chapter["created_by"],
        "updated_by": chapter["updated_by"],
    }


# Retrieve all chapters present in the database
async def retrieve_chapters():
    chapters = []
    async for chapter in chapter_collection.find():
        chapters.append(chapter_helper(chapter))
    return chapters


# Add a new chapter into to the database
async def add_chapter(chapter_data: dict) -> dict:
    chapter_number = await chapter_collection.count_documents({"novel_id": chapter_data["novel_id"]}) + 1
    chapter_data["chapter_number"] = chapter_number
    await novel_collection.update_one({"_id": ObjectId(chapter_data["novel_id"])}, {"$set": {"chapter": chapter_number}})
    chapter = await chapter_collection.insert_one(chapter_data)
    new_chapter = await chapter_collection.find_one({"_id": chapter.inserted_id})
    return chapter_helper(new_chapter)


async def get_chapter_detail(chapter_number: int, novel_id: str):
    chapter = await chapter_collection.find_one({"chapter_number": chapter_number, "novel_id": novel_id})
    if chapter:
        previous_chapter = await chapter_collection.find_one({"chapter_number": chapter_number - 1, "novel_id": novel_id})
        next_chapter = await chapter_collection.find_one({"chapter_number": chapter_number + 1, "novel_id": novel_id})
        chapter = chapter_helper(chapter)
        chapter["previous"] = chapter_helper(
            previous_chapter) if previous_chapter else None
        chapter["next"] = chapter_helper(
            next_chapter) if next_chapter else None
        return chapter

# Retrieve a chapter with a matching ID


async def retrieve_chapter(id: str) -> dict:
    chapter = await chapter_collection.find_one({"_id": ObjectId(id)})
    if chapter:
        return chapter_helper(chapter)


# Update a chapter with a matching ID
async def update_chapter(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    chapter = await chapter_collection.find_one({"_id": ObjectId(id)})
    if chapter:
        updated_chapter = await chapter_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_chapter:
            return True
        return False


# Delete a chapter from the database
async def delete_chapter(id: str):
    chapter = await chapter_collection.find_one({"_id": ObjectId(id)})
    if chapter:
        await chapter_collection.delete_one({"_id": ObjectId(id)})
        return True

# get chapter by novel_id


async def get_chapter_by_novel_id(novel_id: str):
    chapters = []
    async for chapter in chapter_collection.find({"novel_id": novel_id}).sort("chapter_number", -1):
        chapters.append(chapter_helper(chapter))
    return chapters

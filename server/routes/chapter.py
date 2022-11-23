from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder

from server.databases.chapter import *

from server.models.chapter import *

from server.config.response import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="Chapter data added into the database")
async def add_chapter_data(chapter: ChapterSchema = Body(...)):
    chapter = jsonable_encoder(chapter)
    new_chapter = await add_chapter(chapter)
    return ResponseModel(new_chapter, "Chapter added successfully.")


@router.get("/", response_description="Chapters retrieved")
async def get_chapters():
    chapters = await retrieve_chapters()
    if chapters:
        return ResponseModel(chapters, "Chapters data retrieved successfully")
    return ResponseModel(chapters, "Empty list returned")


@router.get("/detail", response_description="Chapter data retrieved")
async def get_chapter_data(chapter_number: int = 0, novel_id: str = ""):
    chapter = await get_chapter_detail(chapter_number, novel_id)
    if chapter:
        return ResponseModel(chapter, "Chapter data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Chapter doesn't exist.")


@router.put("/{id}")
async def update_chapter_data(id: str, req: UpdateChapter = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_chapter = await update_chapter(id, req)
    if updated_chapter:
        return ResponseModel(
            "Chapter with ID: {} name update is successful".format(id),
            "Chapter name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the chapter data.",
    )


@router.delete("/{id}", response_description="Chapter data deleted from the database")
async def delete_chapter_data(id: str):
    deleted_chapter = await delete_chapter(id)
    if deleted_chapter:
        return ResponseModel(
            "Chapter with ID: {} removed".format(
                id), "Chapter deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Chapter with id {0} doesn't exist".format(
            id)
    )

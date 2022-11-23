from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.databases.novel import *

from server.models.novel import (
    Novel as NovelSchema,
    UpdateNovel as UpdateNovelModel,
)

from server.config.response import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="Novel data added into the database")
async def add_novel_data(novel: NovelSchema = Body(...)):
    novel = jsonable_encoder(novel)
    new_novel = await add_novel(novel)
    return ResponseModel(new_novel, "Novel added successfully.")


@router.get("/", response_description="Novels retrieved")
async def get_novels():
    novels = await retrieve_novels()
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")


@router.get("/{id}", response_description="Novel data retrieved")
async def get_novel_data(id):
    novel = await retrieve_novel(id)
    if novel:
        return ResponseModel(novel, "Novel data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Novel doesn't exist.")


@router.put("/{id}")
async def update_novel_data(id: str, req: UpdateNovelModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_novel = await update_novel(id, req)
    if updated_novel:
        return ResponseModel(
            "Novel with ID: {} name update is successful".format(id),
            "Novel name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the novel data.",
    )


@router.delete("/{id}", response_description="Novel data deleted from the database")
async def delete_novel_data(id: str):
    deleted_novel = await delete_novel(id)
    if deleted_novel:
        return ResponseModel(
            "Novel with ID: {} removed".format(
                id), "Novel deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Novel with id {0} doesn't exist".format(id)
    )


@router.get("/top/{number}", response_description="Top novels retrieved")
async def get_top_novels(number: int):
    novels = await get_random_novel(number)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from server.databases.novel import *

from server.models.novel import (
    Novel as NovelSchema,
    UpdateNovel as UpdateNovelModel,
)

from server.config.response import ResponseModel, ErrorResponseModel
from server import oauth2
import json

router = APIRouter()


@router.post("/create", response_description="Novel data added into the database")
async def add_novel_data(novel: NovelSchema = Body(...), account_id: str = Depends(oauth2.require_user)):
    novel = jsonable_encoder(novel)
    novel['account_id'] = account_id
    await add_novel(novel)
    return ResponseModel(novel, "Novel added successfully.")


@router.get("/", response_description="Novels retrieved")
async def get_novels():
    novels = await retrieve_novels()
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")


@router.get("/detail/{id}", response_description="Novel data retrieved")
async def get_novel_data(id):
    novel = await retrieve_novel(id)
    if novel:
        return ResponseModel(novel, "Novel data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Novel doesn't exist.")


@router.put("/update/{id}")
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


@router.get("/random/{number}", response_description="Top novels retrieved")
async def get_random_novels(number: int):
    novels = await get_random_novel(number)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

@router.get("/top/{number}", response_description="Top novels retrieved")
async def get_top_novels(number: int):
    novels = await get_top_novel(number)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

# get my novel list
@router.get("/my", response_description="My novels retrieved")
async def get_my_novels(user_id: str = Depends(oauth2.require_user)):
    novels = await get_my_novel(user_id)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

# get novel by status

@router.get("/status/{status}", response_description="Novels retrieved")
async def get_novels_by_status(status: str, admin: bool = Depends(oauth2.require_admin)):
    if not admin:
        return ErrorResponseModel("An error occurred.", 404, "You are not admin")
    novels = await get_novel_by_status(status)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

# get novel last update

@router.get("/last-update/{number}", response_description="Novels retrieved")
async def get_novels_last_update(number: int):
    novels = await get_novel_last_update(number)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

#  rating novel

@router.post("/rating/{id}", response_description="Novel data added into the database")
async def add_novel_rating(id: str, rating: float = Body(...), user_id: str = Depends(oauth2.require_user)):
    rating = await add_rating_novel(id, rating, user_id)
    if rating:
        return ResponseModel(200, "Rating added successfully.")
    return ResponseModel(400, "Empty list returned")

#search novel

@router.get("/search/{keyword}", response_description="Novels retrieved")
async def search_novel(keyword: str):
    novels = await get_novel_by_search(keyword)
    if novels:
        return ResponseModel(novels, "Novels data retrieved successfully")
    return ResponseModel(novels, "Empty list returned")

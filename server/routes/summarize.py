from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from server.config.response import ResponseModel, ErrorResponseModel
from server.summarize.textrank import generate_summary as textrank_summary
from server.summarize.frequency import summarize as frequency_summary

router = APIRouter()

@router.post("/textrank_summary", response_description="Summarize text")
async def summarize(request: Request, text: str = Body(...)):
    try:
        data = jsonable_encoder(request.json())
        summary = textrank_summary(data["text"], 3)
        return ResponseModel(summary, "Summary generated successfully")
    except Exception as e:
        return ErrorResponseModel("An error occurred", 500, str(e))

@router.post("/frequency_summary", response_description="Summarize text")
async def summarize(request: Request, text: str = Body(...)):
    try:
        data = jsonable_encoder(request.json())
        summary = frequency_summary(data["text"], 3)
        return ResponseModel(summary, "Summary generated successfully")
    except Exception as e:
        return ErrorResponseModel("An error occurred", 500, str(e))

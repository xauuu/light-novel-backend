from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from server.config.response import ResponseModel, ErrorResponseModel
from server.summarize.textrank import generate_summary as textrank_summary
from server.summarize.frequency import summarize as frequency_summary
from pydantic import BaseModel, Field

router = APIRouter()

class SummarySchema(BaseModel):
    text: str = Field(...)
    method: str = Field(...)
    sentences: int = Field(...)
    type: str = Field(...)
    url: str = Field(None)

@router.post("/", response_description="Summarize text")
async def summarize(request: SummarySchema = Body(...)):
    try:
        if request.method == "textrank":
            summary = textrank_summary(request.text, request.type, request.url, request.sentences)
        elif request.method == "frequency":
            summary = frequency_summary(request.text, request.type, request.url, request.sentences)
        else:
            return ErrorResponseModel("An error occurred", 500, "Invalid method")
        return ResponseModel(summary, "Summary generated successfully")
    except Exception as e:
        return ErrorResponseModel("An error occurred", 500, str(e))

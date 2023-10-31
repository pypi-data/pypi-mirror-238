from pydantic import BaseModel, Field
from typing import List

class Word(BaseModel):
    start: float
    end: float
    word: str
    disfluency: bool = Field(None)
    profanity: bool = Field(None)
    speaker: int = Field(None)

class Chapter(BaseModel):
    start: float
    end: float
    title: str
    summary: str

class Chapters(BaseModel):
    title: str
    chapters: List[Chapter]

class APIJob(BaseModel):
    id: str
    status: str
    step: str
    raw_duration: int = Field(None)

    language_code: str = Field(None)
    speech_duration: int = Field(None)
    sentences: List[List[Word]] = Field(None)
    summary: str = Field(None)
    chapters: Chapters = Field(None)


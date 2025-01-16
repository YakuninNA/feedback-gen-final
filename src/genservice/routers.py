import json
from datetime import datetime

from arq.connections import (
    create_pool,
    RedisSettings
)
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Form,
    Request,
    Query,
)
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates

from src.authservice.dependencies import get_current_user
from src.database import get_async_session
from src.genservice.functionality.utility import convert_to_html
from src.genservice.models import FeedbackGen


router = APIRouter(
    prefix="/functionality",
    tags=["functionality"]
)


templates = Jinja2Templates(directory="template/gen_templates")


redis_settings = RedisSettings(
    host='localhost',
    port=6379,
    database=0
)


@router.get("/home", response_class=HTMLResponse)
async def functionality_home(
    request: Request,
    user=Depends(get_current_user)
):
    return templates.TemplateResponse("functionality_page.html", {
        "request": request,
        "user": user
    })


@router.get("/feedback_generation", response_class=HTMLResponse)
async def get_registration_form(
    request: Request,
    user=Depends(get_current_user)
):
    try:
        is_authenticated = user is True

    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "user": user,
            "is_authenticated": False,
            "error": f"User is not authenticated - {str(e)}."
        })

    return templates.TemplateResponse("feedback_generation.html", {
        "request": request,
        "user": user,
        "is_authenticated": is_authenticated
    })


@router.post("/feedback_generation", response_class=HTMLResponse)
async def process_transcript(
        request: Request,
        transcript: UploadFile = File(...),
        requirements: str = Form(...),
        position: str = Form(...),
        user=Depends(get_current_user)
):
    try:
        file_content = await transcript.read()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        redis = await create_pool(redis_settings)
        job = await redis.enqueue_job(
            'process_transcript_task',
            file_content.decode(),
            requirements,
            position,
            user.username,
            user.name,
            user.surname,
            transcript.filename,
            timestamp,
        )

        # Return the job_id for the frontend to track
        context = {
            "request": request,
            "user": user,
            "message": "Your feedback is being generated. Use the job ID to download the file later.",
            "job_id": job.job_id
        }

        return templates.TemplateResponse("feedback_popup.html", context)

    except Exception as e:
        return templates.TemplateResponse("feedback_generation.html", {
            "request": request,
            "user": user,
            "is_authenticated": True,
            "error": f"An error occurred: {str(e)}."
        })


@router.get("/feedback_status/{job_id}", response_model=dict)
async def feedback_status(job_id: str):
    redis = await create_pool(redis_settings)
    result = await redis.get(job_id)

    if result:
        data = json.loads(result)
        if "error" in data:
            return {"status": "failed", "error": data["error"]}
        return {"status": "completed", "filename": data["filename"], "file_ready": True}
    return {"status": "pending", "file_ready": False}


@router.get("/feedback_review")
async def get_feedback_components(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(get_current_user),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100)
):
    try:
        interviewer_username = f"{user.username}"
        offset = (page - 1) * limit

        query = select(
            FeedbackGen.interviewer_full_name,
            FeedbackGen.feedback_name,
            FeedbackGen.soft_skills,
            FeedbackGen.engineering_basics,
            FeedbackGen.technical_skills
        ).where(FeedbackGen.interviewer_username == interviewer_username).offset(offset).limit(limit)

        result = await session.execute(query)
        feedbacks = result.fetchall()

        formatted_feedbacks = []
        for feedback in feedbacks:
            feedback_dict = {
                "interviewer_full_name": feedback.interviewer_full_name,
                "feedback_name": feedback.feedback_name,
                "soft_skills": convert_to_html(feedback.soft_skills),
                "engineering_basics": convert_to_html(feedback.engineering_basics),
                "technical_skills": convert_to_html(feedback.technical_skills)
            }
            formatted_feedbacks.append(feedback_dict)

        total_feedbacks_query = select(func.count()).select_from(FeedbackGen).where(
            FeedbackGen.interviewer_username == interviewer_username
        )
        total_feedbacks_result = await session.execute(total_feedbacks_query)
        total_count = total_feedbacks_result.scalar()

        total_pages = (total_count + limit - 1) // limit

    except Exception as e:
        return templates.TemplateResponse("feedback_review.html", {
            "request": request,
            "user": user,
            "is_authenticated": True,
            "error": f"An error occurred: {str(e)}."
        })

    return templates.TemplateResponse("feedback_review.html", {
        "request": request,
        "feedbacks": formatted_feedbacks,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_count": total_count,
    })

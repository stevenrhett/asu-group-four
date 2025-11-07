import shutil
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import require_role
from app.core.config import settings
from app.models.profile import Profile, ProfilePublic
from app.models.user import User
from app.services.parsing import SUPPORTED_EXTENSIONS, ResumeParsingError, parse_resume

router = APIRouter()


@router.post("/resume", response_model=ProfilePublic)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role("seeker")),
):
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()
    if not filename or not extension:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename with extension required")
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported resume format: {extension}",
        )

    storage_dir = Path(settings.resume_storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)

    dest_path = storage_dir / f"{current_user.id}_{int(datetime.utcnow().timestamp())}{extension}"
    try:
        file.file.seek(0)
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        if dest_path.stat().st_size == 0:
            dest_path.unlink(missing_ok=True)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")
    finally:
        await file.close()

    try:
        parsed = parse_resume(dest_path)
    except ResumeParsingError as exc:
        dest_path.unlink(missing_ok=True)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    now = datetime.utcnow()
    profile = await Profile.find_one(Profile.user_id == str(current_user.id))
    if profile:
        profile.skills = parsed.skills
        profile.titles = parsed.titles
        profile.raw_text = parsed.raw_text
        profile.resume_path = str(dest_path)
        profile.parsed_at = now
        await profile.save()
    else:
        profile = Profile(
            user_id=str(current_user.id),
            skills=parsed.skills,
            titles=parsed.titles,
            raw_text=parsed.raw_text,
            resume_path=str(dest_path),
            parsed_at=now,
        )
        await profile.insert()

    return ProfilePublic.from_document(profile)

from fastapi import APIRouter

from app.api.routes import users, auth, event, topic, group

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(event.router, prefix="/events", tags=["Events"])
api_router.include_router(topic.router, prefix="/topics", tags=["Topics"])
api_router.include_router(group.router, prefix="/groups", tags=["Groups"])

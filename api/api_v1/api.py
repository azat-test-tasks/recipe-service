from fastapi import APIRouter

from api.api_v1.endpoints.auth import login, registration
from api.api_v1.endpoints.recipes import recipe
from api.api_v1.endpoints.users import user
from api.api_v1.endpoints.ratings import rating
from api.api_v1.endpoints.images import image

api_router = APIRouter()

api_router.include_router(recipe.router, prefix="/recipe", tags=["Recipes"])

api_router.include_router(user.router, prefix="/users", tags=["User"])

api_router.include_router(login.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(registration.router, prefix="/auth", tags=["Authentication"])

api_router.include_router(rating.router, prefix="/ratings", tags=["Ratings"])

api_router.include_router(image.router, prefix="/images", tags=["Images"])

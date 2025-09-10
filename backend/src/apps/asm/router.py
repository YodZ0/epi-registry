from fastapi import APIRouter

__all__ = ("router",)


router = APIRouter(
    prefix="/asm",
    tags=["ASM - anti-seizure medication"],
)


@router.get("/recommend")
async def get_recommended_medications():
    return {"msg": "Hello world!"}

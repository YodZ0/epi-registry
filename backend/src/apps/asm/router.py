from fastapi import APIRouter

__all__ = ("router",)


router = APIRouter(
    prefix="/asm",
    tags=["ASM - anti-seizure medication"],
)


@router.post("/selection")
async def select_asm():
    """
    Selects antiseizure medications (ASMs) based on seizure type(s) and
    patient-specific clinical modifiers.

    Returns three mandatory tiers:\n
        1. Preferred (first-line)
        2. Alternative (second-line)
        3. Less preferred (third-line)

    And one optional tier:\n
        4. Contraindicated / least desirable – populated only when a drug
           is completely excluded (e.g., valproate in a woman of child-bearing
           potential with focal seizures) or falls below tier 3 after all
           modifier adjustments.

    Drugs inside each tier are sorted alphabetically; every entry includes
    short rationale text (“why this tier”).
    """
    return {"msg": "Hello world!"}

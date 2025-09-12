import logging
from fastapi import APIRouter

from .service import ASMService
from .schemas import ASMSelectionRequestSchema, ASMSelectionResponseSchema

logger = logging.getLogger(__name__)

__all__ = ("router",)


router = APIRouter(
    prefix="/asm",
    tags=["ASM - anti-seizure medication"],
)


@router.post("/selection")
async def select_asm(
    asm_selection: ASMSelectionRequestSchema,
) -> ASMSelectionResponseSchema:
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
    asm_service = ASMService()
    proposed_selection = asm_service.select(asm_selection)
    logger.debug("Proposed selection: %s", proposed_selection)
    return proposed_selection

import pytest

from src.apps.asm.service import ASMService
from src.apps.asm.schemas import ASMSelectionRequestSchema, ASMSelectionResponseSchema


class TestASMService:

    @pytest.fixture
    def service(self) -> ASMService:
        return ASMService()

    @pytest.mark.asyncio
    async def test_selection_female(self, service: ASMService):
        female_test_case = {
            "gender": "female",
            "age": 22,
            "weight": 45.5,
            "seizureTypes": ["gtc", "myoclonic", "absence"],
            "modifiers": ["oral-contraceptive", "migraine", "female-fertile"],
        }
        selection_request = ASMSelectionRequestSchema.model_validate(female_test_case)
        expected_result = ASMSelectionResponseSchema(
            tiers={
                "tier_1": ["LTG", "LEV"],
                "tier_2": ["VPA"],
                "tier_3": ["TPM", "ZNS", "CLB", "CLN"],
            },
            patient_snapshot={
                "gender": selection_request.gender,
                "age": selection_request.age,
                "weight": selection_request.weight,
            },
        )
        selection = service.select(selection_request)
        assert expected_result == selection

    @pytest.mark.asyncio
    async def test_selection_male(self, service: ASMService):
        male_test_case = {
            "gender": "male",
            "age": 35,
            "weight": 74.8,
            "seizureTypes": ["focal"],
            "modifiers": ["diabetes", "comedications"],
        }
        selection_request = ASMSelectionRequestSchema.model_validate(male_test_case)
        expected_result = ASMSelectionResponseSchema(
            tiers={
                "tier_1": ["LEV", "LTG", "OXC", "ESL", "LCM", "BRV", "ZNS"],
                "tier_2": ["TPM", "PER", "GBP"],
                "tier_3": ["CBZ", "VPA", "CLB", "PGB"],
                "tier_4": ["PHT", "PB"],
            },
            patient_snapshot={
                "gender": selection_request.gender,
                "age": selection_request.age,
                "weight": selection_request.weight,
            },
        )
        selection = service.select(selection_request)
        assert expected_result == selection


# "focal": {
#     "1": ["LEV", "CBZ", "LTG", "OXC", "ESL", "LCM"],
#     "2": ["TPM", "VPA", "PER", "PHT", "BRV", "ZNS"],
#     "3": ["CLB", "PB", "GBP", "PGB"]
#   }
# modifiers: "diabetes", "comedications"
#
# INITIAL SCORE MAP
# "LEV" = 1; comedications focal -= 1; 1
# "CBZ" = 1; diabetes += 1; 2; comedications focal += 1; 3
# "LTG" = 1; comedications focal -= 1; 1
# "OXC" = 1;
# "ESL" = 1;
# "LCM" = 1; comedications focal -= 1; 1
#
# "TPM" = 2;
# "VPA" = 2; diabetes += 1; 3;
# "PER" = 2; diabetes += 1; 3; comedications focal -= 1; 2
# "PHT" = 2; diabetes += 1; 3; comedications focal += 1; 4
# "BRV" = 2; comedications focal -= 1; 1;
# "ZNS" = 2; comedications focal -= 1; 1;
#
# "CLB" = 3;
# "PB" = 3; comedications focal += 1; 4
# "GBP" = 3; comedications focal -= 1; 2
# "PGB" = 3;
#
### RESULT SCORE MAP
# "LEV" = 1;
# "LTG" = 1;
# "OXC" = 1;
# "ESL" = 1;
# "LCM" = 1;
# "BRV" = 1;
# "ZNS" = 1;
#
# "TPM" = 2;
# "PER" = 2;
# "GBP" = 2;
#
# "CBZ" = 3;
# "VPA" = 3;
# "PHT" = 3;
# "CLB" = 3;
# "PB" = 3;
# "PGB" = 3;
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

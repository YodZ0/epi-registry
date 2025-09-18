import logging
from typing import List, Dict

from .json_repository import (
    get_drugs,
    get_seizure_map,
    get_modifier_rules,
)

from .schemas import ASMSelectionRequestSchema, ASMSelectionResponseSchema

logger = logging.getLogger(__name__)


class ASMService:
    def __init__(self) -> None:
        self._drugs = get_drugs()
        self._seizure_map = get_seizure_map()
        self._rules = get_modifier_rules()

    def select(
        self,
        selection: ASMSelectionRequestSchema,
    ) -> ASMSelectionResponseSchema:
        """
        Input: ASMSelectionRequestSchema(
          gender="female",
          age=22,
          weight=45.5,
          seizure_types=["gtc", "myoclonic", "absence"],
          modifiers=["oral-contraceptive", "migraine", "female-fertile"],
        )
        Output:
        """
        seizure_types = selection.seizure_types
        mods = selection.modifiers
        combined_st = self._combine_seizure_types(seizure_types)
        proposed_drugs = self._get_proposed_drugs(combined_st)
        drugs_score_map = self._create_asm_score_map(proposed_drugs)
        modified_drugs_score_map = self._apply_modifiers_rules(
            score_map=drugs_score_map,
            mods=mods,
            seizure_types=seizure_types,
        )
        grouped_drugs = self._group_by_tiers(modified_drugs_score_map)
        return ASMSelectionResponseSchema(
            tiers=grouped_drugs,
            patient_snapshot={
                "gender": selection.gender,
                "age": selection.age,
                "weight": selection.weight,
            },
        )

    @staticmethod
    def _combine_seizure_types(seizure_types: List[str]) -> str:
        """
        Sort seizure_type and return combined string.

        Input: ["gtc", "myoclonic", "absence"]
        Output: "absence+gtc+myoclonic"
        """
        seizure_types.sort()
        combined_seizure_types = "+".join(seizure_types)
        logger.debug("Combined seizure types: %r", combined_seizure_types)
        return combined_seizure_types

    def _get_proposed_drugs(self, combined_seizure_types: str) -> Dict[int, List[str]]:
        """
        Returns proposed ASMs dict based on seizure types combination.
        Where dict key - tier level, value - list of ASMs.

        Input: "absence+gtc+myoclonic"
        Output: {
          1: ["VPA"],
          2: ["LTG", "LEV"],
          3: ["TPM", "ZNS", "CLB", "CLN"]
        }
        """
        proposed_drugs = self._seizure_map.get(combined_seizure_types)
        logger.debug(
            "Proposed drugs for %r: %s",
            combined_seizure_types,
            proposed_drugs,
        )
        return proposed_drugs

    @staticmethod
    def _create_asm_score_map(proposed_drugs: Dict[int, List[str]]) -> Dict[str, int]:
        """
        Input: {
          1: ["VPA"],
          2: ["LTG", "LEV"],
          3: ["TPM", "ZNS", "CLB", "CLN"]
        }
        Output: {"VPA": 1, "LTG": 2, ..., "CLN": 3}
        """
        asm_score_map = {}
        for key, values in proposed_drugs.items():
            for value in values:
                asm_score_map[value] = key
        logger.debug("ASM score map: %s", asm_score_map)
        return asm_score_map

    def _apply_modifiers_rules(
        self,
        *,
        score_map: Dict[str, int],
        mods: List[str],
        seizure_types: List[str],
    ) -> Dict[str, int]:
        """
        Applies modifiers rules to drugs score map.

        Input:
          score_map = {"VPA": 1, "LTG": 2, ..., "CLN": 3}
          mods = ["oral-contraceptive", "migraine", "female-fertile"]
          seizure_types = ["gtc", "myoclonic", "absence"]
        Output: {
          "VPA": 2,  # calc -1, but has max level 2
          "LTG": 1, "LEV": 1,
          "TPM": 3, "ZNS": 3, "CLB": 3, "CLN": 3,
        }
        """
        for asm, _ in score_map.items():
            asm_rules = self._rules.get(asm, None)

            if asm_rules is None:
                continue

            max_level = 1  # by default every ASM can have max tier
            for rule in asm_rules:
                # Filter rules by modifier and seizure
                # If ASM does not have a rule for a modifier, skip
                if rule.get("modifier") not in mods:
                    continue
                if rule.get("seizure") not in seizure_types:
                    continue

                logger.debug("Rule found for %r: %s", asm, rule)

                # Check if rule have max level lower than default
                max_level = max(max_level, rule.get("max"))

                # Apply rule action
                if rule.get("action") == "upgrade":
                    score_map[asm] -= rule.get("steps")
                else:
                    score_map[asm] += rule.get("steps")

            # Apply max level for asm
            score_map[asm] = max(score_map[asm], max_level)
        logger.debug("Score map after modifiers rules: %s", score_map)
        return score_map

    @staticmethod
    def _group_by_tiers(score_map: Dict[str, int]) -> Dict[str, List[str]]:
        """
        Group modified score map by tiers.

        Input: {
          "VPA": 2,
          "LTG": 1, "LEV": 1,
          "TPM": 3, "ZNS": 3, "CLB": 3, "CLN": 3,
        }
        Output: {
          "tier_1": ["LTG", "LEV"],
          "tier_2": ["VPA"],
          "tier_3": ["TPM", "ZNS", "CLB", "CLN"],
        }
        """
        tiers: Dict[str, List[str]] = {
            "tier_1": [],
            "tier_2": [],
            "tier_3": [],
            "tier_4": [],
        }

        for drug, score in score_map.items():
            if score <= 1:
                tiers["tier_1"].append(drug)
            elif score == 2:
                tiers["tier_2"].append(drug)
            elif score == 3:
                tiers["tier_3"].append(drug)
            else:  # 4 и выше
                tiers["tier_4"].append(drug)

        # Exclude empty tiers
        return {k: v for k, v in tiers.items() if v}

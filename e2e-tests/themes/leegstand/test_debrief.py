from api.config import Violation
from api.tasks.debrief import (
    test_opstellen_beeldverslag,
    test_opstellen_rapport_van_bevindingen,
    test_terugkoppelen_melder_2,
    test_verwerken_debrief,
)
from api.tasks.summon import (
    test_monitoren_binnenkomen_vergunningaanvraag,
    test_nakijken_aanschrijving,
    test_opstellen_concept_aanschrijving,
    test_verwerk_aanschrijving,
)
from api.tasks.unoccupied import test_opstellen_aanschrijving_eigenaar
from api.tasks.visit import test_doorgeven_status_top, test_inplannen_status
from api.test import DefaultAPITest
from api.validators import ValidateOpenTasks


class TestLeegstandViolationYes(DefaultAPITest):
    def get_case_data(self):
        return {
            "theme_id": 5,
            "reason": 15,
            "bag_id": "234",
            "subjects": [22],
        }

    def test(self):
        self.get_case().run_steps(
            test_inplannen_status(),
            test_doorgeven_status_top(),
            test_verwerken_debrief(violation=Violation.YES),
            ValidateOpenTasks(
                test_opstellen_rapport_van_bevindingen,
                test_opstellen_beeldverslag,
            ),
            test_opstellen_beeldverslag(),
            test_opstellen_rapport_van_bevindingen(),
            ValidateOpenTasks(test_opstellen_concept_aanschrijving),
        )


class TestLeegstandViolationLikelyInhabited(DefaultAPITest):
    def get_case_data(self):
        return {
            "theme_id": 5,
            "reason": 15,
            "bag_id": "234",
            "subjects": [22],
        }

    def test(self):
        self.get_case().run_steps(
            test_inplannen_status(),
            test_doorgeven_status_top(),
            test_verwerken_debrief(violation=Violation.LIKELY_INHABITED),
            ValidateOpenTasks(test_opstellen_aanschrijving_eigenaar),
        )

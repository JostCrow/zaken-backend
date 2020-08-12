import logging

import requests
from django.conf import settings
from faker import Faker
from tenacity import after_log, retry, stop_after_attempt

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), after=after_log(logger, logging.ERROR))
def get_fines(id):
    """
    Search the Belasting API for fines with case_id identification
    """

    print(f"Retrieving fines for {id}")
    # Just logging the length of the token here, to see if it's coming through correctly
    print(f"Check for access {len(settings.BELASTING_API_ACCESS_TOKEN)}")

    parameter = {"identificatienummer": "67018_1_22"}
    header = {"authorization": f"Bearer {settings.BELASTING_API_ACCESS_TOKEN}"}

    try:
        response = requests.get(
            url=settings.BELASTING_API_URL, headers=header, params=parameter
        )
    except Exception as e:
        print(e)

    print("Parameter:")
    print(parameter)
    print("Done request")
    print(response)

    response.raise_for_status()

    return response.json()


def get_mock_fines(case_id):
    fake = Faker("nl_NL")
    return {
        "message": "mocked data",
        "items": [
            {
                "identificatienummer": case_id,
                "vorderingnummer": fake.ssn(),
                "jaar": 2020,
                "soort_vordering": "PBN",
                "omschrijving_soort_vordering": "Publiekrechtelijk (niet-fiscaal)",
                "indicatie_publiekrechtelijk": "N",
                "subjectnr": fake.ssn(),
                "opgemaaktenaam": fake.name(),
                "subjectnr_opdrachtgever": fake.ssn(),
                "opgemaaktenaam_opdrachtgever": "Wonen inc. vord.",
                "runnr": fake.ssn(),
                "omschrijving_run": "Wonen inc. vord.",
                "code_runwijze": "IVO",
                "omschrijving_runwijze": "Incidentele vorderingen",
                "dagtekening": "2020-01-29T23:00:00Z",
                "vervaldatum": "2020-02-28T23:00:00Z",
                "indicatie_combi_dwangbevel": "N",
                "notatekst": None,
                "omschrijving": None,
                "invorderingstatus": "AANM",
                "indicatie_bet_hern_bevel": "N",
                "landcode": None,
                "kenteken": None,
                "bonnummer": None,
                "bedrag_opgelegd": 10000,
                "bedrag_open_post_incl_rente": 10215.50,
                "totaalbedrag_open_kosten": 15,
                "bedrag_open_rente": 200.50,
                "reden_opschorting": None,
                "omschrijving_1": f"Het onttrekken van de woonruimte {fake.address()}",
                "omschrijving_2": "aan de woonruimtevoorraad zonder dat hiervoor",
            }
        ],
    }

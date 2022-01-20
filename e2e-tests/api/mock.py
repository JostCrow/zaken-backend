from api.config import Reason, Theme
from faker import Faker

fake = Faker()
profile = fake.profile(fields=["username", "mail", "name"])


def get_person():
    return {
        "id": fake.uuid4(),
        "email": profile["mail"],
        "username": profile["username"],
        "first_name": profile["name"].split(" ")[0],
        "last_name": " ".join(profile["name"].split(" ")[1:]),
        "full_name": profile["name"],
    }


def get_case_mock(
    theme_id=Theme.VAKANTIEVERHUUR,
    reason=Reason.Vakantieverhuur.NOTIFICATION,
    bag_id="234",
    subjects=[],
    description_citizenreport=None,
    identification=None,
):
    return {
        "theme_id": theme_id,
        "reason_id": reason,
        "bag_id": bag_id,
        "subject_ids": subjects,
        "description_citizenreport": description_citizenreport,
        "identification": identification,
    }

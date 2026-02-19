from core.models import Place
import requests
from typing import Sequence

from tripplan.settings import MAX_ALLOWED_PLACES_PER_PROJECT, ARTIC_API_ENDPOINT


def validate_and_cache_initial_places(ids: Sequence[int]) -> tuple[bool, str]:
    """
    Get a sequence of IDs and validate them.

    Validate maximum number per a project, duplicates, existence in
    the external API and in the internal DB.
    if the ID is valid and not save in the DB yey it will be saved.

    Args:
        ids (Sequence[int]): IDs to be checked.

    Returns:
        tuple[bool, str]: success state and explanation message.
    """
    msg = ""
    success = True
    if len(ids) > MAX_ALLOWED_PLACES_PER_PROJECT:
        msg = (
            f"Too many places per project - {len(ids)}. "
            "The maximum number of allowed places per project is "
            f"{MAX_ALLOWED_PLACES_PER_PROJECT}"
        )
        success = False
    elif len(ids) != len(set(ids)):
        msg = "'initial_places' has duplicates"
        success = False

    if not success:
        return success, msg

    valid, invalid = fetch_and_cache_places(ids)

    if invalid:
        msg = (
            "Some of the places are invalid "
            "[" + ", ".join(str(id) for id in invalid) + "]"
        )
        success = False

    return success, msg


def fetch_and_cache_places(ids: Sequence[int]) -> tuple[list, list]:
    """
    Get a sequence of IDs and check if each exists in the internal DB.
    If the ID doesn't exist in the DB the function will try to fetch it from the API.

    Args:
        ids (Sequence[int]): IDs to be checked.

    Returns:
        tuple[list, list]: valid and invalid IDs.
    """
    valid = []
    invalid = []
    for ID in ids:
        if Place.objects.filter(artic_id=ID).exists():
            valid.append(ID)
            continue

        resp = requests.get(ARTIC_API_ENDPOINT + str(ID))
        if resp.status_code == 200:
            place = resp.json()["data"]
            Place.objects.create(name=place["title"], artic_id=place["id"])
            valid.append(ID)
        else:
            invalid.append(ID)

    return valid, invalid

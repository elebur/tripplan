from core.models import Place
import requests
from typing import Sequence

from rest_framework.serializers import ValidationError
from rest_framework import status

from tripplan.settings import MAX_ALLOWED_PLACES_PER_PROJECT, ARTIC_API_ENDPOINT


def validate_places(ids: Sequence[int]) -> tuple[bool, str]:
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

    invalid = fetch_and_cache_places(ids)

    if invalid:
        msg = (
            "Some of the places are invalid "
            "[" + ", ".join(str(id) for id in invalid) + "]"
        )
        success = False

    return success, msg


def fetch_and_cache_places(ids: Sequence[int]) -> list:
    """
    Get a sequence of IDs and check if each exists in the internal DB.
    If the ID doesn't exist in the DB the function will try to fetch it from the API.

    Args:
        ids (Sequence[int]): IDs to be checked.

    Returns:
        list: a list of invalid IDs.
    """
    non_cached = set()
    cached = set()
    for ID in ids:
        if not Place.objects.filter(artic_id=ID).exists():
            non_cached.add(ID)
        else:
            cached.add(ID)

    query = "?ids=" + ",".join(str(id) for id in non_cached)

    resp = requests.get(ARTIC_API_ENDPOINT + query)
    if resp.status_code != 200:
        raise ValidationError(
            {"details": resp.json()["detail"]},
            code=status.HTTP_400_BAD_REQUEST,
        )

    places = resp.json()["data"]
    fetched = set()
    for place in places:
        Place.objects.get_or_create(name=place["title"], artic_id=place["id"])
        fetched.add(place["id"])

    return list(non_cached.difference(fetched))

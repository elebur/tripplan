# Task & description
Task description can be found [here](task.md).

# Postman

[Link](https://web.postman.co/workspace/Redirector~ff1fb23a-1c5f-4bb2-9bea-4772c9a56cc3/collection/38964050-a6c41bfe-7811-4dbf-96ae-a88ccfb61b02?action=share&source=copy-link&creator=38964050) to the collection of requests.



# Setup & launch
* clone the repository: `git clone https://github.com/elebur/tripplan.git`
* `cd tripplan`
* create a virtual environment: `python -m venv .venv`
* activate it `source .venv/bin/activate`
* install requirements: `pip install -r requirements.txt`
* navigate to the project root: `cd tripplan`
* apply migrations: `python manage.py migrate`
* run the development server: `python manage.py runserver`

The API root url is http://localhost:8000/api/

# Project endpoints
## Errors
If an error occurs during the request the status code will be `non-2**` (`400, 404, 503` etc.)

**Body**:
```json
{
    "details": <error description>
}
```
## `project/`
### `POST`
**Description**: Create new project.

**Body**:
```json
{
    "name": "Project's Name",
    "description": "Description",
    "start_date": "2026-12-12",
    "initial_places": [
        1, 2, 3, 4
    ]
}
```
* The length of the `name` must be less then or equal to 64
* All fields except the `name` are optional.
* `start_date` must be in the next format - `YYYY-MM-DD`
* `initial_places` is an array of IDs of places.
    * ID must be a valid ID of a gallery from https://api.artic.edu/docs/#galleries
    * Up to ten places per project.
    * No duplicates allowed.

**Return value**:

*Status code*: `201`
```json
{
    "project_id": <id of the created project>
}
```

## `project/<project_id>/`
### `GET`
**Description**: Return a project by its ID.

**Body**: None

**Return value**:
```json
{
    "id": 4,
    "name": "Project's Name",
    "description": "Description",
    "start_date": "2026-12-12"
}
```

### `DELETE`
**Description**: Delete the project by ID.

**Body**: None

**Return value**:
```json
{
    "details": "The project<project_id> has been deleted."
}
```

### `PUT`
**Description**: Update any field in the project (except `places`)

**Body**: None
```json
{
    "name": "new name",
    "description": "new description",
    "start_date": "2027-12-12"
}
```
* All fields are optional.

**Return value**:
All project's fields with updated values.

*Status code*: `200`

```json
{
    "id": 2,
    "name": "new name",
    "description": "description",
    "start_date": "2026-12-12"
}
```

## `projects/`
### `GET`
Return all available projects.

**Body**: None

**Return value**:

An array of objects. Each object is a project.
Empty array if no projects available.

*Status code*: `200`

```json
[
    {
        "id": 2,
        "name": "new name",
        "description": "description",
        "start_date": "2026-12-12"
    },
    {
        "id": 4,
        "name": "Project's Name",
        "description": "Description",
        "start_date": "2026-12-12"
    },
    {
        "id": 5,
        "name": "Project's Name",
        "description": "Description",
        "start_date": "2026-12-12"
    }
]
```

# Place endpoints
## `project/<project_id>/place/`
### `POST`
Create new place for the given project.

**Body**:
```json
{
    "artic_id": 2147476040
}
```
* ID of the gallery from the https://api.artic.edu/docs/#galleries (will be validated)

**Return value**:

IDs of the project and of the place.

*Status code*: `201`

```json
{
    "project_id": 5,
    "place_id": 12,
    "pair_id": 2
}
```
* a place must be a valid gallery from the https://api.artic.edu/docs/#galleries
* duplicated places are not allowed
* maximum 10 places allowed per project

## `project/<project_id>/place/<place_id>/`
### `GET`
Return a place by its ID for the given project. With additional information such notes and visiting status.

**Body**: None

**Return value**:

*Status code*: `200`

```json
{
    "id": 22,
    "notes": null,
    "visited": false,
    "project": 4,
    "place": 10
}
```

## `project/<project_id>/place/<place_id>/notes/`
### `PATCH`
Update the note of the place for the specific project.

**Body**:
```json
{
    "notes": "New text for the note."
}
```

**Return value**: Project-Place pair with updated data.

*Status code*: `200`

```json
{
    "id": 12,
    "notes": "New text for the note.",
    "visited": false,
    "project": 2,
    "place": 6
}
```

## `project/<project_id>/place/<place_id>/visit/`
### `PATCH`
Toggle `visit` status for the given place.

**Body**: None

**Return value**: Project-Place pair with updated data.

*Status code*: `200`

```json
{
    "id": 12,
    "notes": "New text for the note.",
    "visited": true,
    "project": 2,
    "place": 6
}
```

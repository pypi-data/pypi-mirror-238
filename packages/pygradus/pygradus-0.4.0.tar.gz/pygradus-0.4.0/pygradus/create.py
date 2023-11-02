from getpass import getpass
from pygradus.config import settings as st
from pygradus.api import send_request


def create_exercise(username, config, url=st.BASE_URL):

    password = getpass()
    login_data = {"username": username, "password": password}
    r = send_request("token", url, data=login_data)
    if r.status_code == 200:
        token = f"Bearer {r.json()['access_token']}"
    else:
        raise Exception(r.text)

    # Get existing user data
    r = send_request("users", url, token=token)
    if r.status_code == 200:
        user_data = r.json()
    else:
        raise Execption("Failed to get user data")

    course = config["course_name"]
    my_course = {}
    for c in user_data["courses"]:
        if course == c["name"]:  # the course is already mine
            my_course = c
            break
    else:
        course = {"name": course}
        r = send_request("course", url, json=course, token=token)
        if r.status_code != 200:
            return r.text

        my_course = r.json()

    exercise = config["exercise_name"]
    data = {"course_name": course, "name": exercise}
    my_exercise = {}
    for ex in my_course["exercises"]:
        if exercise == ex["name"]:
            my_exercise = ex
            break
    else:
        r = send_request("exercise", url, json=data, token=token)
        if r.status_code != 200:
            return r.text
        my_exercise = r.json()

    tasks = config["tasks"]
    my_tasks = my_exercise["tasks"]
    data = {"course_name": course, "exercise_name": exercise}
    for t in tasks:
        payload = {
            **data,
            **t,
            "disabled": False,
        }
        r = send_request("task", url, json=payload, token=token)
        if r.status_code != 200:
            return r.text

    # disable missing tasks
    new_tasks_names = [t["name"] for t in tasks]
    for t in my_tasks:
        if t["name"] not in new_tasks_names:
            payload = {
                **t,
                "disabled": True,
            }
            r = send_request("task", url, json=payload, token=token)
            if r.status_code != 200:
                return r.text

    r = send_request("users", url, token=token)
    if r.status_code == 200:
        user_data = r.json()
        print("Exercise correctly updated")
    else:
        return r.text

    return user_data

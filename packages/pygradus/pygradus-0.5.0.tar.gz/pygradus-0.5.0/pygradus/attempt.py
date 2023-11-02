from pygradus.api import send_request
from pygradus.config import settings as st


def check_solution(proposal, url=st.BASE_URL):

    r = send_request("attempt", url, json=proposal)
    if r.status_code != 200:
        return r.text
    res = r.json()

    max_len = 50
    answers = res["task_attempts"]
    title = f"Total Correct Answers {res['total_correct']} / {len(answers)}"
    row = f"|{{0:^{max_len}}}|{{1:^20}}|"
    sep = row.format("-" * max_len, "-" * 20)
    print(row.format("Task Name", "Status"))
    print(sep)
    print(sep)
    for a in answers:
        print(
            row.format(
                a["name"][:max_len], "Correct" if a["is_correct"] else "Incorrect"
            )
        )
        print(sep)

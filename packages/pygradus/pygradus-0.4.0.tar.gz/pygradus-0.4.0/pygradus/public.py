import re
import json
from pathlib import Path
import nbformat.v4 as nbf
from nbformat import write as nbf_write

from pygradus.config import settings as st

start_re = re.compile(st.START_RE)
end_re = re.compile(st.END_RE)
delete_re = re.compile(st.DEL_RE)
tasks_re = re.compile(st.TASKS_RE)


def public_version(input: str, output: str):

    filename = Path(input)
    with open(filename, "r") as fh:
        data = json.load(fh)

    cells = data["cells"]

    nb = nbf.new_notebook()

    tasks_content = None
    new_cells = []
    for c in cells:
        src = c["source"]
        start = None
        end = None
        delete = False
        tasks = False
        for i, l in enumerate(src):
            # print(i, l)
            if start_re.search(l):
                start = i
            if end_re.search(l):
                end = i
            if delete_re.search(l):
                delete = True
            if tasks_re.search(l):
                tasks = True

        if start is not None and end is not None:
            new_src = src[:start] + ["    # Write your code here\n"] + src[end + 1 :]
        else:
            new_src = src

        if tasks:
            tasks_content = src

        if delete or tasks:
            pass
        elif c["cell_type"] == "markdown":
            cell = nbf.new_markdown_cell(new_src)
            new_cells.append(cell)
        elif c["cell_type"] == "code":
            cell = nbf.new_code_cell(new_src)
            new_cells.append(cell)

    tasks_content = "".join(tasks_content[1:]).replace("TASKS = ", "")

    submission = f"""
proposed_solution = {{
        'attempt': {{
        'course_name': COURSE_NAME,
        'exercise_name': EXERCISE_NAME,
        'username': STUDENT_NAME,
    }},
    'task_attempts': {tasks_content}

    }}
import pygradus as gr
gr.check_solution(proposed_solution)
    """
    cell = nbf.new_code_cell(submission)
    new_cells.append(cell)

    nb["cells"] = new_cells

    with open(output, "w") as f:
        nbf_write(nb, f, 4)


if __name__ == "__main__":
    import sys

    input = sys.argv[1]
    output = sys.argv[2]
    public_version(input, output)

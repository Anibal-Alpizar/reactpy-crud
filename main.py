from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, html, use_state
import reactpy
from uuid import uuid4


@component
def App():
    tasks, setTasks = use_state([])
    title, setTitle = use_state("")
    description, setDescription = use_state("")
    editing, setEditing = use_state(False)
    task_id, set_task_id = use_state(None)

    @reactpy.event(prevent_default=True)
    def handle_submit(e):
        if not title or not description:
            return
        if not editing:
            new_task = {
                "title": title,
                "description": description,
                "id": uuid4(),
            }
            setTasks(tasks + [new_task])

        else:
            updated_tasks = [task if task['id'] != task_id else {
                "title": title,
                "description": description,
                "id": task_id,
            } for task in tasks]
            setTasks(updated_tasks)

        setTitle("")
        setDescription("")
        setEditing(False)
        set_task_id(None)

    def handle_delete(id):
        filtered_tasks = [task for task in tasks if task['id'] != id]
        setTasks(filtered_tasks)

    def handle_edit(task):
        print(task)
        setTitle(task['title'])
        setDescription(task['description'])
        setEditing(True)
        set_task_id(task['id'])

    list_items = [html.li(
        f"{task['title']} - {task['description']}",
        html.p(task['id']),
        html.button({
            "on_click": lambda e, task_id=task['id']: handle_delete(task_id),
        }, 'Delete'),
        html.button({
            "on_click": lambda e, task=task: handle_edit(task)
        }, 'Edit'),
    ) for task in tasks]

    return html.div(
        html.form(
            {
                "onsubmit": handle_submit,
            },
            html.input({
                "type": "text",
                "placeholder": "Write a title",
                "onchange": lambda e: setTitle(e["target"]["value"]),
                "value": title,
                "auto_focus": True
            }),
            html.textarea({
                "placeholder": "Write a description",
                "on_change": lambda e: setDescription(e["target"]["value"]),
                "value": description,
            }),
            html.button("Create task" if not editing else "Update task"),
        ),
        html.ul(list_items),
    )


app = FastAPI()

configure(app, App)

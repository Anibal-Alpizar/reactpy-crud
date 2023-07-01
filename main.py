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

    @reactpy.event(prevent_default=True)
    def handle_submit(e):
        print(title)
        print(description)
        new_task = {
            "title": title,
            "description": description,
            "id": uuid4(),
        }
        # print(new_task)
        setTasks(tasks + [new_task])

    list_items = [html.li(
        f"{task['title']} - {task['description']}",
        html.button('Delete'),
        html.button('Edit'),
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
            }),
            html.textarea({
                "placeholder": "Write a description",
                "on_change": lambda e: setDescription(e["target"]["value"]),
            }),
            html.button("Create task"),
        ),
        html.ul(list_items),
    )


app = FastAPI()

configure(app, App)

from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, html


@component
def App():
    return html.div("Hello World")


app = FastAPI()

configure(app, App)

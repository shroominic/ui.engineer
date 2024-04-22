import funcchain
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html, AnyComponent, FastUI
from fastui import components as c, events as e
from langchain_groq import ChatGroq
from typing import Annotated

from .simple_fastui import AnyComponent as _AnyComponent, render

funcchain.settings.llm = ChatGroq(model="llama3-70b-8192")
funcchain.settings.console_stream = True

app = FastAPI()

db: dict[str, list[_AnyComponent]] = {}


async def generate_app(app_name: str) -> list[_AnyComponent]:
    """
    Generate a plain app based on the given app name.
    Do not insert default data or demo values.
    Give every component proper bootstrap classes.
    """
    return await funcchain.achain()


async def update_app(
    app_name: str, state: str, update_instructions: str
) -> list[_AnyComponent]:
    """
    This is the current UI state of the app {{ app_name }}:
    {{ state }}

    Respond with and updated state of the ui based on the given update instructions:
    {{ update_instructions }}
    """
    return await funcchain.achain()


@app.get("/api/{app_name}", response_model=FastUI, response_model_exclude_none=True)
async def show(app_name: str, action: str | None = None) -> list[AnyComponent]:
    """
    Show state of UI from database or generate a new one based on the url.
    e.g.: http://127.0.0.1:8000/todo-list
    """
    if not (state := db.get(app_name)):
        state = await generate_app(app_name)

    elif action:
        state = await update_app(app_name, repr(state), action)

    db[app_name] = state
    return render(state, app_name)


@app.post("/api/{app_name}", response_model=FastUI, response_model_exclude_none=True)
async def update(app_name: str, request: Request) -> list[AnyComponent]:
    form_fields = await request.form()

    if not db[app_name]:
        raise HTTPException(detail="App not found", status_code=404)

    return [
        c.FireEvent(
            event=e.GoToEvent(url=f"/{app_name}", query={"action": repr(form_fields)})
        )
    ]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def index() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.PageTitle(text="👨🏼‍🔬 UI Engineer"),
                c.Paragraph(
                    text="This is a playground for the ai rendered user interfaces."
                ),
                c.Form(
                    form_fields=[
                        c.FormFieldInput(name="app_name", title="App Description"),
                    ],
                    submit_url="",
                ),
            ],
            class_name="container",
        )
    ]


@app.post("/", response_model=FastUI, response_model_exclude_none=True)
async def create_app(app_name: Annotated[str, Form()]) -> list[AnyComponent]:
    return [
        c.FireEvent(
            event=e.GoToEvent(
                url=f"/{app_name.replace(' ', '-')}",
            )
        )
    ]


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """fastui runtime"""
    return HTMLResponse(prebuilt_html(title="FastUI AI"))


def main():
    try:
        import uvicorn, webbrowser  # noqa

        webbrowser.open("http://127.0.0.1:8000/")
        uvicorn.run(app)
    except ImportError:
        print("missing uvicorn, do pip install uvicorn")


if __name__ == "__main__":
    main()

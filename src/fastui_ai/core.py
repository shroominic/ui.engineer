from typing import Annotated
from fastapi import FastAPI, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastui import prebuilt_html, AnyComponent, FastUI
from fastui import components as c
from funcchain import achain, settings

from .component_types import SimpleComponents, convert_to_fastui

settings.llm = "gpt-4-turbo-preview"
settings.console_stream = True

UI_ROOT = "/ui"


app = FastAPI()

ui = APIRouter(prefix=UI_ROOT, tags=["UI"])


@ui.get("/", response_model=FastUI, response_model_exclude_none=True)
async def index() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Form(
                    method="POST",
                    submit_url="/ui/generate",
                    form_fields=[
                        c.FormFieldInput(title="Create App", name="instruction")
                    ],
                )
            ],
        ),
    ]


async def generate_app(instruction: str) -> list[SimpleComponents]:
    """
    Generate an app based on the given instruction.
    """
    return await achain()


@ui.post("/generate", response_model=FastUI, response_model_exclude_none=True)
async def generate(
    instruction: Annotated[str, Form()],
) -> list[AnyComponent]:
    return convert_to_fastui(await generate_app(instruction))


app.include_router(ui)


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    return HTMLResponse(
        prebuilt_html(
            title="FastUI AI",
            api_root_url=UI_ROOT,
        )
    )

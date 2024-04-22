"""
simplified versions of the fastui component types
this helps the language model better understand the structure of the components
so it can build more accurate ui structures

using native fastui components bloats the function calling json schema
because there are many cross references between the components
but we can maybe solve this differently feel free to change this if you have a better idea
"""

from typing import Union
from pydantic import BaseModel, Field
from fastui.components import AnyComponent as FastUIAnyComponent
from fastui import components as c, events as e


class Text(BaseModel):
    text_content: str = Field(description="Content of simple text component.")


class StyledComponent(BaseModel):
    bootstrap_class_names: str = Field(
        description="Optional bootstrap class names for styling."
    )


class Button(StyledComponent):
    text_content: str = Field(description="Button text.")
    on_click_action: str = Field(
        description="Description of what happens to the app when the button is clicked."
    )


class InputField(StyledComponent):
    """Form to input data (already includes submit button)"""

    label: str = Field(description="Label for the input field.")
    placeholder: str = Field(description="Placeholder text for the input field.")
    on_submit_action: str = Field(
        description=(
            "Description of what happens to the app state when the input field is submitted."
            "Encode the action description as url safe string."
        )
    )
    submit_button_label: str = Field(description="Label for the submit button.")


class Link(StyledComponent):
    text_content: str = Field(description="Link text.")
    on_click_action: str = Field(
        description=(
            "Description of what happens to the app when the link is clicked."
            "Encode the action description as url safe string."
        )
    )


class Container(StyledComponent):
    components: list["AnyComponent"]


AnyComponent = Union[Button, Text, InputField, Link, Container]


def render(components: list[AnyComponent], app_name: str) -> list[FastUIAnyComponent]:
    """
    Convert a list of simplified components into actual fastui components.
    """
    fastui_components: list[FastUIAnyComponent] = []
    for component in components:
        if isinstance(component, Button):
            fastui_components.append(
                c.Button(
                    text=component.text_content,
                    class_name=component.bootstrap_class_names,
                    on_click=e.GoToEvent(
                        url=f"/{app_name}?action={component.on_click_action}"
                    ),
                )
            )

        elif isinstance(component, Text):
            fastui_components.append(c.Text(text=component.text_content))

        elif isinstance(component, InputField):
            fastui_components.append(
                c.Form(
                    loading=[c.Spinner()],
                    submit_url=f"/api/{app_name}",
                    submit_trigger=e.PageEvent(
                        name=component.on_submit_action,
                        next_event=e.GoToEvent(
                            url=f"/{app_name}?action={component.on_submit_action}"
                        ),
                    ),
                    form_fields=[
                        c.FormFieldInput(
                            title="Update instructions",
                            name="update_instructions",
                            initial=component.on_submit_action,
                            class_name="d-none",
                        ),
                        c.FormFieldInput(
                            name=component.label,
                            title=component.placeholder,
                            class_name=component.bootstrap_class_names,
                        ),
                    ],
                )
            )

        elif isinstance(component, Link):
            fastui_components.append(
                c.Link(
                    components=[c.Text(text=component.text_content)],
                    class_name=component.bootstrap_class_names,
                    on_click=e.GoToEvent(
                        url=f"/{app_name}?action={component.on_click_action}"
                    ),
                )
            )

        elif isinstance(component, Container):
            fastui_components.append(
                c.Div(
                    components=render(component.components, app_name=app_name),
                    class_name=component.bootstrap_class_names,
                )
            )
        else:
            raise ValueError(f"Unknown component type: {component}")
    return fastui_components

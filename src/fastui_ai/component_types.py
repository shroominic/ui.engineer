from typing import Union
from pydantic import BaseModel, Field
from fastui.components import AnyComponent as FastUIComponent
from fastui import components as c


class Text(BaseModel):
    text: str = Field(description="Content of simple text component.")


class StyledComponent(BaseModel):
    class_name: str = Field(description="Optional bootstrap class names for styling.")


class Button(StyledComponent):
    text: str
    on_click_action: str = Field(
        description="Description of what happens to the app when the button is clicked."
    )


class InputField(StyledComponent):
    label: str
    placeholder: str
    on_change_action: str = Field(
        description="Description of what happens to the app when the input field is changed."
    )


class Link(StyledComponent):
    text: str
    on_click_action: str = Field(
        description="Description of what happens to the app when the link is clicked."
    )


class Div(StyledComponent):
    components: list["SimpleComponents"]


SimpleComponents = Union[Button, Text, InputField, Link, Div]


def convert_to_fastui(components: list[SimpleComponents]) -> list[FastUIComponent]:
    fastui_components: list[FastUIComponent] = []
    for component in components:
        if isinstance(component, Button):
            fastui_components.append(
                c.Button(
                    text=component.text,
                    class_name=component.class_name,
                    # on_click_action=component.on_click_action,
                )
            )
        elif isinstance(component, Text):
            fastui_components.append(c.Text(text=component.text))
        elif isinstance(component, InputField):
            fastui_components.append(
                c.Form(
                    submit_url="/update",
                    form_fields=[
                        c.FormFieldInput(
                            name=component.label,
                            title=component.placeholder,
                            class_name=component.class_name,
                            # on_change_action=component.on_change_action,
                        )
                    ],
                )
            )
        elif isinstance(component, Link):
            fastui_components.append(
                c.Link(
                    components=[c.Text(text=component.text)],
                    class_name=component.class_name,
                    # on_click_action=component.on_click_action,
                )
            )
        elif isinstance(component, Div):
            fastui_components.append(
                c.Div(
                    components=convert_to_fastui(component.components),
                    class_name=component.class_name,
                )
            )
        else:
            raise ValueError(f"Unknown component type: {component}")
    return fastui_components

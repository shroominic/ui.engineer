"""
simplified versions of the fastui component types
this helps the language model better understand the structure of the components
so it can build more accurate ui structures

using native fastui components bloats the function calling json schema
because there are many cross references between the components
but we can maybe solve this differently feel free to change this if you have a better idea
"""

from abc import ABC, abstractmethod
from typing import Union
from pydantic import BaseModel, Field
from fastui.components import AnyComponent as FastUIComponent
from fastui import components as c, events as e


class Component(BaseModel, ABC):
    class_name: str = Field(description="Optional bootstrap class names for styling.")

    @abstractmethod
    def to_fastui(self, **kwargs: str) -> FastUIComponent: ...


class Text(Component):
    text_content: str = Field(description="Content of simple text component.")

    def to_fastui(self, **kwargs: str) -> FastUIComponent:
        return c.Div(
            components=[c.Text(text=self.text_content)],
            class_name=self.class_name,
        )


class Button(Component):
    text_content: str = Field(description="Button text.")
    on_click_action: str = Field(
        description="Description of what happens to the app when the button is clicked."
    )

    def to_fastui(self, **kwargs: str) -> FastUIComponent:
        return c.Button(
            text=self.text_content,
            class_name=self.class_name,
            on_click=e.GoToEvent(
                url=f"/{kwargs.get('app_name')}?action={self.on_click_action}"
            ),
        )


class InputField(Component):
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

    def to_fastui(self, **kwargs: str) -> FastUIComponent:
        return c.Form(
            loading=[c.Spinner()],
            submit_url=f"/api/{kwargs.get('app_name')}",
            submit_trigger=e.PageEvent(
                name=self.on_submit_action,
                next_event=e.GoToEvent(
                    url=f"/{kwargs.get('app_name')}?action={self.on_submit_action}"
                ),
            ),
            form_fields=[
                c.FormFieldInput(
                    title="Update instructions",
                    name="update_instructions",
                    initial=self.on_submit_action,
                    class_name="d-none",
                ),
                c.FormFieldInput(
                    name=self.label,
                    title=self.placeholder,
                    class_name=self.class_name,
                ),
            ],
        )


class Link(Component):
    text_content: str = Field(description="Link text.")
    on_click_action: str = Field(
        description=(
            "Description of what happens to the app when the link is clicked."
            "Encode the action description as url safe string."
        )
    )

    def to_fastui(self, **kwargs: str) -> FastUIComponent:
        return c.Link(
            components=[c.Text(text=self.text_content)],
            class_name=self.class_name,
            on_click=e.GoToEvent(
                url=f"/{kwargs.get('app_name')}?action={self.on_click_action}"
            ),
        )


class Container(Component):
    """
    A container for other components. (div)
    For a vertical list of components, add the class_name "flex flex-col",
    a horizontal list: "flex flex-row", and so on...
    """

    components: list["AnyComponent"]

    def to_fastui(self, **kwargs: str) -> FastUIComponent:
        return c.Div(
            components=patch(self.components, **kwargs),
            class_name=self.class_name,
        )


AnyComponent = Union[Button, Text, InputField, Link, Container]


def patch(components: list[AnyComponent], app_name: str) -> list[FastUIComponent]:
    """
    Convert a list of simplified components into actual fastui components.
    """
    return [c.to_fastui(app_name=app_name) for c in components]

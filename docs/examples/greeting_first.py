from napolitan.core import Component, Attr, customElement
from napolitan.livingstandard import p


@customElement("my-greeting")
class Greeting(Component):
    name = Attr(str, "World")

    def render(self):
        # this is also ok
        # return p(cls="msg")(self.t("Hello, ${name}!"))
        return p(cls="msg")("Hello, ", self.name, "!")

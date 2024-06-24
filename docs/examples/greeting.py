from napolitan.core import Component, Attr, customElement
from napolitan.livingstandard import p


@customElement("my-greeting-with-blue-text")
class Greeting(Component):

    name = Attr(str, "World")

    @staticmethod
    def style():
        return """
        .msg {
            color: blue;
        }
        """

    def render(self):
        # this is also ok
        # return p(cls="msg")(self.t("Hello, ${name}!"))
        return p(cls="msg")("Hello, ", self.name, "!")

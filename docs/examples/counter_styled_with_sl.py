from napolitan.core import Component, Attr, customElement
from napolitan.livingstandard import div, span
from napolitan.shoelace import button, button_group, icon, card


@customElement("my-counter-styled-with-sl")
class Counter(Component):

    count = Attr(int, 0)

    @staticmethod
    def style():
        return """
        .counter {
            --padding: 1rem;
            --border-color: #1E2129;
        }
        .count {
            font-size: 3rem;
            font-weight: bold;
            color: #1E2129;
            display: flex;
            justify-content: center;
        }
        """

    def render(self):
        return card(cls="counter")(
            span(cls="count")(self.count),
            div(slot="footer", cls="footer")(
                button_group(label="btns")(
                    button(variant="primary", onclick=self.increment)(
                        icon(name="plus-lg")
                    ),
                    button(variant="primary", onclick=self.decrement)(
                        icon(name="dash-lg")
                    ),
                )
            ),
        )

    def increment(self, e):
        self.count += 1

    def decrement(self, e):
        self.count -= 1

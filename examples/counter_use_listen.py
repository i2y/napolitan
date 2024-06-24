from napolitan.core import Component, Attr, customElement, listen
from napolitan.livingstandard import div, span
from napolitan.shoelace import button, button_group, icon, card


@customElement("my-counter-use-listen")
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

    # def render(self):
    #     return card(cls="counter")(
    #         span(cls="count")(self.count),
    #         div(slot="footer")(
    #             button_group(label="btns")(
    #                 button(cls="inc", variant="primary")(
    #                     icon(name="plus-lg"),
    #                 ),
    #                 button(cls="dec", variant="primary")(icon(name="dash-lg")),
    #             )
    #         ),
    #     )

    def render(self):
        return self.html(
            f"""<sl-card class="counter">
            <span class="count">$[count]</span>
            <div slot="footer">
                <sl-button-group label="btns">
                    <sl-button class="inc" variant="primary">
                        <sl-icon name="plus-lg"></sl-icon>
                    </sl-button>
                    <sl-button class="dec" variant="primary">
                        <sl-icon name="dash-lg"></sl-icon>
                    </sl-button>
                </sl-button-group>
            </div>
        </sl-card>"""
        )

    @listen("click", ".inc")
    def increment(self, e):
        self.count += 1

    @listen("click", ".dec")
    def decrement(self, e):
        self.count -= 1

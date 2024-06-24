from napolitan.core import Component, Attr, customElement
from napolitan.livingstandard import div, button


@customElement("my-counter-not-styled")
class Counter(Component):

    count = Attr(int, 0)

    def render(self):
        return div()(
            button(onclick=self.increment)("Increment"),
            self.count,
            button(onclick=self.decrement)("Decrement"),
        )

    def increment(self, _):
        self.count += 1

    def decrement(self, _):
        self.count -= 1

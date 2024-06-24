from napolitan.core import State, Component, customElement
from napolitan.nord import button, icon, stack


@customElement("my-counter")
class Counter(Component):

    count = State(int, 0)

    def render(self):
        return stack(direction="horizontal", align_items="center")(
            button("square", onclick=self.increment)(
                icon(name="interface-add"),
            ),
            self.count,
            button("square", onclick=self.decrement)(
                icon(name="interface-remove"),
            ),
        )
        # The code above is equivalent to the following commented out code
        # return """
        # <nord-stack direction="horizontal" align-items="center">
        #     <nord-button class="inc" variant="square">
        #         <nord-icon name="interface-add"></nord-icon>
        #     </nord-button>
        #     $[count]
        #     <nord-button class="dec" variant="square">
        #         <nord-icon name="interface-remove"></nord-icon>
        #     </nord-button>
        # </nord-stack>
        # """

    # @listen("click", ".inc")
    def increment(self, _):
        self.count += 1

    # @listen("click", ".dec")
    def decrement(self, _):
        self.count -= 1

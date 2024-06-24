Napolitan is a lightweight, user-friendly library for creating custom elements with a simple API for PyScript. It uses a declarative approach for easy component structure definition and updates only changed parts of the DOM for efficiency. It works with both Pyodide and MicroPython, using only the language features and built-in libraries supported by both, intentionally avoiding certain modules like typing and metaclasses. Based on Web Components, probably, Napolitan works with any PyScript, JavaScript, or TypeScript framework.

## Quick Look
<link rel="stylesheet" href="https://pyscript.net/releases/2024.4.1/core.css">
<script type="module" src="https://pyscript.net/releases/2024.4.1/core.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.15.1/cdn/themes/light.css" />
<script type="module" src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.15.0/cdn/shoelace.js"></script>
<link rel="stylesheet" href="https://nordcdn.net/ds/css/3.2.0/nord.min.css"
integrity="sha384-x2XdCI8Yog7KGRmrrGLegjFrrIYXEhGNxql/xEXdMoW5NkpEhlAkUHdQJxkL1vPg" crossorigin="anonymous" />
<script type="module" src="https://nordcdn.net/ds/components/3.11.1/index.js" integrity="sha384-0BctO4fitxuXRemuc9/T9rR9jUz7iqugmJhzcvRiNzotBtKKGUWfFmr9b7wMgeZi" crossorigin="anonymous"></script>

<style>
  :root {
    /* CUSTOM ACCENT COLORS */
    --n-color-accent: tomato;

    --md-primary-fg-color: tomato;
  }
</style>

<script type="mpy" src="examples/counter_not_styled.py" config="examples/pyscript.toml"></script>
<script type="mpy" src="examples/counter.py" config="examples/pyscript.toml"></script>
<script type="mpy" src="examples/counter_styled_with_sl.py" config="examples/pyscript.toml"></script>
<script type="mpy" src="examples/counter_use_listen.py" config="examples/pyscript.toml"></script>


### Example: Counter (Not Styled)
=== "Python"
    ```python
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
    ```

=== "HTML"
    ```html
    <my-counter-not-styled count="0"></my-counter-not-styled>
    ```

=== "Result"
    <my-counter-not-styled count="0"></my-counter-not-styled>


### Example: Counter (Styled using Shoelace)
!!! info
    "+" annotations in this example explain each part of the code well, so could please click "+" if you want to know the details.

=== "Python"
    ```python
    from napolitan.core import Component, Attr, customElement
    from napolitan.livingstandard import div, span
    from napolitan.shoelace import button, button_group, icon, card


    @customElement("my-counter")  #(1)
    class Counter(Component): #(2)

        count = Attr(int, 0) #(3)

        @staticmethod
        def style(): #(4)
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

        def render(self): #(5)
            return card(cls="counter")(
                span(cls="count")(self.count),
                div(slot="footer", cls="footer")(
                    button_group(label="btns")(
                        button(variant="primary", onclick=self.increment)( #(8)
                            icon(name="plus-lg")
                        ),
                        button(variant="primary", onclick=self.decrement)( #(9)
                            icon(name="dash-lg")
                        ),
                    )
                ),
            )

        def increment(self, e): #(6)
            self.count += 1

        def decrement(self, e): #(7)
            self.count -= 1
    ```

    1.  Register the component with the name `my-counter` as a custom element.
    2.  Define the `Counter` class that extends the `Component` class.
    3.  Define a `count` attrerty with a default value of `0`.
        The `Attr` class is used to define a attrerty of the component.
        The `Attr` class takes two arguments: the type of the attrerty and the default value.
        `my-counter` custom element can be used with the `count` attribute.
        If you want to use the `count` as an internal state, you can define it using `State` class instead of using `Attr` class. If you use `State` class, the `count` will not be related to the `count` attribute of the `my-counter` custom element.
    4.  Define the `style` method to return the CSS styles for the component.
    5.  Define the `render` method to return the HTML structure of the component.
        Napolitan provides some sets of helper functions to create DOM elements and factory class to create a helper function for any DOM element as well. Here, `sl_card`, `sl_button`, `sl_button_group`, and `sl_icon` are helper functions to create Shoelace components. Napolitan currently provides a set of helper functions to create Shoelace components, HTML Living Standard elements, and Nord components. And also, you can use HTML tags text directly to create DOM elements, please refer to examples directory in the Napolitan repository, if you are interested in that.
    6.  Define the `increment` method to increment the `count` attrerty.
        When `count` attrerty is updated, the only `count` span will be re-rendered automatically.
    7.  Define the `decrement` method to decrement the `count` attrerty.
        When `count` attrerty is updated, the only `count` span will be re-rendered automatically.
    8.  Add an event listener to the `+` button click to call the `increment` method.
    9.  Add an event listener to the `-` button click to call the `decrement` method.

=== "HTML"
    ```html
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.15.0/cdn/themes/light.css" />
    <script type="module" src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.15.0/cdn/shoelace.js"></script>
    <script type="mpy" src="examples/counter.py" config="examples/pyscript.toml"></script>
    <my-counter count="10"></my-counter>
    ```

=== "Result"
    <my-counter-styled-with-sl count="10"></my-counter-styled-with-sl>


### Example: Counter (Used `listen` decorator for event handling)
=== "Python"
    ```python
    from napolitan.core import Component, Attr, customElement, track_method_calls, listen
    from napolitan.livingstandard import div, span
    from napolitan.shoelace import sl_button, sl_button_group, sl_icon, sl_card


    @customElement("my-counter-use-listen")
    class Counter(Component):

        count = Attr(int, 0)

        @staticmethod
        def style():
            return """
            :host {
                display: flex;
                width: fit-content;
                height: fit-content;
            }
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
            .counter [slot='footer'] {
                display: flex;
                justify-content: center;
            }
            """

        def render(self):
            return sl_card(cls="counter")(
                span(cls="count")(self.count),
                div(slot="footer")(
                    sl_button_group(label="btns")(
                        sl_button(cls="inc", variant="primary")(
                            sl_icon(name="plus-lg"),
                        ),
                        sl_button(cls="dec", variant="primary")(
                            sl_icon(name="dash-lg")
                        ),
                    )
                ),
            )

        @listen("click", ".inc")
        def increment(self, e):
            self.count += 1

        @listen("click", ".dec")
        def decrement(self, e):
            self.count -= 1
    ```

=== "HTML"
    ```html
    <script type="mpy" src="examples/counter_use_listen.py" config="examples/pyscript.toml"></script>
    <my-counter-use-listen count="20"></my-counter-use-listen>
    ```

=== "Result"
    <my-counter-use-listen count="20"></my-counter-use-listen>

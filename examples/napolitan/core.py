from pyscript import window, document
from pyscript.ffi import to_js, create_proxy


try:
    import ure as re
except ImportError:
    import re


class HTMLParser:
    def __init__(self):
        self.reset()

    def reset(self):
        self._data = []
        self._stack = []
        self._variables = {}

    def set_variables(self, variables):
        self._variables = variables

    def feed(self, html):
        pos = 0
        while pos < len(html):
            if html[pos] == "<":
                end_pos = html.find(">", pos)
                if end_pos == -1:
                    break
                self.handle_tag(html[pos : end_pos + 1])
                pos = end_pos + 1
            else:
                end_pos = html.find("<", pos)
                if end_pos == -1:
                    self.handle_data(html[pos:])
                    break
                self.handle_data(html[pos:end_pos])
                pos = end_pos
        retval = self._data
        self.reset()
        return retval

    def handle_tag(self, tag):
        is_closing_tag = tag.startswith("</")
        tag_content = tag[1:-1].strip() if not is_closing_tag else tag[2:-1].strip()

        if is_closing_tag:
            self.end_tag(tag_content)
        else:
            if " " in tag_content:
                tag_name, attr_string = tag_content.split(" ", 1)
                attrs = self.parse_attributes(attr_string)
            else:
                tag_name = tag_content
                attrs = {}
            self.start_tag(tag_name, attrs)

    def handle_data(self, data):
        if data.strip():
            self.process_text(data.strip())

    def process_text(self, text):
        while "$[" in text:
            start = text.find("$[")
            end = text.find("]", start)
            if end == -1:
                break
            varname = text[start + 2 : end]
            before = text[:start]
            after = text[end + 1 :]
            if before:
                self._stack[-1]["children"].append(_TextElement(before))
            if varname in self._variables:
                v = self._variables[varname]
                if isinstance(v, State):
                    self._stack[-1]["children"].append(v)
                else:
                    self._stack[-1]["children"].append(
                        _TextElement(str(self._variables[varname]))
                    )
            text = after
        if text:
            self._stack[-1]["children"].append(_TextElement(text))

    def parse_attributes(self, attr_string):
        attrs = {}
        attr_string = attr_string.strip()
        while attr_string:
            if "=" in attr_string:
                attr, rest = attr_string.split("=", 1)
                attr = attr.strip()
                if rest[0] in ('"', "'"):
                    quote = rest[0]
                    end_quote_pos = rest.find(quote, 1)
                    value = rest[1:end_quote_pos]
                    rest = rest[end_quote_pos + 1 :].strip()
                else:
                    space_pos = rest.find(" ")
                    if space_pos == -1:
                        value = rest
                        rest = ""
                    else:
                        value = rest[:space_pos]
                        rest = rest[space_pos + 1 :].strip()
                attrs[attr] = value
                attr_string = rest
            else:
                space_pos = attr_string.find(" ")
                if space_pos == -1:
                    attrs[attr_string.strip()] = None
                    break
                else:
                    attrs[attr_string[:space_pos].strip()] = None
                    attr_string = attr_string[space_pos + 1 :].strip()
        return attrs

    def start_tag(self, tag, attrs):
        element = {"name": tag, "nameattrs": [], "kwattrs": attrs, "children": []}
        self._stack.append(element)

    def end_tag(self, tag):
        if self._stack and self._stack[-1]["name"] == tag:
            element = self._stack.pop()
            template_element = _TemplateElement(
                element["name"],
                element["nameattrs"],
                element["kwattrs"],
                *element["children"],
            )
            if self._stack:
                self._stack[-1]["children"].append(template_element)
            else:
                self._data.append(template_element)


class TextParser:
    def __init__(self):
        self.reset()

    def reset(self):
        self._data = []
        # self._stack = []
        self._variables = {}

    def set_variables(self, variables):
        self._variables = variables

    def feed(self, html):
        self.handle_data(html)
        retval = self._data
        self.reset()
        return retval

    def handle_data(self, data):
        if data.strip():
            self.process_text(data.strip())

    def process_text(self, text):
        while "${" in text:
            start = text.find("${")
            end = text.find("}", start)

            if end == -1:
                break

            varname = text[start + 2 : end]
            before = text[:start]
            after = text[end + 1 :]

            if before:
                self._data.append(_TextElement(before))

            if varname in self._variables:
                v = self._variables[varname]

                if isinstance(v, State):
                    self._data.append(v)
                else:
                    self._data.append(_TextElement(str(self._variables[varname])))

            text = after

        if text:
            self._data.append(_TextElement(text))


class State:
    def __init__(self, conv, v=None):
        self._convert = conv
        self._value = conv(v)
        self._observers = []
        self._owner = None

    def clone(self):
        return State(self._convert, self._value)

    def set_owner(self, owner):
        self._owner = owner

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        cv = self._convert(v)
        if self._value != cv:
            self._value = cv
            self.notify_observers()

    def notify_observers(self):
        if len(self._observers) == 0 and self._owner is not None:
            self._owner.update()
            return

        for observer in self._observers:
            observer.reaction(self._value)

    def __iadd__(self, other):
        if isinstance(other, State):
            self.value += other.value
        else:
            self.value += other
        return self

    def __isub__(self, other):
        if isinstance(other, State):
            self.value -= other.value
        else:
            self.value -= other
        return self

    def __imul__(self, other):
        if isinstance(other, State):
            self.value *= other.value
        else:
            self.value *= other
        return self

    def __itruediv__(self, other):
        if isinstance(other, State):
            self.value /= other.value
        else:
            self.value /= other
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, State):
            self.value //= other.value
        else:
            self.value //= other
        return self

    def __imod__(self, other):
        if isinstance(other, State):
            self.value %= other.value
        else:
            self.value %= other
        return self

    def __ipow__(self, other):
        if isinstance(other, State):
            self.value **= other.value
        else:
            self.value **= other
        return self

    def __ilshift__(self, other):
        if isinstance(other, State):
            self.value <<= other.value
        else:
            self.value <<= other
        return self

    def __irshift__(self, other):
        if isinstance(other, State):
            self.value >>= other.value
        else:
            self.value >>= other
        return self

    def __iand__(self, other):
        if isinstance(other, State):
            self.value &= other.value
        else:
            self.value &= other
        return self

    def __ixor__(self, other):
        if isinstance(other, State):
            self.value ^= other.value
        else:
            self.value ^= other
        return self

    def __ior__(self, other):
        if isinstance(other, State):
            self.value |= other.value
        else:
            self.value |= other
        return self

    def __lt__(self, other):
        if isinstance(other, State):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, State):
            return self.value <= other.value
        return self.value <= other

    def __eq__(self, other):
        if isinstance(other, State):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        if isinstance(other, State):
            return self.value != other.value
        return self.value != other

    def __gt__(self, other):
        if isinstance(other, State):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, State):
            return self.value >= other.value
        return self.value >= other

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __hash__(self):
        return hash(self.value)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __delitem__(self, key):
        self.value.__delitem__(key)

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, item):
        return item in self.value

    def __reversed__(self):
        return reversed(self.value)

    def __add__(self, other):
        if isinstance(other, State):
            return CombinedState(self, other)
        self.value += other
        return self

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __floordiv__(self, other):
        return self.value // other

    def __mod__(self, other):
        return self.value % other

    def __pow__(self, other):
        return self.value**other

    def __and__(self, other):
        return self.value & other

    def __xor__(self, other):
        return self.value ^ other

    def __or__(self, other):
        return self.value | other

    def __lshift__(self, other):
        return self.value << other

    def __rshift__(self, other):
        return self.value >> other

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value


class Attr(State):
    pass


class CombinedState(State):
    def __init__(self, first, second):
        first.add_observer(self)
        second.add_observer(self)
        self._value = first.value + second.value
        self._first = first
        self._second = second

    def reaction(self, value):
        self._value = self._first.value + self._second.value
        self.notify_observers()


# from collections.abc import Iterable


def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


class _TemplateElement:
    def __init__(self, name, nameattrs, kwattrs, *children):
        self._name = name
        self._nameattrs = nameattrs
        self._kwattrs = kwattrs
        self._children = flatten(children)
        self._elem = None

    def dom(self):
        elem = document.createElement(self._name)
        self._elem = elem
        return self._build()

    def _build(self):
        elem = self._elem
        for a in self._nameattrs:
            elem.setAttribute(a, "")

        for k, v in self._kwattrs.items():
            if k.startswith("on") and callable(v):
                elem.addEventListener(k[2:], create_proxy(v))
            else:
                if isinstance(v, State):
                    v.add_observer(self)
                    v = v.value
                if k == "cls":
                    k = "class"
                k = k.replace("_", "-")
                elem.setAttribute(k, v)

        for c in self._children:
            elem.appendChild(_dom(c))

        return elem

    def __str__(self):
        return self.dom().outerHTML

    def reaction(self, value):
        self._elem.innerHTML = ""
        self._build()


class _TemplateElementFactory:
    def __init__(self, name, args, kwargs):
        self._name = name.replace("_", "-")
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *children):
        return _TemplateElement(self._name, self._args, self._kwargs, *children)

    def __str__(self):
        return str(self.dom())

    def dom(self):
        return _TemplateElement(self._name, self._args, self._kwargs).dom()


class TemplateElementFactory:
    def __init__(self):
        pass

    def __getattr__(self, name):
        def factoryfactory(*args, **kwargs):
            return _TemplateElementFactory(name, args, kwargs)

        return factoryfactory


class _TextElement:
    def __init__(self, text):
        self._elem = document.createTextNode(text)

    def dom(self):
        return self._elem

    def __str__(self):
        return self.dom().textContent

    def reaction(self, value):
        self._elem.textContent = str(value)


def _dom(w):
    if isinstance(w, str):
        return document.createTextNode(w)
    elif isinstance(w, State):
        t = _TextElement(str(w.value))
        w.add_observer(t)
        return t.dom()
    else:
        return w.dom()


class Component:

    def __init__(self):
        fields = {
            key: value
            for key, value in self.__class__.__dict__.items()
            if isinstance(value, State)
        }
        for key, field in fields.items():
            clone = field.clone()
            clone.set_owner(self)
            setattr(self, key, clone)
        self._elem = None

    @staticmethod
    def style():
        return ""

    def render(self):
        return ""

    @classmethod
    def observedAttributes(cls):
        return [key for key, value in cls.__dict__.items() if isinstance(value, Attr)]

    @classmethod
    def setup(cls, elem):
        self = cls()
        elem._self = self
        self._elem = elem
        self._mounted = False
        # for event, selector, listener in cls._event_listeners:
        #     elem.addEventListener(event, create_proxy(getattr(self, listener)), selector)

    def mount(self, root):
        if self._mounted:
            return

        style = document.createElement("style")
        style.innerHTML = self.style()
        rendered = self.render()
        content = _dom(self.html(rendered) if isinstance(rendered, str) else rendered)
        root.appendChild(style)
        root.appendChild(content)
        self._style = style
        self._content = content

        for event, selector, listener in self.__class__._event_listeners:
            children = root.querySelectorAll(selector)
            for c in children:
                c.addEventListener(event, create_proxy(getattr(self, listener)))

        self._mounted = True

    def unmount(self, root):
        if not self._mounted:
            return

        if hasattr(self, "_style") and self._style is not None:
            root.removeChild(self._style)
            self._style.remove()
            self._style = None

        if hasattr(self, "_content") and self._content is not None:
            root.removeChild(self._content)
            self._content.remove()
            self._content = None

        self._mounted = False

    def dispatchEvent(self, ev):
        self._elem.dispatchEvent(ev)

    @staticmethod
    def attrchanged(root, elem, attrName, newValue, oldValue):
        elem._self._attrchanged(root, elem, attrName, newValue, oldValue)

    def _attrchanged(self, root, elem, attrName, newValue, oldValue):
        if newValue == oldValue:
            return

        if not hasattr(self, attrName):
            return

        attr = getattr(self, attrName)
        if isinstance(attr, State):
            attr.value = newValue
        else:
            setattr(self, attrName, newValue)
            self.unmount(root)
            self.mount(root)

    def update(self):
        self.unmount(self._elem.shadowRoot)
        self.mount(self._elem.shadowRoot)

    @staticmethod
    def connected(elem):
        elem._self.mount(elem.shadowRoot)

    @staticmethod
    def disconnected(elem):
        elem._self.unmount(elem.shadowRoot)

    @staticmethod
    def adopted(elem): ...

    def html(self, html_str):
        parser = HTMLParser()
        parser.set_variables(self.__dict__)
        return parser.feed(html_str)[0]

    def text(self, text_str):
        parser = TextParser()
        parser.set_variables(self.__dict__)
        return parser.feed(text_str)

    def t(self, text_str):
        return self.text(text_str)


window.eval(
    """
    function defineCustomElement(
        tagName,
        setup,
        observedAttributes,
        attributeChanged,
        connected,
        disconnected,
        adopted,
    ) {
        customElements.define(tagName, class extends HTMLElement {
            constructor() {
                super();
                this.attachShadow({ mode: 'open' });
                setup(this);
            }

            static get observedAttributes() {
                return observedAttributes;
            }

            attributeChangedCallback(name, oldValue, newValue) {
                attributeChanged(this.shadowRoot, this, name, newValue, oldValue);
            }

            connectedCallback() {
                connected(this);
            }

            disconnectedCallback() {
                disconnected(this);
            }

            adoptedCallback() {
                adopted(this);
            }
        });
    }

    function newEvent(name, options) {
        return new Event(name, options);
    }
    """
)
_defineCustomElement = window.defineCustomElement
_newEvent = window.newEvent


def customElement(name):
    def wrapper(cls):
        # collect event listeners
        cls._event_listeners = []
        for method, tp in event_listeners_map.items():
            cls._event_listeners.append((tp[0], tp[1], method))

        _defineCustomElement(
            name,
            cls.setup,
            to_js(cls.observedAttributes()),
            cls.attrchanged,
            cls.connected,
            cls.disconnected,
            cls.adopted,
        )

        return cls

    return wrapper


def newEvent(name, options={}):
    return _newEvent(name, to_js(options))


event_listeners_map = {}


# listen is a decorator that adds an event listener to the element
def listen(event, selector):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            return method(self, *args, **kwargs)

        event_listeners_map[method.__name__] = (event, selector)
        return method

    return decorator

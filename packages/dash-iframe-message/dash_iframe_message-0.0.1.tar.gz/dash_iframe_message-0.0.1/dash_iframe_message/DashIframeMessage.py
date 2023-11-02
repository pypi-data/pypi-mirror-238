# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashIframeMessage(Component):
    """A DashIframeMessage component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- height (string; required):
    The height of the iframe.

- message (dict; optional):
    The message from iframe.

- src (string; required):
    The src of the iframe.

- width (string; optional):
    The width of the iframe."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_iframe_message'
    _type = 'DashIframeMessage'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, message=Component.UNDEFINED, src=Component.REQUIRED, width=Component.UNDEFINED, height=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'height', 'message', 'src', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'height', 'message', 'src', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['height', 'src']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DashIframeMessage, self).__init__(**args)

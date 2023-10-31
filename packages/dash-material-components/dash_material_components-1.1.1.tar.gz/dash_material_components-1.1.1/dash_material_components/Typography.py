# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Typography(Component):
    """A Typography component.
Typography component from Material UI
https://mui.com/components/typography/

Keyword arguments:

- id (string; default 'text'):
    Used to identify dash components in callbacks.

- component (string; default 'h6'):
    Typography HTML node type.

- text (string | number; optional):
    Text to display.

- variant (string; default 'h6'):
    Typography variant."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Typography'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, component=Component.UNDEFINED, variant=Component.UNDEFINED, text=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'component', 'text', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'component', 'text', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Typography, self).__init__(**args)

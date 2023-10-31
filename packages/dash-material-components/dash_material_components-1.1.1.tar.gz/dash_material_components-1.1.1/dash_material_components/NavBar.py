# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class NavBar(Component):
    """A NavBar component.
Dashboard navigation bar component
https://mui.com/components/app-bar/

Keyword arguments:

- id (string; default 'navbar'):
    Used to identify dash components in callbacks.

- title (string; optional):
    Dashboard navigation bar title."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'NavBar'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, title=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'title']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(NavBar, self).__init__(**args)

# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Toggle(Component):
    """A Toggle component.
Toggle component

Keyword arguments:

- id (string; default 'toggle'):
    Used to identify dash components in callbacks.

- margin (string | number; default 2):
    Margin of the component.

- options (list of string | numbers; required):
    Array of options to select through the toggle.

- orientation (a value equal to: 'horizontal', 'vertical'; default 'horizontal'):
    Toggle orientation (horizontal or vertical).

- selected (string | number; optional):
    Selected toggle index."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Toggle'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, orientation=Component.UNDEFINED, options=Component.REQUIRED, selected=Component.UNDEFINED, margin=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'margin', 'options', 'orientation', 'selected']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'margin', 'options', 'orientation', 'selected']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Toggle, self).__init__(**args)

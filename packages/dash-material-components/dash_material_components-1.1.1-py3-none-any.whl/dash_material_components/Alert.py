# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Alert(Component):
    """An Alert component.
Alert component

Keyword arguments:

- id (string; default 'alert'):
    Used to identify dash components in callbacks.

- autoHide (number; default 5000):
    Automatically hide the alert (in ms).

- message (string; optional):
    Message to display.

- severity (a value equal to: 'error', 'warning', 'info', 'success'; default 'error'):
    Alert type."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Alert'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, severity=Component.UNDEFINED, autoHide=Component.UNDEFINED, message=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'autoHide', 'message', 'severity']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'autoHide', 'message', 'severity']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Alert, self).__init__(**args)

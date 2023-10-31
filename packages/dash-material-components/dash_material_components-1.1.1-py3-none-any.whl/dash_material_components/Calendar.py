# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Calendar(Component):
    """A Calendar component.
Calendar component

Keyword arguments:

- id (string; default 'calendar'):
    Used to identify dash components in callbacks.

- disableFuture (boolean; default True):
    Disable future dates.

- disablePast (boolean; default False):
    Disable past dates.

- disableToolbar (boolean; default False):
    Disable toolbar.

- helperText (string; optional):
    Text to display under the calendar form.

- labelText (string; optional):
    Text to display in the calendar form.

- margin (string | number; default 2):
    Margin.

- maxDate (string; default '2100-01-01'):
    Latest date available in the calendar.

- minDate (string; default '1900-01-01'):
    Earliest date available in the calendar.

- selected (string; optional):
    Active date selection.

- width (string | number; default '100%'):
    Width of calendar form."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Calendar'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labelText=Component.UNDEFINED, helperText=Component.UNDEFINED, width=Component.UNDEFINED, margin=Component.UNDEFINED, maxDate=Component.UNDEFINED, minDate=Component.UNDEFINED, disableFuture=Component.UNDEFINED, disablePast=Component.UNDEFINED, selected=Component.UNDEFINED, disableToolbar=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'disableFuture', 'disablePast', 'disableToolbar', 'helperText', 'labelText', 'margin', 'maxDate', 'minDate', 'selected', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'disableFuture', 'disablePast', 'disableToolbar', 'helperText', 'labelText', 'margin', 'maxDate', 'minDate', 'selected', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Calendar, self).__init__(**args)

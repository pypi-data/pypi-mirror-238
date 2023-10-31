# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Autocomplete(Component):
    """An Autocomplete component.
Autocomplete component

Keyword arguments:

- id (string; default 'autocomplete'):
    Used to identify dash components in callbacks.

- freeSolo (boolean; optional):
    Enable free solo.

- groupByField (string; optional):
    Group options.

- labelText (string; optional):
    Text to display above the slider form.

- limitTags (number; optional):
    Limit number of selected values.

- margin (string | number; default 2):
    Component margin.

- multiple (boolean; default False):
    Enable multiple selection.

- options (optional):
    Options to display.

- selected (optional):
    Current value.

- size (a value equal to: 'small', 'medium'; default 'small'):
    Mui TextField size parameter.

- variant (a value equal to: 'filled', 'outlined', 'standard'; default 'outlined'):
    Variant of mui input style.

- width (string; default '100%'):
    Component width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Autocomplete'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labelText=Component.UNDEFINED, size=Component.UNDEFINED, variant=Component.UNDEFINED, selected=Component.UNDEFINED, options=Component.UNDEFINED, limitTags=Component.UNDEFINED, freeSolo=Component.UNDEFINED, groupByField=Component.UNDEFINED, multiple=Component.UNDEFINED, width=Component.UNDEFINED, margin=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'freeSolo', 'groupByField', 'labelText', 'limitTags', 'margin', 'multiple', 'options', 'selected', 'size', 'variant', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'freeSolo', 'groupByField', 'labelText', 'limitTags', 'margin', 'multiple', 'options', 'selected', 'size', 'variant', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Autocomplete, self).__init__(**args)

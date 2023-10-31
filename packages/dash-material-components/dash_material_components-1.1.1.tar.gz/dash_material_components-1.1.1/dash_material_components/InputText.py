# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class InputText(Component):
    """An InputText component.
InputText component

Keyword arguments:

- id (string; optional):
    Used to identify dash components in callbacks.

- adornmentLeft (string; optional):
    Adornment on the left of the input.

- adornmentRight (string; optional):
    Adornment on the right of the input.

- autoFocus (boolean; default False):
    autoFocus.

- disabled (boolean; default False):
    Input disabled.

- error (boolean; default False):
    Input error.

- inputType (a value equal to: 'text', 'integer', 'float'; default 'text'):
    Input type.

- labelText (string; optional):
    Text to display above the slider form.

- margin (string | number; default 2):
    Component margin.

- maxLength (number; optional):
    Text length.

- maxValue (number; optional):
    Maximum selection allowed in the slider.

- minValue (number; optional):
    Minimum selection allowed in the slider.

- multiline (boolean; default False):
    Multiline input.

- precision (number; default 2):
    Number of decimal places.

- size (a value equal to: 'small', 'medium'; default 'small'):
    Mui TextField size parameter.

- value (string | number; default ''):
    Current value.

- variant (a value equal to: 'filled', 'outlined', 'standard'; default 'outlined'):
    Variant of mui input style.

- width (string; optional):
    Component width."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'InputText'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labelText=Component.UNDEFINED, value=Component.UNDEFINED, maxValue=Component.UNDEFINED, minValue=Component.UNDEFINED, precision=Component.UNDEFINED, inputType=Component.UNDEFINED, multiline=Component.UNDEFINED, variant=Component.UNDEFINED, maxLength=Component.UNDEFINED, autoFocus=Component.UNDEFINED, size=Component.UNDEFINED, width=Component.UNDEFINED, margin=Component.UNDEFINED, adornmentLeft=Component.UNDEFINED, adornmentRight=Component.UNDEFINED, disabled=Component.UNDEFINED, error=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'adornmentLeft', 'adornmentRight', 'autoFocus', 'disabled', 'error', 'inputType', 'labelText', 'margin', 'maxLength', 'maxValue', 'minValue', 'multiline', 'precision', 'size', 'value', 'variant', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'adornmentLeft', 'adornmentRight', 'autoFocus', 'disabled', 'error', 'inputType', 'labelText', 'margin', 'maxLength', 'maxValue', 'minValue', 'multiline', 'precision', 'size', 'value', 'variant', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(InputText, self).__init__(**args)

# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashpoolProvider(Component):
    """A DashpoolProvider component.
Context provider for easy interaction between Dashpool components

Keyword arguments:

- children (list of a list of or a singular dash component, string or numbers; required):
    Array of children.

- id (string; required):
    Unique ID to identify this component in Dash callbacks.

- dragElement (boolean | number | string | dict | list; optional):
    The last drag element.

- initialData (boolean | number | string | dict | list; optional):
    The initial state for the user. Note! Not everything is reactive.

- sharedData (dict; optional):
    the shared data.

    `sharedData` is a dict with keys:

    - apps (list of dicts; optional)

        `apps` is a list of dicts with keys:

        - group (string; required)

        - icon (string; required)

        - name (string; required)

        - url (string; required)

    - dragElement (boolean | number | string | dict | list; optional)

    - frames (list of dicts; optional)

        `frames` is a list of dicts with keys:

        - group (string; required)

        - icon (string; required)

        - id (string; required)

        - name (string; required)

        - url (string; required)

    - groups (list of dicts; optional)

        `groups` is a list of dicts with keys:

        - id (string; required)

        - name (string; required)

    - users (list of strings; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'DashpoolProvider'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, dragElement=Component.UNDEFINED, initialData=Component.UNDEFINED, sharedData=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'dragElement', 'initialData', 'sharedData']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'dragElement', 'initialData', 'sharedData']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(DashpoolProvider, self).__init__(children=children, **args)

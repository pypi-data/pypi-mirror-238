# Custom fields plugin for model builder

## Custom fields

Custom fields allow extending model at configuration time, with the same sources.
This plugin adds two types of custom fields - ones defined on an explicit element
(usually the "custom_fields" element is used, but any name can be used) and other
one inlining the custom fields directly to the main content.

Currently there is no support for inlining custom fields to "metadata" element,
but this can be changed in the future.

## Model file

Custom fields are defined on the level of "model":

```yaml
model:
    use: invenio
    custom-fields:
    - element: custom_fields
      config: TEST_CUSTOM_FIELDS
    properties:
        metadata:
            properties:
                title: fulltext
```

### Explicit custom fields

Explicit custom fields are defined using a pair of `element name` and `config` variable.
In the instance the custom fields will be separated into the `element name`:

```python
# config

from invenio_records_resources.services.custom_fields.text import KeywordCF

TEST_CUSTOM_FIELDS = [
    KeywordCF('blah')
]
```

```json5
// instance
{
    "metadata": {
        "title": "My Title"
    },
    "custom_fields": {                  // "element" from model
        "blah": "Custom field value"    // as defined in "TEST_CUSTOM_FIELDS" variable
    }
}
```

### Inline custom fields

Inline custom fields are placed on the root level of the instance, without an enclosing element. To define them, just leave the `element` definition. Note that only 1 definition of inline CF is allowed.

```yaml
model:
    use: invenio
    custom-fields:
    - config: INLINE_CF
    properties:
        metadata:
            properties:
                title: fulltext
```


```python
# config

from invenio_records_resources.services.custom_fields.text import KeywordCF

INLINE_CF = [
    KeywordCF('blah')
]
```

```json5
// instance
{
    "metadata": {
        "title": "My Title"
    },
    "blah": "Custom field value"    // as defined in "INLINE_CF" variable
}
```

### Custom fields nested in metadata

Custom fields nested inside the metadata are not supported yet.

## Using custom fields

Custom fields influence the jsonschema file (adding a non-checked object or allowing additional properties) and the mapping file (adding an empty mapping for CF). 

During deployment time, after the index is created and before data are poured in,
a specialized mapping for custom fields must be created. To do so, call

```bash
invenio oarepo cf init
```

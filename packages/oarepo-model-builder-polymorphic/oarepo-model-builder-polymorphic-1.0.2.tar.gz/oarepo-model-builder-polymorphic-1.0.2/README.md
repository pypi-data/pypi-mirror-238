<!--
 Copyright (c) 2022 CESNET

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Polymorphic model builder plugin

An [OARepo Model Builder](https://github.com/oarepo/oarepo-model-builder) plugin to generate
invenio sources for polymorphic models.

## Installation

```bash
pip install oarepo-model-builder-polymorphic
```

## Usage

### What is polymorphic model?

A polymorphic model is a dict that can be defined by multiple schemas.
Which schema is used depends on a value of a present field (that is shared
across all the schemas).

Polymorphic model can be used, for example, to express inheritance:

```yaml

extension1{}:
  disc: { type: keyword }
  a: { type: keyword }

extension2{}:
  disc: { type: keyword }
  b: { type: keyword }

record:
  properties:
    a:
      type: polymorphic
      discriminator: disc
      schemas:
        "1": { use: "/extension1" }
        "2": { use: "/extension2" }
```

The following are valid instances:

```yaml

a:
  disc: "1"
  a: "blah"
---
a:
  disc: "2"
  b: "blah"
```

Invalid instance:

```yaml
a:
  disc: "3"
  b: "blah"
---
a:
  disc: "1"
  a: "blah"
  b: "blah"
```

If the "disc" field contains value "1", first extension schema will be used,
if it contains value "2", second schema will be used. Any other value is not
valid.

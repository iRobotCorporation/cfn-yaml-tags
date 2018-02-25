# cfn-yaml-tags
## Python support for CloudFormation YAML tags

In CloudFormation YAML, references can be made as an object:
```yaml
SomeKey: {Ref: SomeResourceId}
```
or using YAML tags:
```yaml
SomeKey !Ref SomeResourceId
```
However, these are custom YAML tags, and can't be parsed by [PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation) out of the box.

`cfn_yaml_tags` implements this support.
Importing the `cfn_yaml_tags` module will add them
to the PyYAML library so that you can use `load` and
`dump` with them.

By default, they are not added to the `safe_load` and `safe_dump` methods.
Call the `mark_safe()` method to add it to these methods.

It also provides a [JSONEncoder](https://docs.python.org/2/library/json.html#encoders-and-decoders) subclass, `JSONFromYAMLEncoder`, to enable writing out JSON from templates loaded from YAML that have the tags.

**Usage**:
```python
import yaml
import cfn_yaml_tags

doc = """
Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties: {}
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      Environment:
        BucketName: !Ref MyBucket
        # etc.
"""

template = yaml.load(doc)

# optional:
# cfn_yaml_tags.mark_safe()
# template = yaml.safe_load(doc)

yaml_doc = yaml.dump(template)

json_doc = cfn_yaml_tags.JSONFromYAMLEncoder().encode(template)
"""
```
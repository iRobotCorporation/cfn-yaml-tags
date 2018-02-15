# cfn-yaml-tags

Implements support for CloudFormation's YAML tags.
Importing the `cfn_yaml_tags` module will add them
to the PyYAML library so that you can use `load` and
`dump` with them.
Does not add these to the "safe" methods by default.
Call the `mark_safe()` method to add it to these methods.

import unittest
import six
from six.moves import reload_module
import json

import yaml

import cfn_yaml_tags

class CfnYamlTagTest(unittest.TestCase):
    def setUp(self):
        for module in [yaml.representer, yaml.dumper, yaml.constructor, yaml.loader, yaml]:
            reload_module(module)
        reload_module(cfn_yaml_tags)
        
        self.doc = """
AndTest: !And
- Condition1
- Condition2
AZsTest: !GetAZs us-east-1
Base64Test: !Base64 abc
ConditionTest: !Condition MyCondition
EqualsTest: !Equals [Value1, Value2]
FindInMapTest: !FindInMap [MapName, TopLevelKey, SecondLevelKey]
GetAttListTest: !GetAtt [ResourceName, AttName]
GetAttStringTest: !GetAtt ResourceName.AttName
IfTest: !If
- Condition
- ValueIfTrue
- ValueIfFalse
ImportValueTest: !ImportValue ImportName
JoinTest: !Join
- ' '
- - hello
  - world
NotTest: !Not [Condition]
OrTest: !Or
- Condition1
- Condition2
RefTest: !Ref ResourceName
SelectTest: !Select [0, [1, 2, 3]]
SplitTest: !Split [',', 'foo/bar']
SubTest: !Sub
- '$foo'
- foo: bar
NestedTest: !If
- !And
  - !Not [!Condition MyCondition]
  - !Join
    - ' '
    - - !Ref MyResource
      - !Sub
        - $foo
        - foo: !GetAZs us-east-1
- ValueIfTrue
- ValueIfFalse
"""

        self.obj = {
            'AndTest': cfn_yaml_tags.And(['Condition1', 'Condition2']),
            'AZsTest': cfn_yaml_tags.GetAZs('us-east-1'),
            'Base64Test': cfn_yaml_tags.Base64('abc'),
            'ConditionTest': cfn_yaml_tags.Condition('MyCondition'),
            'EqualsTest': cfn_yaml_tags.Equals(['Value1', 'Value2']),
            'FindInMapTest': cfn_yaml_tags.FindInMap(['MapName', 'TopLevelKey', 'SecondLevelKey']),
            'GetAttListTest': cfn_yaml_tags.GetAtt(['ResourceName', 'AttName']),
            'GetAttStringTest': cfn_yaml_tags.GetAtt('ResourceName.AttName'),
            'IfTest': cfn_yaml_tags.If(['Condition', 'ValueIfTrue', 'ValueIfFalse']),
            'ImportValueTest': cfn_yaml_tags.ImportValue('ImportName'),
            'JoinTest': cfn_yaml_tags.Join([' ', ['hello', 'world']]),
            'NotTest': cfn_yaml_tags.Not(['Condition']),
            'OrTest': cfn_yaml_tags.Or(['Condition1', 'Condition2']),
            'RefTest': cfn_yaml_tags.Ref('ResourceName'),
            'SelectTest': cfn_yaml_tags.Select([0, [1, 2, 3]]),
            'SplitTest': cfn_yaml_tags.Split([',', 'foo/bar']),
            'SubTest': cfn_yaml_tags.Sub(['$foo', {'foo': 'bar'}]),
            'NestedTest': cfn_yaml_tags.If([
                cfn_yaml_tags.And([
                    cfn_yaml_tags.Not([cfn_yaml_tags.Condition('MyCondition')]),
                    cfn_yaml_tags.Join([
                        ' ',
                        [
                            cfn_yaml_tags.Ref('MyResource'),
                            cfn_yaml_tags.Sub([
                                '$foo',
                                {
                                    'foo': cfn_yaml_tags.GetAZs('us-east-1'),
                                },
                            ])
                        ]
                    ]),
                ]),
                'ValueIfTrue',
                'ValueIfFalse',
            ])
        }
    
    def test_load(self):
        loaded_obj = yaml.load(self.doc)
        self.assertEqual(loaded_obj, self.obj)
    
    def test_dump(self):
        dumped = yaml.dump(self.obj)
    
    def test_json(self):
        json.JSONEncoder().encode({'Fn::ImportValue': 'ImportName'})
        dumped = cfn_yaml_tags.JSONFromYAMLEncoder().encode(self.obj)
        json_obj = json.loads(dumped)
        self.assertEqual(json_obj['GetAttListTest']['Fn::GetAtt'],   ['ResourceName', 'AttName'])
        self.assertEqual(json_obj['GetAttStringTest']['Fn::GetAtt'], ['ResourceName', 'AttName'])
        
        ref_obj = {'RefTest': cfn_yaml_tags.Ref('ResourceName.AttName')}
        dumped = cfn_yaml_tags.JSONFromYAMLEncoder().encode(ref_obj)
        json_obj = json.loads(dumped)
        self.assertIn('Fn::GetAtt', json_obj['RefTest'])
        self.assertNotIn('Ref', json_obj['RefTest'])
        self.assertEqual(json_obj['RefTest']['Fn::GetAtt'],   ['ResourceName', 'AttName'])
    
    def test_safe_load_fail(self):
        with self.assertRaises(yaml.constructor.ConstructorError):
            yaml.safe_load(self.doc)
    
    def test_safe_load_ok(self):
        cfn_yaml_tags.mark_safe()
        loaded_obj = yaml.safe_load(self.doc)
        self.assertEqual(loaded_obj, self.obj)
    
    def test_safe_dump_fail(self):
        with self.assertRaises(yaml.representer.RepresenterError):
            dumped = yaml.safe_dump(self.obj)
    
    def test_safe_dump_ok(self):
        cfn_yaml_tags.mark_safe()
        dumped = yaml.safe_dump(self.doc)

if __name__ == '__main__':
    unittest.main()
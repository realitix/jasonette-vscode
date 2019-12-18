#!/usr/bin/env python3

import json
import yaml


def json_to_yaml_indent(example):
    example = {k:v for k,v in example.items() if not k == 'api_description'}
    indent_size = 4
    yaml_out = yaml.dump(example, indent=indent_size).rstrip()
    yaml_out = yaml_out.replace(' ' * indent_size, '\t')
    lines = yaml_out.split("\n")
    return lines


def main():
    with open('api.json') as json_file:
        data = json.load(json_file)
    
    model = {}
    for action_name, examples in data['actions'].items():
        for example in examples:
            a = action_name.replace("$", "\\$")
            model[example['api_description']] = {
                'prefix': [action_name],
                'body': [a] + json_to_yaml_indent(example)
            }
    
    with open('snippets/yaml.json', 'w') as outfile:
        json.dump(model, outfile, indent=True)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import json
import yaml


def filter(example):
    return {k:v for k,v in example.items() if not k == 'api_description'}


def add_callbacks(example):
    if "success" not in example and "error" not in example:
        example["success"] = {"type": "$"}
        example["error"] = {"type": "$"}
    
    return example


def json_to_yaml_indent(example):
    indent_size = 4
    yaml_out = yaml.dump(example, indent=indent_size, sort_keys=False).rstrip()
    yaml_out = yaml_out.replace(' ' * indent_size, '\t')
    lines = yaml_out.split("\n")
    return lines


def main():
    with open('api.json') as json_file:
        data = json.load(json_file)
    
    model = {}
    # Actions
    for action_name, examples in data['actions'].items():
        for example in examples:
            a = action_name.replace("$", "\\$")
            model[example['api_description']] = {
                'prefix': [action_name],
                'body': [a] + json_to_yaml_indent(add_callbacks(filter(example)))
            }
    
    # Components
    for component_name, examples in data['components'].items():
        for example in examples:
            c = component_name
            model[example['api_description']] = {
                'prefix': [c],
                'body': [c] + json_to_yaml_indent(filter(example))
            }
    
    with open('snippets/yaml.json', 'w') as outfile:
        json.dump(model, outfile, indent=True)


if __name__ == '__main__':
    main()
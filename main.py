from os import walk
import os
from tree_sitter import Language, Parser
from pydriller import Repository

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'tree-sitter-python'
  ]
)

PY_LANGUAGE = Language('build/my-languages.so', 'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)

# For each file, parse the AST for methods and classes.
# Get a delta of methods and classes for each commit.
# For each AST entry generate a history.

classes = {}

cwd = os.getcwd()

# Walk AST looking for methods associated with a class

def walk_class(node):
    if node.type == 'class_definition':
        class_name = ''
        for child in node.children:
            if child.type == 'identifier':
                class_name = child.text
                classes[class_name] = {}
            if child.type == 'block':
                for grandchild in child.children:
                    if grandchild.type == 'function_definition':
                        func_identifier = next(filter(lambda x: x.type == 'identifier', grandchild.children)).text
                        classes[class_name][func_identifier] = node
    for child in node.children:
        walk_class(child)

for commit in Repository(cwd).traverse_commits():
    for m in commit.modified_files:
        if m.filename.endswith('.py') and m.new_path.startswith('test_files'):
            source = m.source_code
            try:
                tree = parser.parse(bytes(source, 'utf-8'))
                walk_class(tree.root_node)
            except Exception as e:
                print(e)
                continue




# CLI for querying a specific class and method - find all uses and when each use was added.
from collections import defaultdict
from email.policy import default
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
cwd = os.getcwd()

# Walk AST looking for methods associated with a class

class FileSnapshot(object):

    def __init__(self, commit) -> None:
        self.classes = {}
        self.commit = commit

    def walk_class(self, node):
        if node.type == 'class_definition':
            class_name = ''
            for child in node.children:
                if child.type == 'identifier':
                    class_name = child.text.decode('utf-8')
                    self.classes[class_name] = {}
                if child.type == 'block':
                    for grandchild in child.children:
                        if grandchild.type == 'function_definition':
                            func_identifier = next(filter(lambda x: x.type == 'identifier', grandchild.children)).text.decode('utf-8')
                            self.classes[class_name][func_identifier] = node
        for child in node.children:
            self.walk_class(child)
            
snapshots = defaultdict(list)

for commit in Repository(cwd).traverse_commits():
    for m in commit.modified_files:
        if m.filename.endswith('.py') and m.new_path.startswith('test_files'):
            source = m.source_code
            try:
                tree = parser.parse(bytes(source, 'utf-8'))
                snapshot = FileSnapshot(commit)
                snapshot.walk_class(tree.root_node)
                snapshots[m.filename].append(snapshot)
            except Exception as e:
                print(e)
                continue

def find_when_method_added(file, class_name, method_name):
    for i in range(1, len(snapshots[file])):
        cls = snapshots[file][i].classes
        methods = snapshots[file][i].classes[class_name]
        prev_methods = snapshots[file][i-1].classes[class_name]
        if method_name in methods and method_name not in prev_methods:
            return snapshots[file][i].commit.hash

res = find_when_method_added('bungus.py', 'Bungus', 'say_no')

print(res)


# CLI for querying a specific class and method - find all uses and when each use was added.
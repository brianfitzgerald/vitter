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

for commit in Repository(cwd).traverse_commits():
    for m in commit.modified_files:
        if m.new_path.endswith('.py'):
            source = m.source_code
            try:
                tree = parser.parse(bytes(source, 'utf-8'))
                print(tree.sexp())
            except Exception as e:
                print(e)
                continue




# CLI for querying a specific class and method - find all uses and when each use was added.
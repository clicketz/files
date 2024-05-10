import re
from tree_sitter_languages import get_language, get_parser

language = get_language('lua')
parser = get_parser('lua')

found_constants = {}

with open("Constants.lua", "r") as f:
    code = f.read()

tree = parser.parse(code.encode("utf-8"))
root_node = tree.root_node

# First we want to find all of the assignment expressions
# and match them, but we'll leave off any with an underscore
# which we will obtain later
for child in root_node.children:
    if child.type == "variable_assignment":
        capture = re.search(r"^([^\._]+?)\s*=", child.text.decode("utf-8"))

        if capture:
            found_constants[capture.group(1)] = True

# Next we want to find any constants with underscores. This
# is pretty much every constant in this file, but this *will*
# not capture legitimate constants without underscores e.g. "LEGENDARY"
# TODO: Implement a way to get all constants (probably through parser)
capture = re.findall(r"(\w+_\w+)", code)

for match in capture:
    found_constants[match] = True

# Finally we print all found constants to a formatted table that
# can be parsed by our github workflow job
with open("Constants_Parsed.lua", "w+") as f:
    f.write("local Constants = {\n")

    for constant in sorted(found_constants):
        f.write('    "{}",\n'.format(constant))

    f.write("}\n")
    f.write("return Constants\n")

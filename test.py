import sys
import js2xml

text = sys.stdin.read()
if not text:
    text = """
     var x = {
        "key1": "value1",
        "key2": "value2",
        "key3": 1,
        "key4": false
    };
    """
print text
tree = js2xml.parse(text, debug=False)
print js2xml.pretty_print(tree)

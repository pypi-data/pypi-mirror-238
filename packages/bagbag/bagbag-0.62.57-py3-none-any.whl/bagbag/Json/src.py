import json
import io
import os
import html_to_json

#print("load json")

def Dumps(obj, indent=4, ensure_ascii=False) -> str:
    """
    It takes a Python object and returns a JSON string
    
    :param obj: The object to be serialized
    :param indent: This is the number of spaces to indent for each level. If it is None, that
    will insert newlines but won't indent the new lines, defaults to 4 (optional)
    :param ensure_ascii: If True, all non-ASCII characters in the output are escaped with \\uXXXX
    sequences, and the result is a str instance consisting of ASCII characters only. If False, some
    chunks written to fp may be unicode instances. This usually happens because the input contains
    unicode strings or the, defaults to False (optional)
    :return: A string
    """
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii)

def Loads(s:str|io.TextIOWrapper) -> list | dict:
    """
    The function Loads can load JSON or HTML data from 
    1. a file (file path)
    2. a string
    3. a file object
    
    :param s: The parameter `s` can be either a string or a file object (`io.TextIOWrapper`). It
    represents the JSON data or HTML data that needs to be loaded
    :type s: str|io.TextIOWrapper
    :return: The function `Loads` returns a list or a dictionary depending on the input provided. If the
    input is a file object of type `io.TextIOWrapper`, it reads the contents of the file and returns a
    dictionary or a list after parsing the JSON data. If the input is a string, it checks if the string
    starts with `[` or `{` and returns a dictionary or a list after
    """
    if type(s) == io.TextIOWrapper:
        return json.loads(s.read())
    
    if type(s) == str:
        if s.startswith('[') or s.startswith('{'):
            return json.loads(s)
        elif os.path.exists(s):
            data = open(s).read()
            try:
                return json.loads(data)
            except:
                return html_to_json.convert(data)
        else:
            return html_to_json.convert(s)

def ExtraValueByKey(obj:list|dict, key:str) -> list:
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)

                if k == key:
                    arr.append(v)
                    
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


if __name__ == "__main__":
    # j = Dumps({1: 3, 4: 5})
    # print(j)

    # d = Loads(j)
    # print(d)

    # print(type(d))

    # ------------

    # data = {
    #     "key": {
    #         "key": [
    #             {
    #                 "a": "b"
    #             },
    #             {
    #                 "key": "123"
    #             }
    #         ]
    #     }
    # }

    # print(ExtraValueByKey(data, "key"))

    html_string = """<head>
    <title>Test site</title>
    <meta charset="UTF-8"></head>"""

    print(Loads(html_string))
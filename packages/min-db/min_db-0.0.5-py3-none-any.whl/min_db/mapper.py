import re
import xml.etree.ElementTree as ElemTree


class Mapper:
    def __init__(self, path):
        self._path: str = path
        self._queries = ElemTree.parse(self._path).getroot()

    def get_query(self, namespace: str, name: str, param: dict | None = None) -> str:
        namespace = self._queries.findall(".//*[@namespace='" + namespace + "']")
        if len(namespace) > 1:
            raise AttributeError("namespace is duplicated")
        if len(namespace) == 0:
            raise AttributeError("namespace is not exist")
        query_strings = namespace[0].findall(".//*[@id='"+name+"']")
        if len(query_strings) > 1:
            raise AttributeError("id of query is duplicated")
        if len(query_strings) == 0:
            raise AttributeError("id of query not exist")
        query = query_strings[0].text
        if param is not None:
            query = parameter_mapping(query, param)
        return query


def parameter_mapping(query: str, param: dict) -> str:
    mapped = re.sub(r"\#\{(.*?)\}", lambda m: mapping(m.group(1), param), query)
    return mapped


def mapping(s: str, param: dict) -> str | None:
    v = param[s]
    if v is None:
        return "NULL"
    elif type(v) == int or type(param[s]) == float:
        return str(v)
    elif type(v) == str:
        v = v.replace("'", '"')
        return "'" + v + "'"

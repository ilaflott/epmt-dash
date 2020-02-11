#!/usr/bin/env python3


# Taken from well researched SO post
# https://stackoverflow.com/a/25496309/10377587

import urllib.parse
import posixpath
# import ntpath


def path_parse(path_string, *, normalize=True, module=posixpath):
    # Prevent 
    result = []
    if path_string:
        if normalize:
            tmp = module.normpath(path_string)
        else:
            tmp = path_string
        while tmp != "/":
            (tmp, item) = module.split(tmp)
            result.insert(0, item)
    return result


def dump_array(array):
    string = "[ "
    for index, item in enumerate(array):
        if index > 0:
            string += ", "
        string += "\"{}\"".format(item)
    string += " ]"
    return string


def parse_url(url, *, normalize=True, module=posixpath):
    # url must start with 'http://' else host becomes part of path
    # according to urllib.parse.urlparse
    if not url.startswith('http'):
        url = "http://" + url

    url_parsed = urllib.parse.urlparse(url)

    path_parsed = path_parse(urllib.parse.unquote(url_parsed.path),
                             normalize=normalize, module=module)

    query_parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)

    # Parse query key values, values for commas
    # TODO: A better method may be encoding or repeating the key
    # https://stackoverflow.com/a/50537278
    for field in query_parsed.keys():
        if ',' in query_parsed[field][0]:
            query_parsed[field] = query_parsed[field][0].split(',')
    
    #sys.stdout.write("{}\n  --[n={},m={}]-->\n    {}\n".format(
    #    url, normalize, module.__name__, dump_array(path_parsed)))
    return {"path":path_parsed, "query":query_parsed}


#parse_url("http://eg.com/hithere/something/else")
#parse_url("http://eg.com/hithere/something/else/")
#parse_url("http://eg.com/hithere/something/else/", normalize=False)
#parse_url("http://eg.com/see%5C/if%5C/this%5C/works", normalize=False)
#parse_url("http://eg.com/see%5C/if%5C/this%5C/works", normalize=False, module=ntpath)

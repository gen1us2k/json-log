#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from optparse import OptionParser
import pystache

def get_filter_fields(input_filter):
    fields, value = None, None
    if input_filter:
        fields, value = input_filter.split("=")
        fields = fields.split(".")
    return fields, value


def process_stdin(options):
    template_name = options.format if options.format else "default.j2"
    template = open(template_name).read()
    fields, value = get_filter_fields(options.input_filter)
    for line in sys.stdin:
        # TODO: This piece of code smess.
        line = json.loads(line)
        if fields:
            try:
                if line[fields[0]][fields[1]] == value:
                    print pystache.render(template, line)
            except IndexError:
                if line[fields[0]] == value:
                    print pystache.render(template, line)
        else:
            print pystache.render(template, line)




if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--format", dest="format", help="Specify jijna2 template for render output")
    parser.add_option("--filter", dest="input_filter", help="Specify filter")
    (options, args) = parser.parse_args()
    process_stdin(options)

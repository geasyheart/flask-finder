from flask import request

from finder.ext.exceptions import api_view
from finder.service import Finder


@api_view
def ls():
    return Finder.ls()


@api_view
def check():
    return Finder.check()


@api_view
def register():
    if request.is_json:
        content = request.json
    else:
        content = request.form.to_dict()
    return Finder.register(**content)


@api_view
def get(field):
    return Finder.get(field)


@api_view
def remove(field):
    return Finder.remove(field)


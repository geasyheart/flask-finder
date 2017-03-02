from finder.apis import ls, check, register, get, remove


def configure(app):
    app.add_url_rule("/ls", view_func=ls)
    app.add_url_rule("/check", view_func=check)
    app.add_url_rule("/register", view_func=register, methods=["POST"])
    app.add_url_rule("/get/<field>", view_func=get)
    app.add_url_rule("/remove/<field>", view_func=remove, methods=["DELETE"])

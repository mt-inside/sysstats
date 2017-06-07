from flask import Flask, render_template, Response

import sysstats_client

app = Flask(__name__)

# Not built into Flask as apparently uncommon, but copied from
# http://flask.pocoo.org/docs/0.12/patterns/streaming/
def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv

@app.route('/')
def sysstats():
    return Response(stream_template('sysstats.html',
        date = sysstats_client.date(),
        uname_a = sysstats_client.uname_a(),
        kernel_version = sysstats_client.kernel_version(),
        ifaces = sysstats_client.ifaces()
    ))

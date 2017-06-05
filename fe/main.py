from flask import Flask, render_template

import sysstats_client

app = Flask(__name__)

@app.route('/')
def sysstats():
    return render_template('sysstats.html',
        date = sysstats_client.date(),
        uname_a = sysstats_client.uname_a(),
        kernel_version = sysstats_client.kernel_version(),
        ifaces = sysstats_client.ifaces()
    )

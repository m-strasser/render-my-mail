"""
Sets up a simple flask site that allows to render an HTML template and mail it
to a given e-mail-address.
"""
import logging
import os
import yaml
import re
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

#### SERVER SIDE #################
# Read the template
# Replace tags with given values
# Send per mail
##################################

#### CLIENT SIDE #################
# Show input form for allowed tags
# Accept input
# Call backend
##################################

app = Flask(__name__)
tags = []

def read_tags_from_template(name):
    """
    Reads an HTML template and extracts the occurring flask tags.
    :param name: The name of the template file.
    :returns: The list of used tags.
    """
    global tags
    regex = re.compile('{{\s*(\w+)\s*}}')

    with open('{}/templates/{}'.format(
        os.path.dirname(os.path.abspath(__file__)), name), 'r') as template:
        map(lambda x: tags.extend(regex.findall(x)), template.readlines())

def inject_email_field(action, method, tmpl, **context):
    """
    Renders a template, then injects an email input field right after the body
    tag.
    :param action: The value for the forms action tag (i.e. a URL).
    :param method: The value for the forms method tag (i.e. POST or GET).
    :param tmpl: The name of the template.
    :param context: The context of the template (i.e. the values you want to
    pass to it).
    :returns: The rendered template with the injected field.
    """
    injection = """
    <form action='""" + action + """' method='""" + method + """'>
        <label for="email" id="gen_email_lbl">Your E-mail address:</label>
        <input type="email" name="email" id="gen_email_field"/>
        <input type="submit" value="Send" id="gen_submit"/>
    </form>
    """
    rendered = render_template(tmpl, **context).split('\n')
    body_index = next(i for i,x in enumerate(rendered) if '<body>' in x)
    rendered.insert(body_index+1, injection)
    return '\n'.join(rendered)

@app.route("/", methods=['GET'])
def show_input_form():
    """
    Displays the input form which allows a user to enter the values of the
    corresponding tags.
    """
    return render_template('input_form.html', fields=tags)

@app.route("/preview_email", methods=['GET', 'POST'])
def preview_email():
    if request.method == 'GET':
        return redirect('/')

    # Just pass those tags that we extracted earlier, you never know
    tmpl = inject_email_field(url_for('render_email'), 'POST',
            config['template'],
            **{k: v for k, v in request.form.iteritems() if k in tags})

    return tmpl

@app.route("/render_email", methods=['GET', 'POST'])
def render_email():
    if request.method == 'GET':
        return redirect('/')
    return render_template('render_email.html', success=False)

def main():
    """
    Sets up the flask site.
    """
    global config
    path = '{}/{}.yaml'.format(
        os.path.dirname(os.path.abspath(__file__)), # The directory of this file
        __file__.rstrip('.py') # The name of this file without the extension
    )
    with open(path, 'r') as configfile:
        config = yaml.load(configfile)

    read_tags_from_template(config['template'])

    app.run()

if __name__ == '__main__':
    main()

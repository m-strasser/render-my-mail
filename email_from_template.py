#!/usr/bin/env/ python
"""
Sets up a simple flask site that allows to render an HTML template and mail it
to a given e-mail-address.
"""
import logging
import os
import yaml
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
from flask import render_template
from flask import render_template_string
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

    with open('{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)), name), 'r') as template:
        map(lambda x: tags.extend(regex.findall(x)), template.readlines())

def inject_template_extension(tmpl, **context):
    """
    Prepends {% extends "preview.html" %} to the given HTML code and wraps
    its content into a block named email.
    The given HTML code is rendered before and stored in the global variable
    rendered.
    :param tmpl: The path to the HTML file.
    :param context: The context to pass to render_template_string with the
    given HTML file.
    :returns: The modified HTML template.
    """
    global rendered
    with open(tmpl, 'r') as template:
        rendered = render_template_string(template.read(), **context)
        lines = rendered.split('\n')
        body_tags_index = [ i for i,x in enumerate(lines) if '<body>' in x or '</body>' in x ]
        content = lines[body_tags_index[0]+1:body_tags_index[1]]
        content.insert(0, '{% extends "preview.html" %}{% block email %}')
        content.append('{% endblock %}')

        return '\n'.join(content)

def send_mail(to, subject, body_html):
    """
    Sends an email to the specified address.
    :param to: The e-mail address the e-mail is sent to.
    :param subject: The subject of the e-mail.
    :param body_html: The body of the e-mail as HTML.
    :throws smtplib.SMTPException: If something goes wrong.
    """
    smtpserver = smtplib.SMTP(config['host'], config['port'])
    smtpserver.starttls()
    try:
        user = config['user']
    except KeyError:
        user = config['address']
    smtpserver.login(user, config['password'])
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = config['address']
    msg['To'] = to
    msg.add_header('Reply-To', config['reply-to'])

    html = MIMEText(body_html, 'html')
    msg.attach(html)

    smtpserver.sendmail(config['address'], to, msg.as_string())
    smtpserver.quit()

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

    return render_template_string(
        inject_template_extension(config['template'],
        # Just pass those tags that we extracted earlier, you never know
        **{k: v for k, v in request.form.iteritems() if k in tags}))

@app.route("/render_email", methods=['GET', 'POST'])
def render_email():
    if request.method == 'GET':
        return redirect('/')
    try:
        send_mail(request.form['email'], config['subject'], rendered)
    except smtplib.SMTPException as e:
        err_msg = str(e) if config.get('debug', False) else None
        return render_template('render_email.html', success=False, err=err_msg)

    return render_template('render_email.html', success=True)

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

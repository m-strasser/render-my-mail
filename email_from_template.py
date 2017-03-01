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
    global rendered
    injection = """
    <form action='""" + action + """' method='""" + method + """' name="gen_form">
        <label for="email" id="gen_email_lbl">Your E-mail address:</label>
        <input type="email" name="email" id="gen_email_field"/>
        <input type="submit" value="Send" id="gen_submit"/>
    </form>
    """
    global injected_lines
    injected_lines = len(injection.split('\n'))

    rendered = render_template(tmpl, **context).split('\n')
    body_index = next(i for i,x in enumerate(rendered) if '<body>' in x)
    rendered.insert(body_index+1, injection)
    rendered = '\n'.join(rendered)
    return rendered

def remove_email_field():
    """
    Removes the email field from the template that was injected before with
    inject_email_field.
    The global variable rendered is the template which will be used and all
    changes will be saved to it.
    :returns: The template without the email field.
    """
    global rendered
    rendered = rendered.split('\n')
    form_index = next(i for i,x in enumerate(rendered) if 'name="gen_form"' in x)
    del rendered[form_index-1:form_index+injected_lines-1]
    rendered = '\n'.join(rendered)

    return rendered

def send_mail(to, subject, body_html):
    """
    Sends an email to the specified address.
    :param to: The e-mail address the e-mail is sent to.
    :param subject: The subject of the e-mail.
    :param body_html: The body of the e-mail as HTML.
    :throws smtplib.SMTPAuthenticationError: If the authentication failed.
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

    # Just pass those tags that we extracted earlier, you never know
    return inject_email_field(url_for('render_email'), 'POST',
            config['template'],
            **{k: v for k, v in request.form.iteritems() if k in tags})

@app.route("/render_email", methods=['GET', 'POST'])
def render_email():
    if request.method == 'GET':
        return redirect('/')
    try:
        send_mail(request.form['email'], config['subject'], remove_email_field())
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

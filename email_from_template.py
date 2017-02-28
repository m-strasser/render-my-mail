"""
Sets up a simple flask site that allows to render an HTML template and mail it
to a given e-mail-address.
"""
import os
import yaml
import re
from flask import Flask

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

@app.route("/", methods=['GET'])
def show_input_form():
    """
    Displays the input form which allows a user to enter the values of the
    corresponding tags.
    """
    return render_template('u')

def main():
    """
    Sets up the flask site.
    """
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

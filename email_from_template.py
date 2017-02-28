"""
Sets up a simple flask site that allows to render an HTML template and mail it
to a given e-mail-address.
"""
import yaml
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

def read_config(path):
    """
    Reads the configuration file from the given path.
    :param path: The path to the configuration file (a YAML file).
    :returns: The parsed configuration.
    :raises IOError: If the file at the given path does not exist.
    """
    if not os.path.isfile(path):
        raise IOError('Could not find config file {}'.format(path))

    with open(path, 'r') as configfile:
        return yaml.load(configfile)

@app.route("/", methods=['GET'])
def show_input_form():
    """
    Displays the input form which allows a user to enter the values of the
    corresponding tags.
    """
    return render_template('u')

if __name__ == '__main__':
    app.run()

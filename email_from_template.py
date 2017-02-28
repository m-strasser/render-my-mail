"""
Sets up a simple flask site that allows to render an HTML template and mail it
to a given e-mail-address.
"""
from flask import Flask

#### SERVER SIDE #################
# Read the template
# Replace tags with given values
# Send per mail
##################################

#### CLIENT SIDE #################
# Show inputs for allowed tags
# Accept input
# Call backend
##################################

app = Flask(__name__)

@app.route("/")
def show_template():
    return "TEMPLATE"

if __name__ == '__main__':
    app.run()

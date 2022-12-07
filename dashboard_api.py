import flask
#import flask_cors
import json
import os

app = flask.Flask(__name__)
data_folder_path = os.getcwd() # Get current path

@app.route('/')
def index():
    return 'Please put the dashboard name/json filename in url : localhost:5000/<dashboard_name>'

@app.route('/<dashboard_name>')
def get_json_data(dashboard_name):
    if os.path.exists(data_folder_path + '\data\\' + dashboard_name + '.json'):
        json_file = open(data_folder_path + '\data\\' + dashboard_name + '.json')
        dashboard_info = json.load(json_file)
        return dashboard_info
    else:
        return 'No file name ' + dashboard_name + '.json'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
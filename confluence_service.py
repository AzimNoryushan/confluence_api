# Jinja2==2.11.3
import os
import flask
import requests
import json
from atlassian import Confluence
from flask import render_template
from dotenv import load_dotenv

# Load .env file
load_dotenv()

confluence = Confluence(
    url = os.getenv('CONFLUENCE_URL'), 
    username = os.getenv('CONFLUENCE_USER'), 
    password = os.getenv('CONFLUENCE_PASSWORD')
)

app = flask.Flask(__name__)

#TODO - Review usage of this route whether its duplicated or not
@app.route('/create/<space>/<dashboard_name>')
def create_dashboard(space = None, dashboard_name = None):
    # Create a new dashboard
    dashboard_info = requests.get(os.getenv('DASHBOARD_URL') + dashboard_name).json()
    body = render_template('page_template', dashboard_info=dashboard_info)
    status = confluence.create_page(
        space=space,
        title=dashboard_info['Dashboard Name'],
        body=body
    )
    return status

# TODO: Clean up messy logic :(
# /update/DevServices/Advanced+Add-On+Packs/Access+EzBuild/Access+EzBuild+-+Analytics/dashboard_summary
@app.route('/update/<space>/<sub_space>/<project>/<parent>/<dashboard_name>')
def update_dashboard(space = None, sub_space = None, project = None, parent = None, dashboard_name = None):
    # Update an existing dashboard
    try:
        # Clean up URL
        sub_space = sub_space.replace('+', ' ')
        project = project.replace('+', ' ')
        parent = parent.replace('+', ' ')

        #return space + "/" + sub_space + "/" + project + "/" + parent + "/" + dashboard_name
        dashboard_name = dashboard_name.replace('+', '_')

        dashboard_info = requests.get(os.getenv('DASHBOARD_URL') + dashboard_name).json()
        title = dashboard_info['Dashboard Name']
        body = render_template('page_template', dashboard_info=dashboard_info)
        
        #Check if sub_space page exists
        if confluence.page_exists(space=space, title=sub_space):
            sub_space_id = confluence.get_page_id(
                space=space, 
                title=sub_space
            )
            
            # Check project page exists
            if confluence.page_exists(space=space, title=project):
                project_id = confluence.get_page_id(
                    space=space, 
                    title=project
                )

                # Check parent page exists
                if confluence.page_exists(space=space, title=parent):
                    parent_id = confluence.get_page_id(
                        space=space, 
                        title=parent
                    )

                    # Check dashboard page exists
                    if confluence.page_exists(space=space, title=title):
                        page_id = confluence.get_page_id(
                            space=space, 
                            title=title
                        )
                        confluence.update_page(page_id=page_id, parent_id=parent_id, title=title, body=body)
                        return "Successfully updated dashboard: " + dashboard_name
                    else:
                        confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)
                        return "Successfully created dashboard: " + dashboard_name

                else:
                    create_child_page(space=space, parent_id=project_id, title=parent)
                    parent_id = confluence.get_page_id(space=space, title=parent)
                    confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)
                    return "Successfully created dashboard: " + dashboard_name

            else:
                # Create project page
                create_parent_page(space=space, parent_id=sub_space_id, title=project)
                
                project_id = confluence.get_page_id(
                    space=space, 
                    title=project
                )
                # Create parent page
                create_child_page(space=space, parent_id=project_id, title=parent)

                parent_id = confluence.get_page_id(
                    space=space, 
                    title=parent
                )
                # Create dashboard page
                create_child_page(space=space, parent_id=parent_id, title=title, body=body)
        else:
            # Create sub_space page
            create_parent_page(space=space, title=sub_space)

            sub_space_id = confluence.get_page_id(
                space=space, 
                title=sub_space
            )
            # Create project page
            create_parent_page(space=space, parent_id=sub_space_id, title=project)

            project_id = confluence.get_page_id(
                space=space, 
                title=project
            )
            # Create parent page
            create_child_page(space=space, parent_id=project_id, title=parent)

            parent_id = confluence.get_page_id(
                space=space, 
                title=parent
            )
            # Create dashboard page
            create_child_page(space=space, parent_id=parent_id, title=title, body=body)

        return "Successfully created dashboard: " + dashboard_name

    except requests.exceptions.JSONDecodeError:
        return "No Dashboard API for " + dashboard_name
    except requests.exceptions.HTTPError as e:
        return e.response.text

@app.route('/update/dataview/<space>/<project>/<parent>/<dataview_name>')
def update_dataview(space = None, project = None, parent = None, dataview_name = None):
    # Update an existing dataview
    try:
        # Clean up URL
        project = project.replace('+', ' ')
        parent = parent.replace('+', ' ')
        dataview_name = dataview_name.replace('+', '_')

        dataview_info = requests.get(os.getenv('DATAVIEW_URL'), 
            headers={'Authorization': 'Bearer ' + os.getenv('DATAVIEW_AUTHORIZATION')}, 
            params={'top': '1', '_': 1658192997724}
        ).json()
        columns = dataview_info['data']['columns']

        title = 'Subcontrators'
        body = render_template('dataview_template', columns=columns)

        # Check project page exists
        if confluence.page_exists(space=space, title=project):
            project_id = confluence.get_page_id(space=space, title=project)

            # Check parent page exists
            if confluence.page_exists(space=space, title=parent):
                parent_id = confluence.get_page_id(space=space, title=parent)

                # Check dataview page exists
                if confluence.page_exists(space=space, title=title):
                    page_id = confluence.get_page_id(
                        space=space, 
                        title=title
                    )
                    confluence.update_page(page_id=page_id, parent_id=parent_id, title=title, body=body)
                    return "Successfully updated dataview: " + dataview_name
                else:
                    confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)
                    return "Successfully created dataview: " + dataview_name

            else:
                create_child_page(space=space, parent_id=project_id, title=parent)
                parent_id = confluence.get_page_id(space=space, title=parent)
                confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)
                return "Successfully created dataview: " + dataview_name

        else:
            # Create project page
            create_parent_page(space=space, title=project)

            project_id = confluence.get_page_id(
                space=space, 
                title=project
            )
            # Create parent page
            create_child_page(space=space, parent_id=project_id, title=parent)

            parent_id = confluence.get_page_id(
                space=space, 
                title=parent
            )
            # Create dataview page
            create_child_page(space=space, parent_id=parent_id, title=title, body=body)

            return "Successfully created dataview: " + dataview_name
    except requests.exceptions.JSONDecodeError:
        return "No Dataview API for " + dataview_name
    except requests.exceptions.HTTPError as e:
        return e.response.text

# @app.route('/update/data_clone/<space>/<project>/<parent>/<data_name>')
# def update_data_clone(space = None, project = None, parent = None, data_name = None):
#     try:
#         project = project.replace('+', ' ')
#         parent = parent.replace('+', ' ')
#         dataclone_name = dataview_name.replace('+', '_')

#         data_clone_info = ""

#         files = os.listdir('data/')

#         for file in files:
#             f = open('data/' + file, 'r')
#             data_clone_info = data_clone_info.extend(f.readlines())

#         print(data_clone_info)
#         exit()


#         data_clone_file = open('data/' + data_name + '.json', 'r')
#         data_clone_info = json.load(data_clone_file)


#         title = project + ' -  Data Clone'
#         body = render_template('data_clone_template', data_clone_info=data_clone_info)

#         if confluence.page_exists(space=space, title=project):
#             project_id = confluence.get_page_id(space=space, title=project)

#             # Check parent page exists
#             if confluence.page_exists(space=space, title=parent):
#                 parent_id = confluence.get_page_id(space=space, title=parent)

#                 # Check dataview page exists
#                 if confluence.page_exists(space=space, title=title):
#                     page_id = confluence.get_page_id(
#                         space=space, 
#                         title=title
#                     )
#                     confluence.update_page(page_id=page_id, parent_id=parent_id, title=title, body=body)
#                     return "Successfully updated dataview: " + dataclone_name
#                 else:
#                     confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)
#                     return "Successfully created dataview: " + dataclone_name

#             else:
#                 create_child_page(space=space, parent_id=project_id, title=parent)
#                 parent_id = confluence.get_page_id(space=space, title=parent)
#                 confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)
#                 return "Successfully created dataview: " + dataclone_name

#         else:
#             # Create project page
#             create_parent_page(space=space, title=project)

#             project_id = confluence.get_page_id(
#                 space=space, 
#                 title=project
#             )
#             # Create parent page
#             create_child_page(space=space, parent_id=project_id, title=parent)

#             parent_id = confluence.get_page_id(
#                 space=space, 
#                 title=parent
#             )
#             # Create dataview page
#             create_child_page(space=space, parent_id=parent_id, title=title, body=body)

#             return "Successfully created dataview: " + dataview_name
#     except requests.exceptions.JSONDecodeError:
#         return "No Dataview API for " + dataview_name
#     except requests.exceptions.HTTPError as e:
#         return e.response.text

def create_parent_page(space=None, parent_id=None, title=None):
    confluence.create_page(space=space, parent_id=parent_id, title=title, body='')

def create_child_page(space=None, parent_id=None, title=None, body=None):
    confluence.create_page(space=space, parent_id=parent_id, title=title, body=body)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5555, debug=True)
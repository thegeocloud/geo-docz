GeoDocz API Readme

## OVERVIEW ##
- GeoDocz as a simple backend application that helps locate spatial documents on a map. Document metadata can be added to a database which is converted to a qr code. The qr code can be inserted into documents and later scanned to get information like lat/lon, desciption, name, and its unique id. It's easier to find documents via a map rather than the traditional folder structure.
- Projects organize documents where multiple documents can be related to a project. Currently project ids must be added to posted documents manually. Future realeases will automate this. 

## FUTURE WORK ##
- A front-end needs to be developed where location information can be added by clicking on a map. This information would be combined with other metadata and sent to the database. 
- Printed documents that are scanned could be located quickly on a map and even attached to that location. 


## GETTING STARTED ##
- Configuration
    Add your information for database and authentication information. This app utilizes Auth0 and requires an Auth0 domain and audience. 
    To learn more about this visit https://auth0.com/docs/api/management/v2/create-m2m-app 

- Authentication required to access all the endpoints listed below. Roles and permissions are listed as follows:
    Engineer
        Description
            - Engineers can add information related to documents. They also have read-only access to projects.

        Permissions
            - get/post/patch/delete:documents
            - get:projects

    Project Manager
        Description
            - Project Managers can add information related to documents and projects. They have full access to everything. 

        Permissions
            - get/post/patch/delete:documents
            - get/post/patch/delete:projects

- If you want to test locally without authentication, remove the @requires_auth decorator from the routes in app.py

- QR Codes
    QR codes are written to static/qrcodes. An example code image is included in the repository. 

## INSTALLING DEPENDENCIES ##
- Use PIP to install all dependencies in a virtual environment. 
- All dependencies are included in the requirements.txt file, use the following to install all dependencies:
    pip install -r requirements.txt


## RUNNING THE SERVER ##
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```
## FRONT END ## 
- No front end is included with this application.

## ERROR HANDLING ##
- Errors are returned as JSON objects in the following format:

    {
        'success': False, 
        'error': 400, 
        'message': 'bad request'
    }

- The API will reutrn two 400 and 422 errors when a request fails. 


## ENDPOINTS ##

# GET
GET /documents
 - Returns a list of document objects
 - Contains lat/lon and document id
 - Example:
    Request 
        curl http://127.0.0.1:5000/documents
    
    Response
        {
        "all_documents": [
            {
            "document_id": "qMPXTXrXez",
            "lat": 33.2029,
            "lon": 127.234324
            }], 
        "success": true
        }

GET /documents/<category>
 - Returns a list of document objects by a specific category
 - Contains lat/lon, category, document name, description and id
 - Example:
    Request 
        curl http://127.0.0.1:5000/documents/Asbuilt
    
    Response
        {
        "category": "Asbuilt",
        "documents_from_category": [
            {
            "category": "Asbuilt",
            "description": "Sidewalk improvements",
            "document_id": "khFdLuLAgR",
            "id": 36,
            "lat": 33.2029,
            "lon": 127.234324,
            "name": "Sidewalk"
            }]
        "success": true
        }

GET /documents/search
 - Returns a list of document objects based on a search term
 - Contains lat/lon, category, document name, description and id
 - Example:
    Request 
        curl http://127.0.0.1:5000/documents/a
    
    Response
        {
        "matched_documents": [
            {
            "category": "Legal",
            "description": "This project has been moved to La Mesa Blvd",
            "document_id": "qMPXTXrXez",
            "id": 15,
            "lat": 33.2029,
            "lon": 127.234324,
            "name": "La Mesa Blvd"
            }
        ],
        "search_term": "a",
        "success": true
        }

GET /projects
 - Returns a list of project objects
 - Contains project name, description and project manager
 - Example:
    Request 
        curl http://127.0.0.1:5000/projects
    
    Response
        {
        "projects": [
            {
            "description": "To improve median and street infrastructure along the Univeristy Ave corridor.",
            "id": 1,
            "project_manager": "Ken Burger",
            "project_name": "University Project"
            }
        ],
        "success": true,
        "total_projects": 15
        }

GET /projects/<project_manager>
 - Returns a list of project objects by projet manager
 - Contains project name, description and project manager
 - Example:
    Request 
        curl http://127.0.0.1:5000/projects/Ken
    
    Response
        {
        "project_manager": "Ken Burger",
        "projects": [
            {
            "description": "To improve median and street infrastructure along the Univeristy Ave corridor.",
            "id": 1,
            "project_manager": "Ken Burger",
            "project_name": "University Project"
            }
        ],
        "success": true
        }

# POST
POST /documents
 - Adds a new document object to the database
 - Example:
    Request 
        curl POST http://127.0.0.1:5000/documents
    
    Response
        {
        "new_document": {
            "category": "Asbuilt",
            "description": "Another improvement project",
            "document_id": "SuyGtUkmHW",
            "id": 50,
            "lat": 33.2029,
            "lon": 127.234324,
            "name": "Sidewalk"
        },
        "success": true
        }

POST /projects
 - Adds a new projects object to the database
 - Example:
    Request 
        curl POST http://127.0.0.1:5000/projects
    
    Response
        { "new_project": 
            { "description": "To improve median and street infrastructure along the Univeristy Ave corridor.", 
            "project_manager": "Ken Burger", "project_name": "University Project" 
            }, 
        "success": true 
        }

# PATCH
PATCH /documents
 - Updates and existing document in the database
 - Example:
    Request 
        curl PATCH http://127.0.0.1:5000/documents
    
    Response
        {
        "message": "Document updated",
        "success": true,
        "updated_document": {
            "category": "Legal",
            "description": "This is just a test update",
            "document_id": "CjGKGILsqR",
            "id": 33,
            "lat": 33.2029,
            "lon": 127.234324,
            "name": "Wow Update"
        }
        }

PATCH /projects
 - Updates and existing project in the database
 - Example:
    Request 
        curl PATCH http://127.0.0.1:5000/projects
    
    Response
        {
        "message": "Project updated",
        "success": true,
        "updated_project": {
            "description": "To improve median and street infrastructure along the Univeristy Ave corridor.",
            "id": 1,
            "project_manager": "Ken Burger",
            "project_name": "University Project"
            }
        }

# DELETE
DELETE /documents
 - Deletes an existing document in the database
 - Example:
    Request 
        curl DELETE http://127.0.0.1:5000/documents
    
    Response
        {
            "deleted_document": "Document was deleted fromt the database!",
            "success": true
        }

DELETE /projects
 - Deletes a project in the database
 - Example:
    Request 
        curl DELETE http://127.0.0.1:5000/projects
    
    Response
        {
            "deleted_project": "Project was deleted from the database!",
            "success": true
        }   




                                                                             

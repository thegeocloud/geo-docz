import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Document, Project
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        return response

    '''
    GET ENDPOINTS
    '''
    # Get lat/lon and document_id of ALL documents
    @app.route('/documents', methods=['GET'])
    @requires_auth('get:documents')
    def get_documents(payload):
        # Get all document coorindates and return as json
        try:
            all_documents = Document.query.all()
            formatted_documents = [{'lat': item.lat, 'lon': item.lon,
                                    'document_id': item.document_id} for item in all_documents]

            return jsonify({
                'success': True,
                'all_documents': formatted_documents
            })

        except BaseException:
            abort(404)

    # Get documents based on submitted category
    @app.route('/documents/<category>', methods=['GET'])
    @requires_auth('get:documents')
    def get_documents_by_category(payload, category):
        # Get all document coorindates by category
        try:
            all_documents = Document.query.filter(
                Document.category == category).all()

            formatted_documents = [item.format() for item in all_documents]

            if not all_documents:
                abort(404)

            return jsonify({
                'success': True,
                'documents_from_category': formatted_documents,
                'category': category
            })

        except BaseException:
            print(sys.exc_info())
            abort(404)

    # Get projects based
    @app.route('/projects/<project_manager>', methods=['GET'])
    @requires_auth('get:projects')
    def get_projects_by_project_manager(payload, project_manager):
        # Get all projects by project manager
        all_projects = Project.query.filter(
            Project.project_manager == project_manager).all()

        if not all_projects:
            abort(404)

        try:
            formatted_projects = [item.format() for item in all_projects]
            return jsonify({
                'success': True,
                'projects': formatted_projects,
                'project_manager': project_manager
            })

        except BaseException:
            print(sys.exc_info())
            abort(404)

    # Get documents based on search term
    @app.route('/documents/search', methods=['GET'])
    @requires_auth('get:documents')
    def get_documents_by_search_term(payload):
        body = request.get_json()
        search_term = body.get('search_term')

        # Get all document coorindates by category
        try:
            all_documents = Document.query.filter(
                Document.description.ilike("%" + search_term + "%")).all()

            if not all_documents:
                abort(404)

            formatted_documents = [item.format() for item in all_documents]

            return jsonify({
                'success': True,
                'matched_documents': formatted_documents,
                'search_term': search_term
            })

        except BaseException:
            abort(404)

        # Get lat/lon and document_id of ALL documents

    # Get all projects
    @app.route('/projects', methods=['GET'])
    @requires_auth('get:documents')
    def get_projects(payload):

        try:
            projects = Project.query.all()
            formatted_projects = [item.format() for item in projects]

            return jsonify({
                'success': True,
                'projects': formatted_projects,
                'total_projects': len(formatted_projects),
            })

        except BaseException:
            abort(404)

    '''
    POST ENDPOINTS
    '''
    # Add a new document to the database
    @app.route('/documents', methods=['POST'])
    @requires_auth('post:documents')
    def new_document(payload):
        body = request.get_json()

        # Get information from submitted
        lat = body.get('lat', None)
        lon = body.get('lon', None)
        category = body.get('category', None)
        name = body.get('name', None)
        description = body.get('description', None)
        document_id = Document.generate_document_id()

        try:
            new_document = Document(
                lat=lat,
                lon=lon,
                category=category,
                name=name,
                description=description,
                document_id=document_id)
            new_document.insert()

            # Generate QRcode using the document information
            document_formatted = new_document.format()
            Document.generate_qrcode(document_formatted)

            return jsonify({
                'success': True,
                'new_document': document_formatted,
            })

        except BaseException:
            print(sys.exc_info())
            abort(400)

    # Add a new project to the database
    @app.route('/projects', methods=['POST'])
    @requires_auth('post:projects')
    def new_project(payload):
        body = request.get_json()

        # Get information from submitted
        project_name = body.get('project_name', None)
        description = body.get('description', None)
        project_manager = body.get('project_manager', None)

        try:
            # Create new project object
            new_project = Project(
                project_name=project_name,
                description=description,
                project_manager=project_manager)
            new_project.insert()

            # Format project object and returnt to client
            formatted_project = {
                "project_name": new_project.project_name,
                "description": new_project.description,
                "project_manager": new_project.project_manager
            }

            return jsonify({
                'success': True,
                'new_project': formatted_project,
            })

        except BaseException:
            print(sys.exc_info())
            abort(400)

    '''
    PATCH ENDPOINTS
    '''
    # Update an existing documents information
    @app.route('/documents', methods=['PATCH'])
    @requires_auth('patch:document')
    def update_document(payload):
        body = request.get_json()
        description = body.get('description')
        name = body.get('name')
        category = body.get('category')
        document_id = body.get('document_id')
        update_document = Document.query.filter(
            Document.document_id == document_id).one_or_none()

        if not update_document:
            abort(404)

        try:
            update_document = Document.query.filter(
                Document.document_id == document_id).one_or_none()
            update_document.description = description
            update_document.name = name
            update_document.category = category
            update_document.update()

            return jsonify({
                'success': True,
                'updated_document': update_document.format(),
                'message': "Document updated"
            })

        except BaseException:
            abort(400)

    # Update an existing projects information
    @app.route('/projects', methods=['PATCH'])
    @requires_auth('patch:projects')
    def update_project(payload):
        # Get json from request body
        body = request.get_json()
        description = body.get('description', None)
        project_name = body.get('project_name', None)
        project_manager = body.get('project_manager', None)
        project_id = body.get('project_id', None)

        # Find the matching project by id
        update_project = Project.query.filter(
            Project.id == project_id).one_or_none()

        # Check if project exists and return 404 to client if not
        if not update_project:
            abort(404)

        try:
            # Update with new information
            update_project.description = description
            update_project.project_name = project_name
            update_project.project_manager = project_manager
            update_project.update()

            # Return data to client
            return jsonify({
                'success': True,
                'updated_project': update_project.format(),
                'message': "Project updated"
            })

        # Abort if an error occurs
        except BaseException:
            abort(400)

    '''
    DELETE ENDPOINTS
    '''
    # Delete a document from the database
    @app.route('/documents', methods=['DELETE'])
    @requires_auth('delete:documents')
    def delete_document(payload):
        body = request.get_json()
        document_id = body.get('document_id', None)

        # Get document so you can delete from database
        document = Document.query.filter(
            Document.document_id == document_id).one_or_none()

        if not document:
            abort(404)

        try:
            document.delete()
            return jsonify({
                'success': True,
                'deleted_document': "Document was deleted fromt the database!"
            })

        except BaseException:
            print(sys.exc_info())
            abort(400)

    # Delete a document from the database

    @app.route('/projects', methods=['DELETE'])
    @requires_auth('delete:projects')
    def delete_project(payload):
        # Get json from request
        body = request.get_json()
        project_id = body.get('project_id', None)

        # Get project so you can delete from database
        project = Project.query.filter(
            Project.id == project_id).one_or_none()

        if not project:
            abort(404)

        try:
            project.delete()
            return jsonify({
                'success': True,
                'deleted_project': "Project was deleted fromt the database!"
            })

        except BaseException:
            print(sys.exc_info())
            abort(400)

    '''
  ERROR HANDLING
  '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad_request'
        }), 400

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not_found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unable to process'
        }), 422

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

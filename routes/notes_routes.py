"""
Notes CRUD routes: GET, POST, PUT, DELETE /notes endpoints
"""

from flask import Blueprint, request, jsonify
from database import db
from models import Note, SharedNote
from auth import token_required
from utils import validate_note_data, sanitize_note_data

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['GET'])
@token_required
def get_all_notes(current_user):
    """
    Get all notes for authenticated user
    
    Endpoint: GET /notes
    Header: "Authorization": "Bearer <jwt_token>"
    
    Response: 200 OK with list of notes
    """
    try:
        # Get all notes created by the user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1 or per_page < 1 or per_page > 100:
            return jsonify({'message': 'Invalid pagination parameters'}), 400
        
        # Get notes created by user and notes shared with user
        user_notes = Note.query.filter_by(user_id=current_user.id).all()
        
        # Get shared notes
        shared_note_ids = db.session.query(SharedNote.note_id).filter_by(
            shared_with_user_id=current_user.id
        ).all()
        shared_notes = Note.query.filter(Note.id.in_([sn[0] for sn in shared_note_ids])).all()
        
        # Combine and deduplicate
        all_notes = list({note.id: note for note in user_notes + shared_notes}.values())
        all_notes.sort(key=lambda x: x.created_at, reverse=True)
        
        # Paginate
        paginated_notes = all_notes[(page-1)*per_page : page*per_page]
        
        return jsonify({
            'notes': [note.to_dict() for note in paginated_notes],
            'total': len(all_notes),
            'page': page,
            'per_page': per_page
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@notes_bp.route('/notes/<note_id>', methods=['GET'])
@token_required
def get_note(current_user, note_id):
    """
    Get a specific note by ID
    
    Endpoint: GET /notes/{id}
    Header: "Authorization": "Bearer <jwt_token>"
    
    Response: 200 OK with note data (user must own or have access)
    """
    try:
        note = Note.query.get(note_id)
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        # Check if user is author or has access via sharing
        is_author = note.user_id == current_user.id
        has_access = SharedNote.query.filter_by(
            note_id=note_id,
            shared_with_user_id=current_user.id
        ).first() is not None
        
        if not is_author and not has_access:
            return jsonify({'message': 'Access denied'}), 403
        
        return jsonify(note.to_dict()), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@notes_bp.route('/notes', methods=['POST'])
@token_required
def create_note(current_user):
    """
    Create a new note
    
    Endpoint: POST /notes
    Header: "Authorization": "Bearer <jwt_token>"
    Payload: {
        "title": "string",
        "content": "string"
    }
    
    Response: 201 CREATED with note data
    """
    try:
        data = request.get_json()
        
        # Validate note data
        is_valid, error = validate_note_data(data)
        if not is_valid:
            return jsonify({'message': error}), 400
        
        # Sanitize data
        clean_data = sanitize_note_data(data)
        
        # Create note
        new_note = Note(
            user_id=current_user.id,
            title=clean_data['title'],
            content=clean_data['content']
        )
        
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify(new_note.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@notes_bp.route('/notes/<note_id>', methods=['PUT'])
@token_required
def update_note(current_user, note_id):
    """
    Update an existing note
    
    Endpoint: PUT /notes/{id}
    Header: "Authorization": "Bearer <jwt_token>"
    Payload: {
        "title": "string",
        "content": "string"
    }
    
    Response: 200 OK with updated note data
    """
    try:
        note = Note.query.get(note_id)
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        # Check if user is author
        if note.user_id != current_user.id:
            return jsonify({'message': 'Only note author can update'}), 403
        
        data = request.get_json()
        
        # Validate note data
        is_valid, error = validate_note_data(data)
        if not is_valid:
            return jsonify({'message': error}), 400
        
        # Sanitize data
        clean_data = sanitize_note_data(data)
        
        # Update note
        note.title = clean_data['title']
        note.content = clean_data['content']
        
        db.session.commit()
        
        return jsonify(note.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@notes_bp.route('/notes/<note_id>', methods=['DELETE'])
@token_required
def delete_note(current_user, note_id):
    """
    Delete a note
    
    Endpoint: DELETE /notes/{id}
    Header: "Authorization": "Bearer <jwt_token>"
    
    Response: 204 No Content
    """
    try:
        note = Note.query.get(note_id)
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        # Check if user is author
        if note.user_id != current_user.id:
            return jsonify({'message': 'Only note author can delete'}), 403
        
        db.session.delete(note)
        db.session.commit()
        
        return '', 204
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@notes_bp.route('/search', methods=['GET'])
@token_required
def search_notes(current_user):
    """
    Search notes by keyword (STRETCH GOAL)
    
    Endpoint: GET /search?q=keyword
    Header: "Authorization": "Bearer <jwt_token>"
    
    Response: 200 OK with matching notes
    """
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'message': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'message': 'Search query must be at least 2 characters'}), 400
        
        # Search in user's notes and shared notes
        search_pattern = f'%{query}%'
        
        # User's own notes
        user_notes = Note.query.filter_by(user_id=current_user.id).filter(
            db.or_(
                Note.title.ilike(search_pattern),
                Note.content.ilike(search_pattern)
            )
        ).all()
        
        # Get shared notes
        shared_note_ids = db.session.query(SharedNote.note_id).filter_by(
            shared_with_user_id=current_user.id
        ).all()
        
        shared_notes = Note.query.filter(
            Note.id.in_([sn[0] for sn in shared_note_ids])
        ).filter(
            db.or_(
                Note.title.ilike(search_pattern),
                Note.content.ilike(search_pattern)
            )
        ).all()
        
        # Combine and deduplicate
        all_notes = list({note.id: note for note in user_notes + shared_notes}.values())
        all_notes.sort(key=lambda x: x.created_at, reverse=True)
        
        return jsonify({
            'results': [note.to_dict() for note in all_notes],
            'total': len(all_notes),
            'query': query
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
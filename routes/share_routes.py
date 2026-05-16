"""
Note sharing routes: POST /notes/{id}/share
"""

from flask import Blueprint, request, jsonify
from database import db
from models import Note, User, SharedNote
from auth import token_required
from utils import validate_email

share_bp = Blueprint('share', __name__)

@share_bp.route('/notes/<note_id>/share', methods=['POST'])
@token_required
def share_note(current_user, note_id):
    """
    Share a note with another user
    
    Endpoint: POST /notes/{id}/share
    Header: "Authorization": "Bearer <jwt_token>"
    Payload: {
        "share_with_email": "string"
    }
    
    Response: 200 OK with success message.
    After sharing, the user can access via GET /notes/{id}
    """
    try:
        note = Note.query.get(note_id)
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        # Check if user is author
        if note.user_id != current_user.id:
            return jsonify({'message': 'Only note author can share'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'Request body is required'}), 400
        
        share_with_email = data.get('share_with_email', '').strip()
        
        if not share_with_email:
            return jsonify({'message': 'share_with_email is required'}), 400
        
        # Validate email format
        if not validate_email(share_with_email):
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Find user to share with
        share_with_user = User.query.filter_by(email=share_with_email).first()
        
        if not share_with_user:
            return jsonify({'message': 'User not found'}), 404
        
        # Cannot share with self
        if share_with_user.id == current_user.id:
            return jsonify({'message': 'Cannot share note with yourself'}), 400
        
        # Check if note is already shared with this user
        existing_share = SharedNote.query.filter_by(
            note_id=note_id,
            shared_with_user_id=share_with_user.id
        ).first()
        
        if existing_share:
            return jsonify({'message': 'Note is already shared with this user'}), 409
        
        # Create share record
        shared_note = SharedNote(
            note_id=note_id,
            shared_with_user_id=share_with_user.id
        )
        
        db.session.add(shared_note)
        db.session.commit()
        
        return jsonify({
            'message': 'Note shared successfully',
            'shared_with': share_with_email,
            'note_id': note_id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@share_bp.route('/notes/<note_id>/unshare', methods=['POST'])
@token_required
def unshare_note(current_user, note_id):
    """
    Unshare a note with another user (BONUS FEATURE)
    
    Endpoint: POST /notes/{id}/unshare
    Header: "Authorization": "Bearer <jwt_token>"
    Payload: {
        "unshare_with_email": "string"
    }
    
    Response: 200 OK with success message
    """
    try:
        note = Note.query.get(note_id)
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        # Check if user is author
        if note.user_id != current_user.id:
            return jsonify({'message': 'Only note author can unshare'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'Request body is required'}), 400
        
        unshare_with_email = data.get('unshare_with_email', '').strip()
        
        if not unshare_with_email:
            return jsonify({'message': 'unshare_with_email is required'}), 400
        
        # Validate email format
        if not validate_email(unshare_with_email):
            return jsonify({'message': 'Invalid email format'}), 400
        
        # Find user to unshare with
        unshare_with_user = User.query.filter_by(email=unshare_with_email).first()
        
        if not unshare_with_user:
            return jsonify({'message': 'User not found'}), 404
        
        # Find and delete share record
        shared_note = SharedNote.query.filter_by(
            note_id=note_id,
            shared_with_user_id=unshare_with_user.id
        ).first()
        
        if not shared_note:
            return jsonify({'message': 'Note is not shared with this user'}), 404
        
        db.session.delete(shared_note)
        db.session.commit()
        
        return jsonify({
            'message': 'Note unshared successfully',
            'unshared_with': unshare_with_email,
            'note_id': note_id
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500
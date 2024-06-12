from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Add a note.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # Load the JSON data from the request
    noteId = note['noteId']  # Get the note ID from the JSON data
    note = Note.query.get(noteId)  # Query the database for the note with the given ID
    if note:
        if note.user_id == current_user.id:  # Check if the current user owns the note
            db.session.delete(note)  # Delete the note from the database session
            db.session.commit()  # Commit the session to remove the note from the database
            
    return jsonify({})  # Return an empty JSON response


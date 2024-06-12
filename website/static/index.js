// Define a function to delete a note, accepting the note ID as a parameter
function deleteNote(noteId) {
    // Use the fetch API to send a POST request to the /delete-note endpoint
    fetch('/delete-note', {
        method: 'POST',  // Specify the HTTP method as POST
        body: JSON.stringify({noteId: noteId}),  // Convert the note ID to a JSON string and include it in the request body
    }).then((_res) => {
        // After the request is completed, reload the page to reflect the changes
        window.location.href = "/";
    });
}
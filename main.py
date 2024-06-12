from website import create_app # Import the create_app function from the website module

# Create an instance of the Flask app by calling the create_app function
app = create_app()

#To run app
if __name__ == '__main__': # Check if this script is being run directly (not imported as a module)
    app.run(debug=True) # Start the Flask app in debug mode, which provides helpful error messages and auto-reloading


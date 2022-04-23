from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # when make changes, auto rerun the web server
from app.app import create_app
app = create_app(config_filename='',type_db=None, silent=True)

if __name__ == '__main__':
    app.run(debug=True)

    
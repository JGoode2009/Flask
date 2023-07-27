from flaskblog import app

if __name__ == '__main__':
    # with app.app_context():  just took out to see if it is causing the unique constraint to fail, it's not
    #     db.create_all()
    app.run()
    # if ran in debug mode creates issues with adduser running multiple times creating errors
from diary import create_app

app = create_app()



# Ensures app is initialized only from this file
if __name__ == '__main__':
    app.run(debug=True, port=5001) 
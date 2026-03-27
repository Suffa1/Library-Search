from flask import Flask, render_template

app = Flask(__name__)




@app.route("/welcome")

def hello():

    return render_template('home.html')




if __name__ == '__main__':

    # Chạy ứng dụng ở chế độ debug

    app.run(debug=False)
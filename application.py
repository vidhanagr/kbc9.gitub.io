from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcdef"

currentques=0

def checkanswer(option):
	conn = sqlite3.connect('quiz.db')
	cur = conn.cursor()

	cur.execute("SELECT answer FROM questions WHERE id=?", (currentques,))
	result = cur.fetchone()
	print(result)

	cur.close()
	conn.close()
	return False if result is None or result[0] != option else True

def getquizdata():
	global currentques
	conn = sqlite3.connect('quiz.db')
	cur = conn.cursor()


	cur.execute("SELECT * FROM questions WHERE id=?", (currentques+1,))
	result = cur.fetchone()

	cur.close()
	conn.close()
	currentques = (currentques+1)%16
	return result

def authenticateUser(username, password):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("SELECT password FROM user WHERE username=?", (username,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    print('Password obtained from DB is', result)

    return False if result is None or result[0] != password else True

def addToDatabase(fname, lname, email, username, password):

    conn = sqlite3.connect('userdata.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO user(fname, lname, email, username, password) VALUES(?, ?, ?, ?, ?)",
     (fname, lname, email, username, password))

    conn.commit()

    cur.close()
    conn.close()

    print('User added to DB', (fname, lname, email, username, password))

@app.route('/', methods=["GET", "POST"])
def homepage():
    ''' Homepage of the website '''

    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    ''' Login page for users '''
    if "user" in session:
        return redirect("/video")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if authenticateUser(username, password):
            session["user"] = username
            return redirect("/video")
        else:
        	return render_template("login.html")
    else:
    	return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def createAccount():
    """ Register an account """

    if request.method == "GET":
        return render_template("register.html")

    else:

        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        addToDatabase(fname, lname, email, username, password)

        return redirect("/")

@app.route('/video', methods=["GET", "POST"])
def videopage():
    ''' Homepage of the website '''

    return render_template("video.html")

@app.route('/quiz', methods=["GET", "POST"])
def quizControler():
	if request.method == "GET":
		result = getquizdata()
		return render_template("quiz.html", qid = result[0], option1 = result[2], option2 = result[3], option3 = result[4], option4 = result[5], question = result[1])
	else:
		selectedoption = request.form.get("radio")
		print(selectedoption)
		if checkanswer(selectedoption):
			return redirect("/quiz")
		else:
			return render_template("video.html.")
		return render_template("login.html")

if __name__ == "__main__":
	app.run(debug=True)

from distutils.log import error
from flask import Flask, abort, request, make_response, redirect, render_template, g
from user_service import get_user_with_credentials, logged_in
from account_service import get_balance, do_transfer, get_accounts
from flask_wtf.csrf import CSRFProtect
from waiting import wait
import time

def display_error(error):
    return render_template('error.html', error_message=error)

app = Flask(__name__)
# Here we register these error handlers so that they go through our custom error page
# rather than ending up with the defaults
app.register_error_handler(404, display_error)
app.register_error_handler(400, display_error)
# We have the 500 error here, so that any internal issues don't end up crashing our app entirely.
app.register_error_handler(500, display_error)
# Change this secret key to your specific secret.
app.config['SECRET_KEY'] = 'W9h3o5o7p868d68i0di68s868c8o68opp866o5oip54s4c5o7o85p4d4i44di'
# This enables Cross Site request forgery throughout the entirety of the flask app!
# Note that it CSRF protection requires a secret key to securely sign the token. 
# By default this will use the Flask app’s SECRET_KEY. If you’d like to use a 
# separate token you can set WTF_CSRF_SECRET_KEY. In addition to this line, be sure
# to add a hidden input for every form containing your secure token
csrf = CSRFProtect(app) 

@app.route("/", methods=['GET'])
def home():
    if not logged_in():
        return render_template("login.html")
    return redirect('/dashboard')

@app.route("/login", methods=["POST"])
def login():
    start_time = time.perf_counter()
    codename = request.form.get("codename")
    password = request.form.get("password")
    user = get_user_with_credentials(codename, password)
    if not user:
        wait(lambda:time.perf_counter() - start_time > 2)
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    wait(lambda:time.perf_counter() - start_time > 2)
    return response, 303
    
@app.route("/dashboard", methods=['GET'])
def dashboard():
    if not logged_in():
        return render_template("login.html")
    return render_template("dashboard.html", user=g.user)

@app.route("/details", methods=['GET'])
def details():
    if not logged_in():
        return render_template("login.html")
    account_number = request.args['account']
    # Note: By returning a render template with specified variables passed in, we are able
    #       to prevent XSS attacks. Our html will not have access to our cookies or stored
    #       data because render_templates automatically prevents XSS attacks!!!
    return render_template(
        "details.html", 
        user=g.user,
        account_number=account_number,
        balance = get_balance(account_number, g.user))

@app.route("/accounts", methods=['GET'])
def accounts():
    if not logged_in():
        return render_template("login.html")
    stockpiles = get_accounts(g.user)
    return render_template("accounts.html",
        accounts=stockpiles,
        user=g.user)


@app.route("/transfer", methods=["POST"])
def transfer():
    if not logged_in():
        return render_template("login.html")
    # Note: We make sure that every request, regardless of their status 
    #       gives you the same response time, so you cannot deduce the
    #       reasons behind the timing difference. In this case, all
    #       transfers have a duration of at least 4 seconds.
    start_time = time.perf_counter()
    source = request.form.get("from")
    target = request.form.get("to")
    # Note: All value errors and invalid value type errors abort with a status
    #       of 400. Similarly, all account non-ownership issues abort with as 
    #       status 404. This is because we want to make sure that hackers
    #       can't perform user enumeration attacks to find out what accounts exist
    try: 
        amount = int(request.form.get("amount"))
    except ValueError:
        wait(lambda:time.perf_counter() - start_time > 4)
        abort(400, "Not a valid amount")
    if amount < 0:
        wait(lambda:time.perf_counter() - start_time > 4)
        abort(400, "NO STEALING")
    if amount > 1000:
        wait(lambda:time.perf_counter() - start_time > 4)
        abort(400, "WOAH THERE TAKE IT EASY")

    available_balance = get_balance(source, g.user)
    if available_balance is None:
        abort(404, "Account not found")
    if amount > available_balance:
        abort(400, "You don't have that much")

    if do_transfer(source, target, amount):
        pass
    else:
        abort(400, "Something bad happened")

    response = make_response(redirect("/dashboard"))
    return response, 303

@app.route("/transfer", methods=["GET"])
def transfer_page():
    if not logged_in():
        return render_template("login.html")
    return render_template("transfer.html")
    

@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie('auth_token')
    return response, 303

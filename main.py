from flask import Flask, request, render_template, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

# without this handler, error "Method not allowed" is displayed
@app.route('/index')
def display_form():
    return render_template('index.html')

@app.route('/index', methods=["POST"])
def validate_fields():

    user_name_err = ''
    passwd_err = ''
    verify_passwd_err = ''
    email_err = ''

    user_name = request.form['user_name']
    passwd = request.form['passwd']
    verify_passwd = request.form['verify_passwd']
    email = request.form['email']

    # validate data input
    if request.method == 'POST':

        if user_name == '':
            user_name_err = 'Username cannot be empty'
            #user_name = ''

        elif ' ' in user_name:
            user_name_err = 'Username cannot have spaces'
            #user_name = ''

        elif len(user_name) < 3 or len(user_name) > 20:
            user_name_err = 'Username is invalid - needs to be (3-20) characters long'
            #user_name = ''

        if passwd == '':
            passwd_err = 'Password cannot be empty'

        elif ' ' in passwd:
            passwd_err = 'Password cannot have spaces'
    
        elif len(passwd) < 3 or len(passwd) > 20:
            passwd_err = 'Password is invalid - needs to be (3-20) characters long'

        if verify_passwd != passwd:
            verify_passwd_err = "User's password and password-confirmation do not match"

        if passwd_err or verify_passwd_err:
            verify_passwd = ''
            passwd = ''

        if ' ' in email:
            email_err = 'Email cannot have spaces'

        elif email != '' and (len(email) < 3 or len(email) > 20):
            email_err = 'Email is invalid - needs to be (3-20) characters long'

        elif email != '' and '@' not in email:
            email_err = "Email has to have a single @"
        
        elif email != '' and '.' not in email:
            email_err = "Email has to have a single period"
        
        elif email.count('@') > 1:
            email_err = "Email cannot have more than one @"
        
        elif email.count('.') > 1:
            email_err = "Email cannot have more than one ."
        else:
            email_err = ''

        if not user_name_err and not passwd_err and not verify_passwd_err and not email_err:
            # if no input errors found, redirect page with query string
            return redirect('/welcome?user_name={0}'.format(user_name))
        else:
            return render_template("index.html", name=user_name,
             user_name_err=user_name_err, passwd_err=passwd_err, 
             verify_passwd_err=verify_passwd_err, email=email, email_err=email_err)

    # if request not 'POST'
    return render_template('index.html')


    # /welcome is a url/path which is associated with function or view welcome()
@app.route('/welcome')
def welcome():
    # request.args.get() gets query parameters 
    user_name = request.args.get('user_name')
    return render_template('welcome.html', name=user_name)
    

if __name__ == "__main__":
    app.run()
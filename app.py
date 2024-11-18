from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import channels_db
import login_verification
import users_db

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'IJvo345vjEJJIij.g5<<5844vc5f47'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session:
            flash("You must be logged to access this page.")
            return redirect(url_for('index'))

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session or session['role'] != 1:
            url = request.path

            if url[0:9] == "/channels" and session:
                flash("You must be admin to modify this table.")
                return redirect(url_for('channels'))

            elif url[0:11] == "/animations" and session:
                flash("You must be admin to modify this table.")
                return redirect(url_for('animations'))

            else:
                flash("You must be admin to access this page.")
                return redirect(url_for('index'))

        return f(*args, **kwargs)

    return decorated_function


def no_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session and "_flashes" not in session:
            flash("Actually you're logged.")
            return redirect(url_for('index'))

        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/channels')
@login_required
def channels():
    all_channels = channels_db.get_channels()
    return render_template("channels.html", channels=all_channels)


@app.route('/channels/new_channel', methods=["GET", "POST"])
@admin_required
def new_channel():
    if request.method == 'GET':
        return render_template("new_channel.html")
    else:
        name = request.form['name']
        image_url = request.form['image_url']
        founder = None if request.form['founder'] == "" else request.form['founder']
        launch_date = None if request.form['launch_date'] == "" else request.form['launch_date']
        description = None if request.form['description'] == "" else request.form['description']

        channels_db.channel_creation(name, image_url, founder, launch_date, description)

        return redirect(url_for('channels'))


@app.route('/channels/<channel_id>/delete')
@admin_required
def delete_channel(channel_id):
    channels_db.channel_deletion(channel_id)
    return redirect(url_for('channels'))


@app.route('/channels/<channel_id>/modify', methods=["GET", "POST"])
@admin_required
def modify_channel(channel_id):
    all_channels = channels_db.get_channels()

    for channel in all_channels:
        if channel["channel_id"] == int(channel_id):
            if request.method == 'GET':
                return render_template("modify_channel.html", channel=channel)
            else:
                name = request.form['name']
                image_url = request.form['image_url']
                founder = None if request.form['founder'] == "" else request.form['founder']
                launch_date = None if request.form['launch_date'] == "" else request.form['launch_date']
                description = None if request.form['description'] == "" else request.form['description']

                channels_db.channel_modification(name, image_url, founder, launch_date, description, channel_id)

                return redirect(url_for('channels'))


@app.route('/animations')
@login_required
def animations():
    all_channels = channels_db.get_channels()
    shows = channels_db.get_shows()
    return render_template("animations.html", channels=all_channels, shows=shows)


@app.route('/animations/new_animation', methods=["GET", "POST"])
@admin_required
def new_animation():
    all_channels = channels_db.get_channels()
    if request.method == 'GET':
        return render_template("new_animation.html", channels=all_channels)
    else:
        title = request.form['title']
        image_url = request.form['image_url']
        release_date = request.form['release_date']
        director = None if request.form['director'] == "" else request.form['director']
        episodes = None if request.form['episodes'] == "" else request.form['episodes']
        channel_id = None if request.form['channel_id'] == "0" else request.form['channel_id']
        synopsis = None if request.form['synopsis'] == "" else request.form['synopsis']

        channels_db.animation_creation(title, image_url, release_date, director, episodes, channel_id, synopsis)

        return redirect(url_for('animations'))


@app.route('/animations/<animation_id>/delete')
@admin_required
def delete_animation(animation_id):
    channels_db.animation_deletion(animation_id)
    return redirect(url_for('animations'))


@app.route('/animations/<animation_id>/modify', methods=["GET", "POST"])
@admin_required
def modify_animation(animation_id):
    all_channels = channels_db.get_channels()
    shows = channels_db.get_shows()

    for show in shows:
        if show['animation_id'] == int(animation_id):
            if request.method == 'GET':
                return render_template("modify_animation.html", channels=all_channels, show=show)
            else:
                title = request.form['title']
                image_url = request.form['image_url']
                release_date = request.form['release_date']
                director = None if request.form['director'] == "" else request.form['director']
                episodes = None if request.form['episodes'] == "" else request.form['episodes']
                channel_id = None if request.form['channel_id'] == "0" else request.form['channel_id']
                synopsis = None if request.form['synopsis'] == "" else request.form['synopsis']

                channels_db.animation_modification(title, image_url, release_date, director, episodes, channel_id,
                                                   synopsis, animation_id)

                return redirect(url_for('animations'))


@app.route('/login', methods=["GET", "POST"])
@no_login
def form_login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']

        existent_user, role, user_id = login_verification.check_session(username, password)
        if existent_user:
            session['id'] = user_id
            session['username'] = username
            session['role'] = role
        else:
            flash("Incorrect username or password. Try Again.")

        return redirect(url_for('form_login'))


@app.route('/logout')
@login_required
def logout():
    user = session['username']
    session.clear()

    flash(f"The session for user {user} has been closed correctly.")
    return redirect(url_for('index'))


@app.route('/register', methods=["GET", "POST"])
@no_login
def form_register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = request.form['password']
        role = 0
        non_existent_user, crypt_password = login_verification.check_exist(username, password)

        if non_existent_user:
            users_db.user_creation(username, crypt_password, role)
            flash(f"The user {username} has been registered successfully.")
            return redirect(url_for('form_register'))

        else:
            flash("Username already exist. Try Again.")

        return redirect(url_for('form_register'))


@app.route('/users_table')
@admin_required
def users():
    all_users = users_db.get_users()
    return render_template("users.html", all_users=all_users)


@app.route('/users_table/new_user', methods=["GET", "POST"])
@admin_required
def new_user():
    if request.method == 'GET':
        return render_template("new_user.html")
    else:
        username = request.form['username']
        password = request.form['password']
        role = int(request.form['admin_role'])
        non_existent_user, crypt_password = login_verification.check_exist(username, password)

        if non_existent_user:
            users_db.user_creation(username, crypt_password, role)
            flash(f"User {username} has been registered successfully.")
            return redirect(url_for('users'))

        else:
            flash(f"The user {username} already exist. Try Again.")
            return redirect(url_for('new_user'))


@app.route('/users_table/<user_id>/delete')
@admin_required
def delete_user(user_id):
    if int(user_id) == 1:
        flash("You can't delete the admin user.")
    else:
        users_db.user_deletion(user_id)
        if int(user_id) == session['id']:
            return redirect(url_for('logout'))

    return redirect(url_for('users'))


@app.route('/users_table/<user_id>/modify', methods=["GET", "POST"])
@admin_required
def modify_user(user_id):
    for user in users_db.get_users():
        if int(user_id) == 1:
            flash("You can't modify the admin user.")
            return redirect(url_for('users'))

        elif user['id'] == int(user_id):
            if request.method == 'GET':
                return render_template("modify_user.html", user=user)
            else:
                username = request.form['username']
                password = request.form['password']
                role = int(request.form['admin_role'])
                non_existent_user, crypt_password = login_verification.check_exist(username, password, user['username'])

                if non_existent_user:
                    users_db.user_modification(user['id'], username, crypt_password, role)

                    if session['id'] == int(user_id):
                        return redirect(url_for('logout'))

                    return redirect(url_for('users'))

                else:
                    flash(f"The user {username} already exist. Try Again.")
                    return redirect(url_for('modify_user', user_id=user_id))


@app.route('/profile/<user_id>', methods=["GET", "POST"])
@login_required
def profile(user_id):
    if int(user_id) == session['id'] and session['role'] == 0:
        if request.method == 'GET':
            return render_template("profile.html")

        else:
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            password = login_verification.crypt_password(new_password)

            checked = login_verification.check_session(session['username'], old_password)
            if checked[0]:
                users_db.user_modification(user_id, session['username'], password, session['role'])
                flash("Password changed successfully.")
            else:
                flash("Your current password is wrong. Try again.")

            return redirect(url_for('profile', user_id=user_id))

    if session['role'] == 1:
        flash("Actual session have admin role so you don't have access to profile.")
    else:
        flash("You can't access other users profile.")

    return redirect(url_for('index'))


@app.route('/profile/<user_id>/delete')
@login_required
def profile_delete(user_id):
    if int(user_id) == 1:
        flash("You can't delete the admin user.")
        return redirect(url_for('index'))

    elif session['id'] == int(user_id):
        users_db.user_deletion(user_id)
        return redirect(url_for('logout'))

    flash("You can't access other users profile.")
    return redirect(url_for('index'))


@app.route('/api/channels')
def get_json_channels():
    return channels_db.get_channels()


@app.route('/api/channels/<channel_id>')
def channel_api(channel_id):
    for channel in channels_db.get_channels():
        if channel['channel_id'] == int(channel_id):
            return channel

    return redirect(url_for('get_json_channels'))


@app.route('/api/animations')
def get_json_animations():
    return channels_db.get_shows()


@app.route('/api/animations/<animation_id>')
def animation_api(animation_id):
    for animation in channels_db.get_shows():
        if animation['animation_id'] == int(animation_id):
            return animation

    return redirect(url_for('get_json_animations'))


@app.route('/api/users')
def get_json_users():
    users_list = []
    for user in users_db.get_users():
        users_list.append(
            {'user_id': user['id'], 'username': user['username'], 'admin_role': True if user['role'] == 1 else False})

    return users_list


@app.route('/api/users/<user_id>')
def user_api(user_id):
    for user in users_db.get_users():
        if user['id'] == int(user_id):
            search_user = {'user_id': user['id'], 'username': user['username'],
                           'admin_role': True if user['role'] == 1 else False}
            return search_user

    return redirect(url_for('get_json_users'))


if "__main__" == __name__:
    app.run(debug=False, host='0.0.0.0', port=8080)

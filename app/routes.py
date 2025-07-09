from flask import (
    current_app,
    render_template,
    flash,
    redirect,
    url_for,
    request,
    abort,
    send_from_directory,
    jsonify,
)
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProjectForm, ProjectUpdateForm
from app.models import User, Project, ProjectUpdate, UpdatePhoto, Visit
from methods.images import validate_image
from werkzeug.urls import url_parse
import subprocess
import os


@app.route("/")
@app.route("/index")
def index():
    store_visit(request, "index")
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/AlphabeticalClock/")
def alphabetical_clock():
    vite_build_dir = os.path.join(current_app.root_path, '..', 'AlphabeticalClock', 'dist')
    return send_from_directory(vite_build_dir, "index.html")


@app.route("/AlphabeticalClock/<path:filename>")
def submodule_static(filename):
    vite_build_dir = os.path.join(current_app.root_path, '..', 'AlphabeticalClock')
    return send_from_directory(vite_build_dir, filename)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"You registered {user.username} as a user!")
        logout_user()
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/about")
def about():
    store_visit(request, "about")
    return render_template("about.html", title="More About Rylan")


@app.route("/contact")
def contact():
    store_visit(request, "contact")
    return render_template("contact.html", title="Contact Rylan")


@app.route("/portfolio")
def portfolio():
    store_visit(request, "portfolio")
    projects = Project.query.all()
    return render_template("portfolio.html", title="Projects", projects=projects)


@app.route("/project/<proj_num>")
def project(proj_num):
    store_visit(request, f"project{proj_num}")
    project = Project.query.filter_by(id=proj_num).first()
    updates = list(project.updates).copy()
    updates.sort(reverse=True)
    if project is None:
        flash("That link appears to be broken. Sorry!")
        return redirect(url_for("portfolio"))
    return render_template(
        "project.html", title=project.name, project=project, updates=updates
    )


@app.route("/project/new", methods=["GET", "POST"])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, desc=form.desc.data)
        db.session.add(project)
        db.session.commit()
        flash(f"You created the Project {project.name}")
        return redirect(url_for("project", proj_num=project.id))
    return render_template("new_project.html", title="Create Project", form=form)


@app.route("/project/<proj_num>/update", methods=["GET", "POST"])
@login_required
def new_update(proj_num):
    form = ProjectUpdateForm()
    project = Project.query.filter_by(id=proj_num).first()
    if project is None:
        flash("The project id provided does not refer to a valid project")
        return redirect(url_for("portfolio"))
    if form.validate_on_submit():
        update = ProjectUpdate(
            title=form.title.data, text=form.text.data, project=project
        )
        db.session.add(update)
        db.session.commit()
        # now upload photos
        file_num = 1
        for uploaded_file in request.files.getlist("photo"):
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            if file_ext not in app.config[
                "UPLOAD_EXTENSIONS"
            ] or file_ext != validate_image(uploaded_file.stream):
                flash(f"The file does not appear to be a valid image file")
                abort(400)
            filename = f"{project.id:04}_{update.id:04}_{file_num:02}{file_ext}"
            uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], filename))
            f = UpdatePhoto(filename=filename, update=update)
            db.session.add(f)
            db.session.commit()
            file_num += 1
        flash(f"You created a new ProjectUpdate")
        return redirect(url_for("project", proj_num=project.id))
    return render_template(
        "new_update.html", title="Update Project", project=project, form=form
    )


@app.route("/project/<proj_num>/update/<update_num>", methods=["GET", "POST"])
@login_required
def edit_update(proj_num, update_num):
    form = ProjectUpdateForm()
    project = Project.query.filter_by(id=proj_num).first()
    update = ProjectUpdate.query.filter_by(id=update_num).first()
    if project is None or update is None:
        flash("The ids passed to the updater are invalid")
        return redirect(url_for("portfolio"))
    if form.validate_on_submit():
        update.title = form.title.data
        update.text = form.text.data
        db.session.add(update)
        db.session.commit()
        flash(f"You successfully modified the project update")
        return redirect(url_for("project", proj_num=project.id))
    elif request.method == "GET":
        form.title.data = update.title
        form.text.data = update.text
    return render_template(
        "new_update.html", title="Modify Update", project=project, form=form
    )


@app.route("/garage")
@login_required
def garage():
    return render_template("garage.html", title="GaragePi")


@app.route("/garage/<door_num>/<door_command>")
@login_required
def garage_toggle(door_num, door_command):
    if door_command not in ["open", "close"]:
        return jsonify({"door": door_num, "status": f"invalid command {door_command}"})
    if door_num in ["1", "2"]:
        try:
            cmd = [
                "ssh",
                "network-files-remote",
                f"~/.garage.sh {door_command} {door_num}",
            ]
            result = subprocess.run(cmd)
        except subprocess.CalledProcessError as e:
            print(f"Command {command} failed with error:\n{e}")
        except Exception as e:
            print(f"Error occurred: {e}")
        return jsonify({"door": door_num, "status": "changing"})


@app.route("/garage/<door_num>/check")
@login_required
def garage_check(door_num):
    if door_num in ["1", "2"]:
        try:
            cmd = ["ssh", "network-files-remote", f"~/.garage.sh check {door_num}"]
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Command {command} failed with error:\n{e}")
        except Exception as e:
            print(f"Error occurred: {e}")
        return jsonify(
            {"door": door_num, "status": result.stdout.split(" ")[-1].strip()}
        )


@app.route("/uploads/<filename>")
def upload(filename):
    print(os.path.join(app.config["UPLOAD_PATH"], filename))
    return send_from_directory(os.path.join("../", app.config["UPLOAD_PATH"]), filename)


@app.route("/linkedin")
def linkedin():
    store_visit(request, "linkedin")
    return redirect("https://linkedin.com/in/rylan-sturm/")


@app.route("/github")
def github():
    store_visit(request, "github")
    return redirect("https://github.com/rylansturm")


def get_ip(req):
    if req.environ.get("HTTP_X_FORWARDED_FOR") is None:
        return req.environ["REMOTE_ADDR"]
    else:
        return req.environ["HTTP_X_FORWARDED_FOR"]


def store_visit(request, page_to):
    try:
        ip = get_ip(request)
        page_from = request.args.get("page_from")
        visit = Visit()
        visit.visitor_ip = ip
        visit.page_to = page_to
        visit.page_from = page_from
        db.session.add(visit)
        db.session.commit()
    except:
        pass

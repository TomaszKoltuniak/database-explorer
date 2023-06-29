from flask import Flask, redirect, render_template, request, url_for
import json, os, sqlite3, requests, click
from flask_login import (
    LoginManager,
    current_user,
    UserMixin,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from db import (
    init_db_command,
    get_companies,
    get_column_values,
    get_columns_names,
    add_company,
    add_comments,
    edit_company,
    edit_comments,
    delete_company,
)
from user import User


GOOGLE_SPREADSHEET_NAME = "Malmo interns db"
WORKSHEET_NAMES = ["Automatic", "Architects"]
COLUMNS_DICT = {
    "company_name": "Company name",
    "field_of_work": "Field of work",
    "address": "Address",
    "mentor": "Name of Mentor/ Contact person",
    "phone_number": "Phone number",
    "email": "Email",
    "website": "Website",
    "max_students": "Max number of students",
    "current_students": "Current student count",
    "status": "Status",
    "commute": "Commute",
    "equipment": "Required additional equipment/ clothes",
    "info": "Important information",
    "creation_date": "Creation date",
    "last_update": "Last update",
}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
login_manager = LoginManager(app)
client = WebApplicationClient(os.environ.get("GOOGLE_CLIENT_ID"))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


try:
    init_db_command()
except sqlite3.OperationalError:
    pass


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        if current_user.privileges == "guest":
            return render_template(
                "guest.html", email=current_user.email, name=current_user.name
            )
        else:
            all_companies = get_companies()
            company_name = request.form.get("company_name")
            field_of_work = request.form.get("field_of_work")
            output = get_companies(company_name, field_of_work)
            companies_names = get_column_values("Company name")
            fields = get_column_values("Field of work")
            columns = get_columns_names()
            if current_user.privileges in ["admin", "privileged", "user"]:
                template_name = f"{current_user.privileges}.html"
                return render_template(
                    template_name,
                    email=current_user.email,
                    name=current_user.name,
                    companies_names=companies_names,
                    fields=fields,
                    columns=columns,
                    output=output or all_companies,
                )
            else:
                return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(
            os.environ.get("GOOGLE_CLIENT_ID") or "",
            os.environ.get("GOOGLE_CLIENT_SECRET") or "",
        ),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google."

    user = User.get(unique_id)
    if not user:
        User.create(unique_id, users_name, users_email, "guest")

    try:
        login_user(user)
    except:
        return redirect(url_for("index"))

    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(
        "https://accounts.google.com/.well-known/openid-configuration"
    ).json()


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST" and current_user.privileges in ["admin", "privileged"]:
        new_record = {}
        for key, value in COLUMNS_DICT.items():
            new_record[value] = request.form.get(key)
        new_id = add_company(new_record)
        add_comments(request.form.getlist("comment"), current_user.name, new_id)
        return redirect(url_for("index"))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST" and current_user.privileges in ["admin", "privileged"]:
        edited_record = {}
        for key, value in COLUMNS_DICT.items():
            edited_record[value] = request.form.get(f'{key}')

        edited_record["id"] = request.form.get("e_id")
        edit_company(edited_record)
        edit_comments(request.form.getlist(), current_user.name, edited_record["id"])
        return redirect(url_for("index"))
    

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST" and current_user.privileges in ["admin", "privileged"]:
        delete_company(request.form.get("d_id"))
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)

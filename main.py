import requests
from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class AddCafeForm(FlaskForm):
    cafe = StringField('Cafe name', name="name", validators=[DataRequired()])
    price = StringField('Price', name="coffee_price", validators=[DataRequired()])
    location = StringField('location', name="loc", validators=[DataRequired()])
    img_url = StringField('image url', name="img_url", validators=[DataRequired(), URL()])
    map_url = StringField('Map URL', name="map_url", validators=[URL(), DataRequired()])
    seats = StringField(label="No.of. Seats", name="seats", validators=[DataRequired()])
    has_toilet = SelectField(label='toilet', name="toilet", validators=[DataRequired()], choices=['yes', 'no'])
    has_wifi = SelectField(label='WiFi', name="wifi", validators=[DataRequired()], choices=['yes', 'no'])
    has_socket = SelectField(label='Sockets', name="sockets", validators=[DataRequired()], choices=['yes', 'no'])
    allow_call = SelectField(label='Allow phone', name="calls", validators=[DataRequired()], choices=['yes', 'no'])
    submit = SubmitField(label="Add Cafe")


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        searched_loc = requests.post(url="https://cafe-yuk2.onrender.com/search",
                                     params={'loc': request.form.get('loc')})
        for key in dict(searched_loc.json()):
            if key == 'cafe':
                return render_template("index.html", cafes=searched_loc.json()['cafe'], status=True)
            else:
                return render_template('index.html', msg=searched_loc.json()['error'], status=False)
    return render_template("index.html", cafes=requests.get("https://cafe-yuk2.onrender.com/all").json()['cafe'],
                           status=True)


@app.route("/post<id_>")
def post(id_):
    response = requests.get("https://cafe-yuk2.onrender.com/all")
    post_ = response.json()['cafe'][id_]
    print(type(post_["has_wifi"]))
    return render_template("post.html", post=post_)


@app.route("/add", methods=["POST", "GET"])
def add_cafe():
    form_ = AddCafeForm()
    if form_.validate_on_submit():
        print(form_.allow_call.data == 'Yes')
        add_param = {
            "cafe": form_.cafe.data,
            "coffee_price": form_.price.data,
            "loc": form_.location.data,
            "img_url": form_.img_url.data,
            "map_url": form_.map_url.data,
            "seats": form_.seats.data,
            "toilet": int(form_.has_toilet.data == 'yes'),
            "wifi": int(form_.has_wifi.data == 'yes'),
            "sockets": int(form_.has_socket.data == 'yes'),
            "calls": int(form_.allow_call.data == 'yes')
        }
        print(add_param["toilet"])
        postt = requests.post(url="https://cafe-yuk2.onrender.com/add", params=add_param)
        print(postt.status_code)
        return redirect('/')
    return render_template('add.html', form=form_)


@app.route("/delete/<int:_id_>", methods=["POST", "GET"])
def delete_cafe(_id_):
    del_request__ = requests.post(
        url=f"https://cafe-yuk2.onrender.com/delete-report/{int(_id_)}?secret_key=qwertyuiopasdfghjkl")
    print(del_request__.text)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

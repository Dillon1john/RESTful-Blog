from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime

ckeditor = CKEditor()

def create_app():
    app = Flask(__name__)
    ckeditor.init_app(app)
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    return app


app = create_app()

Bootstrap(app)



##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    ##CONFIGURE TABLE
    class BlogPost(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        subtitle = db.Column(db.String(250), nullable=False)
        date = db.Column(db.String(250), nullable=False)
        body = db.Column(db.Text, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        img_url = db.Column(db.String(250), nullable=False)


    ##WTForm
    class CreatePostForm(FlaskForm):
        title = StringField("Blog Post Title", validators=[DataRequired()])
        subtitle = StringField("Subtitle", validators=[DataRequired()])
        author = StringField("Your Name", validators=[DataRequired()])
        img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
        body = CKEditorField("Blog Content", validators=[DataRequired()])
        submit = SubmitField("Submit Post")


    ##RENDER HOME PAGE USING DB
    @app.route('/')
    def get_all_posts():
        posts = BlogPost.query.all()
        return render_template("index.html", all_posts=posts)

    @app.route('/delete/<int:post_id>')
    def delete_post(post_id):
        requested_post = BlogPost.query.get(post_id)
        db.session.delete(requested_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))

    ##RENDER POST USING DB
    @app.route("/post/<int:post_id>")
    def show_post(post_id):
        requested_post = BlogPost.query.get(post_id)
        return render_template("post.html", post=requested_post)


    @app.route("/edit/<int:post_id>", methods=['GET','POST'])
    def edit_post(post_id):
        requested_post = BlogPost.query.get(post_id)
        form = CreatePostForm()
        if form.is_submitted():
            requested_post.title = form.title.data
            requested_post.subtitle = form.subtitle.data
            requested_post.author = form.author.data
            requested_post.img_url = form.img_url.data
            requested_post.body = form.body.data
            # requested_post.date = datetime.date.today().strftime("%B %d, %Y")
            return redirect(url_for('get_all_posts'))

        return render_template('make-post.html', word='Edit', form=form)

    @app.route("/new-post", methods=['GET', 'POST'])
    def create_post():
        form = CreatePostForm()
        if form.is_submitted():
            new_post = BlogPost(title=form.title.data,
                                subtitle=form.subtitle.data,
                                author=form.author.data,
                                img_url=form.img_url.data,
                                body=form.body.data,
                                date=datetime.date.today().strftime("%B %d, %Y")
                                )

            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('get_all_posts'))

        return render_template('make-post.html', form=form, word='New')


    @app.route("/about")
    def about():
        return render_template("about.html")


    @app.route("/contact")
    def contact():
        return render_template("contact.html")


    if __name__ == "__main__":
        app.run(debug=True)

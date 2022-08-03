from flask import Blueprint
import datetime, json
from email.generator import DecodedGenerator
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    get_flashed_messages,
    flash,
)
from src.forms import UserLoginForm
from src.forms import UserCreateAccountForm
from .. import db
from src.forms import RegistrationForm, ViewUserProfileForm, CreatePostForm
from src.model.schemas import Attributes, Team, Post, Bookmarks
from src.controller.user import User
from src.utility import schedule
from src.utility.email import ManageEmailTemplate
from src import login_manager, mail
from flask_login import current_user, login_required, login_user, logout_user
from src.utility import blogsview


blog_bp = Blueprint('blog', __name__, template_folder='templates')

@blog_bp.route("/blog/homepage/", methods=["POST", "GET"])
@login_required
def blog_page():
    content = CreatePostForm()
    # blogs that current_user created.
    user_blogs = (
        Post.query.filter_by(creator_id=current_user.id)
        .order_by(Post.date_created)
        .limit(2)
    )
    
    # all blogs
    all_blogs = blogsview.blog()

    # all blogs where that current_user has bookmarked.
    bookmarks = Bookmarks.query.all()

    if request.method == "POST":
        # data received when a user clicks on the heart button to signify bookmarks.
        like = request.form.get(
            "post_liked"
        )  # value = 1; used to increase likes count/ bookmarks
        # the current post clicked or bookmarked by user.
        postid = request.form.get("current_post_id")
       
        if like == "1":
            # ? retrieve all occurances of the current post from the database.
            current_post = Post.query.filter_by(id=int(postid)).first()

            # ? CHECK if current_user and currentpost has been bookedmarked
            # ? Return the bookmarked posts where post_id equals current_post id. The post user clicked.
            book_mark = Bookmarks.query.filter_by(post_id=current_post.id).all()

            #! VALIDATION
            # ? Before taking any actions such as updating the like count;
            # ?We need to verify that the current_post has been bookmarked or liked the current_user.
            for item in book_mark:
                if item.liker_id == current_user.id:
                    flash("You already liked this post", category="info animate__animated animate__flash")
                    return redirect(url_for("blog.blog_page"))

            else:
                this_post = Post.query.filter_by(id=int(postid)).first()
                post_bookmark = Bookmarks(
                    post_id=this_post.id, liker_id=current_user.id
                )
                db.session.add(post_bookmark)
                db.session.commit()
                this_post.update_likes(like)
                flash("You have liked this post", category="success")
                return redirect(url_for("blog_page"))
            
        else:
            create_post = Post(
                post_title=content.post_title.data,
                post_content=content.post_content.data,
                date_created=datetime.datetime.today(),
                creator_id=current_user.id,
            )
            db.session.add(create_post)
            db.session.commit()
            flash("Your post has been uploaded !!! ")
            return redirect(url_for("blog_page"))

    # for get request
    elif request.method == "GET":
        return render_template(
            "blog/blog-create-post.html",
            content=content,
            user_blogs=user_blogs,
            all_blogs=all_blogs,
            bookmarks=bookmarks,
        )
    else:
        flash("Sorry we have no idea what just happen", category="info")

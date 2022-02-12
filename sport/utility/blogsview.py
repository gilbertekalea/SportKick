from sport.models import *


def blog():
    # find all posts created by current_user
    blogs = Post.query.all()
    all_blogs = []
    # turning the query result into a dictionary, then assign creator name.
    for item in blogs:
        recent_blog = {}
        creator = User.query.filter_by(id=item.creator_id).first()
        recent_blog["id"] = item.id
        recent_blog["post_title"] = item.post_title
        recent_blog["date_created"] = item.date_created
        recent_blog["post_content"] = item.post_content
        recent_blog["creator_name"] = creator.first_name
        recent_blog["likes_count"] = item.likes_count
        all_blogs.append(recent_blog)
    return all_blogs

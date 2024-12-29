from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# 建立名為 'posts' 的 Blueprint 模組，處理文章相關功能
posts = Blueprint('posts', __name__)


# 建立新文章
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    # 初始化表單
    form = PostForm()
    # 驗證表單輸入
    if form.validate_on_submit():
        # 創建新文章並設置作者
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        # 重定向到首頁
        return redirect(url_for('main.home'))
    # 渲染新文章模板
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


# 查看特定文章
@posts.route("/post/<int:post_id>")
def post(post_id):
    # 根據文章 ID 查詢文章，如果不存在則返回 404
    post = Post.query.get_or_404(post_id)
    # 渲染文章模板
    return render_template('post.html', title=post.title, post=post)


# 更新文章
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # 查詢文章
    post = Post.query.get_or_404(post_id)
    # 確保當前用戶是文章作者
    if post.author != current_user:
        abort(403)
    # 初始化表單
    form = PostForm()
    # 驗證表單輸入
    if form.validate_on_submit():
        # 更新文章標題與內容
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        # 重定向到更新後的文章頁面
        return redirect(url_for('posts.post', post_id=post.id))
    # 預填表單內容
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    # 渲染更新文章模板
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


# 刪除文章
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    # 查詢文章
    post = Post.query.get_or_404(post_id)
    # 確保當前用戶是文章作者
    if post.author != current_user:
        abort(403)
    # 刪除文章並提交變更
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    # 重定向到首頁
    return redirect(url_for('main.home'))

from flask import render_template, request, Blueprint
from flaskblog.models import Post

# 建立名為 'main' 的 Blueprint 模組，處理主頁與關於頁面
main = Blueprint('main', __name__)


# 處理首頁與分頁功能
@main.route("/")
@main.route("/home")
def home():
    # 取得 URL 查詢參數中的頁碼，預設為第 1 頁，且類型為整數
    page = request.args.get('page', 1, type=int)
    # 根據文章發布日期降序排序，並每頁顯示 5 篇文章
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # 渲染首頁模板並傳遞文章資料
    return render_template('home.html', posts=posts)


# 處理關於頁面
@main.route("/about")
def about():
    # 渲染關於頁面模板並設定標題為 'About'
    return render_template('about.html', title='About')

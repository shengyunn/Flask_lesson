from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

# 用於加載用戶的函數
@login_manager.user_loader
def load_user(user_id):
    # 根據用戶 ID 查詢用戶
    return User.query.get(int(user_id))

# 定義 User 模型類
class User(db.Model, UserMixin):
    # 用戶 ID，主鍵
    id = db.Column(db.Integer, primary_key=True)
    # 用戶名，唯一且不能為空
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 電子郵件，唯一且不能為空
    email = db.Column(db.String(120), unique=True, nullable=False)
    # 頭像檔案名稱，預設為 'default.jpg'
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # 密碼雜湊值
    password = db.Column(db.String(60), nullable=False)
    # 與文章的關聯，建立反向關聯 'author'
    posts = db.relationship('Post', backref='author', lazy=True)

    # 產生密碼重設 Token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # 驗證密碼重設 Token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # 用於打印用戶資訊
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# 定義 Post 模型類
class Post(db.Model):
    # 文章 ID，主鍵
    id = db.Column(db.Integer, primary_key=True)
    # 文章標題，不能為空
    title = db.Column(db.String(100), nullable=False)
    # 發布日期，預設為當前時間
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # 文章內容，不能為空
    content = db.Column(db.Text, nullable=False)
    # 關聯的用戶 ID，外鍵
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 用於打印文章資訊
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

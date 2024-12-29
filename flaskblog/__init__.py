from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# 初始化數據庫
db = SQLAlchemy()
# 初始化密碼加密工具
bcrypt = Bcrypt()
# 初始化登入管理工具
login_manager = LoginManager()
# 設置未登入時的重定向視圖
login_manager.login_view = 'users.login'
# 設置登入提示訊息類別
login_manager.login_message_category = 'info'
# 初始化郵件工具
mail = Mail()

# 建立 Flask 應用實例

def create_app(config_class=Config):
    # 初始化應用
    app = Flask(__name__)
    # 載入配置設定
    app.config.from_object(Config)

    # 初始化擴展工具
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # 匯入 Blueprint 模組
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    # 註冊 Blueprint
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # 返回 Flask 應用實例
    return app

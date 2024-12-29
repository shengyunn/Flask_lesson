from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

# 使用者註冊表單
class RegistrationForm(FlaskForm):
    # 使用者名稱欄位，必填且長度限制為 2 到 20 個字符
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 電子郵件欄位，必填且必須符合電子郵件格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 密碼欄位，必填
    password = PasswordField('Password', validators=[DataRequired()])
    # 確認密碼欄位，必填且需與密碼欄位一致
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # 提交按鈕
    submit = SubmitField('Sign Up')

    # 驗證使用者名稱是否已存在
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # 驗證電子郵件是否已存在
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# 使用者登入表單
class LoginForm(FlaskForm):
    # 電子郵件欄位，必填且必須符合電子郵件格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 密碼欄位，必填
    password = PasswordField('Password', validators=[DataRequired()])
    # 記住我功能的勾選框
    remember = BooleanField('Remember Me')
    # 提交按鈕
    submit = SubmitField('Login')


# 更新帳戶資訊表單
class UpdateAccountForm(FlaskForm):
    # 使用者名稱欄位，必填且長度限制為 2 到 20 個字符
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    # 電子郵件欄位，必填且必須符合電子郵件格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 上傳圖片欄位，僅允許 jpg 和 png 格式
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # 提交按鈕
    submit = SubmitField('Update')

    # 驗證使用者名稱是否已存在
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    # 驗證電子郵件是否已存在
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


# 密碼重設請求表單
class RequestResetForm(FlaskForm):
    # 電子郵件欄位，必填且必須符合電子郵件格式
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # 提交按鈕
    submit = SubmitField('Request Password Reset')

    # 驗證電子郵件是否存在於資料庫
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


# 密碼重設表單
class ResetPasswordForm(FlaskForm):
    # 密碼欄位，必填
    password = PasswordField('Password', validators=[DataRequired()])
    # 確認密碼欄位，必填且需與密碼欄位一致
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # 提交按鈕
    submit = SubmitField('Reset Password')

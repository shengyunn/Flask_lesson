from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# 定義文章表單類別，用於文章創建與編輯
class PostForm(FlaskForm):
    # 標題欄位，要求輸入內容且不能為空
    title = StringField('Title', validators=[DataRequired()])
    # 內容欄位，要求輸入內容且不能為空
    content = TextAreaField('Content', validators=[DataRequired()])
    # 提交按鈕
    submit = SubmitField('Post')

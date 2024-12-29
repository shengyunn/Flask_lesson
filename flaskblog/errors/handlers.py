from flask import Blueprint, render_template

# 建立名為 'errors' 的 Blueprint 模組，處理錯誤頁面
errors = Blueprint('errors', __name__)


# 處理 404 錯誤 (找不到頁面)
@errors.app_errorhandler(404)
def error_404(error):
    # 返回自訂的 404 錯誤頁面及 HTTP 狀態碼 404
    return render_template('errors/404.html'), 404


# 處理 403 錯誤 (禁止訪問)
@errors.app_errorhandler(403)
def error_403(error):
    # 返回自訂的 403 錯誤頁面及 HTTP 狀態碼 403
    return render_template('errors/403.html'), 403


# 處理 500 錯誤 (伺服器內部錯誤)
@errors.app_errorhandler(500)
def error_500(error):
    # 返回自訂的 500 錯誤頁面及 HTTP 狀態碼 500
    return render_template('errors/500.html'), 500

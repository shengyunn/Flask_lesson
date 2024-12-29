from flaskblog import create_app

# 創建 Flask 應用實例
app = create_app()

# 啟動應用程式，啟用除錯模式
if __name__ == '__main__':
    app.run(debug=True)

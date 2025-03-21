from flask import Flask, request, url_for, redirect, render_template
import pymysql

app = Flask(__name__)

# 데이터베이스와 연결
conn = pymysql.connect(host='localhost', user='root', password='root', db='post_db', charset='utf8')
cursor = conn.cursor()

# 테이블 생성
cursor.execute("CREATE TABLE IF NOT EXISTS post(id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.route('/')
def home():
    cursor.execute("SELECT id, title FROM post")
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("INSERT INTO post(title, content) VALUES(%s, %s)", (title, content))
        conn.commit()
        return redirect(url_for('home'))
    return render_template('post.html')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    return render_template('view_post.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['POST', 'GET'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE post SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
        conn.commit()
        return redirect(url_for('view_post', post_id=post_id))
    cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    cursor.execute("DELETE FROM post WHERE id = %s", (post_id,))
    conn.commit()
    return redirect(url_for('home'))

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    cursor.execute("SELECT id, title FROM post WHERE title LIKE %s", ('%' + keyword + '%',))
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

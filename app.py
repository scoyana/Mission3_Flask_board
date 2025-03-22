from flask import Flask, request, url_for, redirect, render_template
import pymysql
from datetime import datetime

app = Flask(__name__)

now = datetime.now()

 # MySQL의 DATETIME 형식에 맞는 문자열로 변환
now_str = now.strftime('%Y-%m-%d %H:%M:%S') 


# 데이터베이스와 연결
conn = pymysql.connect(host='localhost', user='root', password='root', db='post_db', charset='utf8')
cursor = conn.cursor()

# 테이블 생성
cursor.execute("CREATE TABLE IF NOT EXISTS post(id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), content TEXT, created_at DATETIME, views INT DEFAULT 0)")


# 게시판 메인 화면
@app.route('/')
def home():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

# 게시판 작성
@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("INSERT INTO post(title, content, created_at) VALUES(%s, %s, %s)", (title, content, now_str))
        conn.commit()
        return redirect(url_for('home'))
    return render_template('post.html')

# 게시글 상세보기
@app.route('/post/<int:post_id>')
def view_post(post_id):
    # 조회수 증가
    cursor.execute("UPDATE post SET views = views + 1 WHERE id = %s", (post_id,))
    conn.commit()
    
    cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    return render_template('view_post.html', post=post)

# 게시글 수정
@app.route('/post/<int:post_id>/edit', methods=['POST', 'GET'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE post SET title = %s, content = %s, created_at = %s WHERE id = %s", (title, content, now_str,post_id))
        conn.commit()
        return redirect(url_for('view_post', post_id=post_id))
    cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    return render_template('edit_post.html', post=post)

# 게시글 삭제
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    cursor.execute("DELETE FROM post WHERE id = %s", (post_id,))
    conn.commit()
    return redirect(url_for('home'))

# 검색
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    search_option = request.form['search_option']
    if search_option == 'title':
        cursor.execute("SELECT id, title FROM post WHERE title LIKE %s", ('%' + keyword + '%',))
    elif search_option == 'content':
        cursor.execute("SELECT id, title FROM post WHERE content LIKE %s", ('%' + keyword + '%',))
    elif search_option == 'all':
        cursor.execute("SELECT id, title FROM post WHERE title LIKE %s OR content LIKE %s", ('%' + keyword + '%', '%' + keyword + '%'))
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

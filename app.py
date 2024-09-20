from flask import Flask, request

import dal

app = Flask(__name__)
with app.app_context():
    dal.init_db()


@app.route('/')
def index():
    posts = dal.get_posts()
    html_code = f'''
    <!DOCTYPE html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
        <title>Posts</title>
    </head>
    <body>
        <h1>Posts</h1>
        <h2>Create a post</h2>
        <form action="/create_post" method="post">
            <label for="writer">Writer:</label>
            <input type="text" id="writer" name="writer">
            <br>
            <label for="content">Content:</label>
            <input type="text" id="content" name="content">
            <br>
            <input type="submit" value="Submit">
        </form>
        <h2>All posts</h2>
        <ul>
    '''
    for post_id, writer, content, created_at in posts:
        html_code += f'''
            <li>
                <b>{writer}</b> - <div class="content">{content}</div>
            </li>
        '''
    html_code += '''
        </ul>
    </body>
    </html>
    '''
    return html_code


@app.route('/create_post', methods=['POST'])
def create_post():
    writer = request.form.get('writer', '')
    content = request.form.get('content', '')
    if writer and content:
        dal.create_post(writer, content)

    html_code = f'''
    <script>
        window.location.href = "/";
    </script>
    '''
    return html_code


if __name__ == '__main__':
    app.run()

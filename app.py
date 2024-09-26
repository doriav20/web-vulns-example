from flask import Flask, request

import dal

app = Flask(__name__)
with app.app_context():
    dal.init_db()


@app.route('/')
def index():
    posts = dal.get_posts()
    html_code = '''
    <!DOCTYPE html>
    <head>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
        <title>Posts</title>
    </head>
    <body>
        <h1>Posts</h1>
        <h2>Create a post</h2>
        <form action="/create_post" method="post">
            <label for="author">Author:</label>
            <input type="text" id="author" name="author">
            <br>
            <label for="content">Content:</label>
            <input type="text" id="content" name="content">
            <br>
            <input type="submit" value="Submit">
        </form>
        <h2>All posts</h2>
        <ul>
    '''
    for post_id, author, content, created_at in posts:
        html_code += '''
            <li>
                <b>''' + author + '''</b>
                <span class="created-at">(''' + created_at + ''')</span>
                <div class="content">''' + content + '''</div>
            </li>
        '''
    html_code += '''
        </ul>
        <div class="scroll-button-container">
            <button id="scrollToBottom" onclick="scrollToBottom()">&#8595;</button>
        </div>
        <script>
            function scrollToBottom() {
                window.scrollTo(0, document.body.scrollHeight);
            }
        </script>
    </body>
    </html>
    '''
    return html_code


@app.route('/create_post', methods=['POST'])
def create_post():
    author = request.form.get('author', '')
    content = request.form.get('content', '')
    if author and content:
        dal.create_post(author, content)

    html_code = f'''
    <script>
        window.location.href = "/";
    </script>
    '''
    return html_code


if __name__ == '__main__':
    app.run()

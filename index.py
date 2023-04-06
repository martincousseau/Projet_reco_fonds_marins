#coding:utf-8
import cgi

print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>Ma page web</title>
<head>
<body>
    <h1>Bonjour</h1>

    <form method="post" action="result.py" enctype="multipart/form-data">
            <p><input type="file" name="profile_pic" accept=".jpg">
            <input type="submit" value="Envoyer"></p>
    </form>

<body>
</html>
"""

print(html)
#coding:utf-8
import cgi


print("Content-type: text/html; charset=utf-8\n")
html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ProjetM1</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

    <style>
        .navbar{
            background-color: #38023B;
        }

        td {
            padding: 10px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #38023B;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        h1{
            font-weight: bold;
            color: #95D9DA;
        }

        body{
            background-color: #95D9DA;
        }

        .sub{
            background-color: #38023B;
            color: #95D9DA;
            font-weight: bold;
            width: 80px;
            height: 40px;
            border-radius: 8%;
        }

    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container-fluid">
            <table>
                <tr>
                    <td class="col-md-4 offset-md-1"><img src="image/isen.png"></td>
                    <td class="col-md-4 offset-md-2"><h1>Comprendre le milieu sous-marin</h1></td>             
                </tr>
            </table>
        </div>
    </nav>

      <br>

    <div class="container">
        <div class="row">
            <div class="col-sm-6">
                <h3>SUIM</h3>
                <br>
                <form method="post" action="suim.py" enctype="multipart/form-data">
                    <input type="file" name="profile_pic" accept="jpg">
                    <input type="submit" value="Predict" class="sub">
                </form>
                <br>
            </div>
        </div>

        <hr>

        <div class="row">
            <div class="col-sm-6">
                <h3>DeepLab</h3>
                <br>
                <form method="post" action="deeplab.py" enctype="multipart/form-data">
                    <input type="file" name="profile_pic" accept="jpg">
                    <input type="submit" value="Predict" class="sub">
                </form>
                <br>
            </div>
        </div>

        <hr>

        <div class="row">
            <div class="col-sm-6">
                <h3>PSPNet</h3>
                <br>
                <form method="post" action="pspnet.py" enctype="multipart/form-data">
                    <input type="file" name="profile_pic" accept="jpg">
                    <input type="submit" value="Predict" class="sub">
                </form>
                <br>
            </div>
        </div>

        <hr>

        <div class="row">
            <div class="col-sm-6">
                <h3>FCN8</h3>
                <br>
                <form method="post" action="fcn8.py" enctype="multipart/form-data">
                    <input type="file" name="profile_pic" accept="jpg">
                    <input type="submit" value="Predict" class="sub">
                </form>
                <br>
            </div>
        </div>

        <hr>

        <div class="row">
            <div class="col-sm-6">
                <h3>SegNet</h3>
                <br>
                <form method="post" action="segnet.py" enctype="multipart/form-data">
                    <input type="file" name="profile_pic" accept="jpg">
                    <input type="submit" value="Predict" class="sub">
                </form>
                <br>
            </div>
        </div>

        <hr>

        <div class="row">
            <div class="col-sm-6">
                <h3>UNet</h3>
                <br>
                <form method="post" action="unet.py" enctype="multipart/form-data">
                    <input type="file" name="profile_pic" accept="jpg">
                    <input type="submit" value="Predict" class="sub">
                </form>
                <br>
            </div>
        </div>
    </div>
</body>
</html>
"""

print(html)


#with open("index.html", "w") as file:
#   file.write(html)


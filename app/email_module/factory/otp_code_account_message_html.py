

def get_otp_code_message_html(name = 'Subscriber', otpcode=0, time_remaining=0):
   
    html = """\


<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        .header img {
            max-width: 200px;
            border-radius: 50%;
        }
        .content {
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            color: #888888;
        }
        button{
            padding: 2rem 4rem;
            border: none;
            font-size: 2.3rem;
        }
        .btn{
            background-color: #098edb;
            color: #ffffff;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
        }
        .btn:hover{
            background-color: #0a6ebd;
        }
        img{
            max-width: 60%;
            border-radius: 30rem;
        }
        .row{
            display: flex;
            justify-content: space-between;
        }
        .box-image{
            
            width: 45%;
        }
        .box-content{
            width: 100%;
        }
        .box-content div{
            justify-content: center;
            text-align: center;
            margin-top: 20px;
        }
        ul{
            list-style: none;
            padding: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://th.bing.com/th/id/OIG3.yf0p6Gj8f9kiKZKgGA6V?pid=ImgGn" 
            alt="Company Logo" >

            <h1 style="color: #098edb; font-size:2.5rem;">
                <strong>Verify Your Identity</strong>
            </h1>
        </div>
        <div class="content">
            <h3>Hi <span style="color: #098edb;">""" + name + """</span></h3>
            <p>Welcome to DTuning</p>
            
            <div class="row">
                
                <div class="box-content">
                    <p>
                        You probably have registered to receive a 2FA authentication code by email.
                    </p>
                    <p>Here's your verification code to complete the authentication.</p>
                    <div>
                        <button class="btn" >""" + otpcode + """</button>

                        <strong style="color: #098edb;">
                            <p style="margin-top: 20px;font-size:1.2rem;">""" + time_remaining + """</p>
                        </strong>

                    </div>
                </div>
            </div>
            <p>If you have any questions or need further assistance, please don't hesitate to contact us.</p>

            
        </div>
        <div class="team">
            <ul>
                <li style="text-decoration: underline;">Best Regards,</li>
                <li>Main Developer: <strong>Laurindo C.Benjamim</strong> </li>
                <li>Activity: <strong>Data Engineer & Software Developer</strong></li>
            </ul>
        </div>
        <div class="footer">            
            <p>&copy;2024 Laurindo C.Benjamim (<i>DTuning</i>). All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """
    return html


def get_simple_html(name = 'Subscriber'):
   
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
        .content {
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            color: #888888;
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
        ul{
            list-style: none;
            padding: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to our Webpage!</h1>
        </div>
        <div class="content">
            <h3>Dear <span style="color: #098edb;">Subscriber</span></h3>
            <p>We are excited to share with you the latest updates and news from our company.</p>
            
            <div class="row">
                <div class="box-image">
                    <img src="https://media.istockphoto.com/id/1253903573/vector/glowing-neon-line-musical-tuning-fork-for-tuning-musical-instruments-icon-isolated-on-black.jpg?s=612x612&w=0&k=20&c=OWksrvIypSsWsghC5uNXYLhuflLArq2qJC9oCKhqpTU=" 
            alt="Company Logo" >
                </div>
                <div class="box-content">
                    <p>
                        This is the last step in the process of creating your account.
                        Please click in the link below to verify your email address and complete your registration.
                    </p>
                    <p>
                        <p><a href="http://localhost:5000/users/activate/1">Activate my account</a>.</p>
                    </p>
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
            <p>&copy;2024 Laurindo C.Benjamim (<i>TuningD</i>). All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """
    return html
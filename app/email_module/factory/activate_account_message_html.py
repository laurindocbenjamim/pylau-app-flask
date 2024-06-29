
from flask import request, url_for
from datetime import datetime, timedelta

def get_activate_account_message_html(name = 'Subscriber', user_token='', time_remaining=''):
    base_url = request.url_root + 'auth/user/activate/account/' + str(user_token)

    created_date = datetime.now()#user['created_date']
    created_date = datetime.strftime(created_date,'%Y-%m-%d %H:%M:%S')            
    date_obj = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
    date_created_int = int(date_obj.timestamp())
            
    date_now_int = int(datetime.now().timestamp())
    
            
    #date_obj = datetime.strptime(str(created_date), '%a, %d %b %Y %H:%M:%S %Z')
            

    expiration_date = date_obj + timedelta(days=5)

    #time_remaining = expiration_date - datetime.now()
            #time_remaining_int = int(datetime.strptime(str(time_remaining), '%Y-%m-%d %H:%M:%S').timestamp())
    #total_seconds = int(time_remaining.total_seconds())
    #total_minutes = total_seconds // 60
    #total_hours = total_minutes // 60
    #time_left_days = total_hours // 24
    
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
                        <h3>Dear <span style="color: #098edb;">"""+name+"""</span></h3>
                        <p>We are excited to share with you the latest updates and news from our company.</p>
                        
                        <div class="row">
                            <div class="box-image">
                                <img src="https://th.bing.com/th/id/OIG3.yf0p6Gj8f9kiKZKgGA6V?pid=ImgGn" 
                        alt="Company Logo" >
                            </div>
                            <div class="box-content">
                                <p>
                                    This is the last step in the process of creating your account.
                                    Please click in the link below to activate your account.
                                </p>
                                <p>
                                    <p><a class="btn" style="font-size: 1.7rem;" href='""" +base_url+ """'>Activate my account</a>.</p>
                                    <strong style="color: #098edb;">
                                        <p style="margin-top: 20px;font-size:1.2rem;">""" + time_remaining + """</p>
                                    </strong>
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
                        <p>&copy;2024 Laurindo C.Benjamim (<i>DTuning</i>). All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
        """
    return html

# utils.py
from django.core.mail import EmailMessage
import base64
import os
from notify_app.settings import EMAIL_HOST_USER, BASE_DIR
EMAIL_TEMPLATE = '''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f9f9fc;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .email-container {{
            max-width: 600px;
            margin: 30px auto;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            display: flex;
                flex-direction: row;
                flex-wrap: nowrap;
                align-content: center;
                justify-content: center;
                align-items: center;
            background-color: #191a1af1;
            color: white;
            text-align: center;
            padding: 20px;
            height: 50px;
            position: relative;
        }}
        .header svg {{
            background: white;
            border-radius: 127px;
            width: 60px;
            height: auto;
            position: relative;
            left: -10%;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 30px;
            text-align: left;
        }}
        .content h2 {{
            color: #0c0c0cf1;
            margin-bottom: 10px;
            font-size: 20px;
        }}
        .content p {{
            font-size: 16px;
            color: #555;
            line-height: 1.6;
            margin: 15px 0;
        }}
        .button {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 25px;
            font-size: 16px;
            color: white;
            background-color: #191a1af1;
            text-decoration: none;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }}
        .button:hover {{
            background-color: #4f5050f1;
        }}
        .footer {{
            text-align: center;
            padding: 15px;
            background-color: #0d0d0e;
            color: #dbdbdb;
            font-size: 14px;
        }}
        .footer a {{
            color: #ffffff;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
      
            <!-- Replace this SVG with your actual logo -->
            
            <h1>Notification</h1>
        </div>
        <div class="content">
            <p>Email:- {}</p>
            <p>Transaction ID:- {}</p>
            <p>Image:- <a href="{}" target="_blank">Click Here</a></p>
        </div>
      
    </div>
</body>
</html>

'''



def send_email(email, image_url, transaction_id):
    """
    Send an email using Django's EmailMessage class.
    """
    # image_file = os.path.join(BASE_DIR,'images', str(image_url))
    # with open(image_file, "rb") as image_file:
    #     base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    # with open('text.txt', "w") as file:
    #     file.write(EMAIL_TEMPLATE.format(email, transaction_id,image_url,approve_url))
        
    email = EmailMessage(
        subject="Notification",
        body=EMAIL_TEMPLATE.format(email, transaction_id,image_url),
        from_email=EMAIL_HOST_USER,  # Replace with your email
        to=['jashcontact750@gmail.com'],
    )
    email.content_subtype = "html"
    email.send()

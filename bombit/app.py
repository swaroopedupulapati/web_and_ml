import concurrent.futures
import random
import time

from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask('bombit')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "swaroop qis"
app.config['MAIL_PASSWORD'] = 'swaroopQis'


mail = Mail(app)

@app.route('/',methods=['GET'])
def bombit():
    print("Address is:", request.remote_addr)
    return render_template('bombit.html')

def send_emails(recipient):
    name = recipient[:recipient.index('@')]
    with app.app_context():
        otp = random.randint(000000,999999)

        message = Message('check',sender='YOUR MAIL',recipients=[recipient])
        message.body = f'{otp}\nyour are from |...| college right..?\nYour email is hacked {name}❌\nbe ready to face the consequences'
        mail.send(message)
        print(mail,'success')
    
@app.route('/send',methods=['POST'])
def send_email():
    if request.method == 'POST':
        email = request.form['email']
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
            s = [ex.submit(send_emails,email) for _ in range(20)]
        #print(s)
        end = time.time()
        return {'response' : f'executed in {end-start} seconds'}
    return {'error':'methods'}

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Lead, Customer
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meinefirma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():

    sort_by = request.args.get('sort_by', 'id')
    if sort_by not in ['id', 'last_name', 'status']:
        sort_by = 'id'

    if request.method == 'POST':
        if request.form['action'] == 'add_lead':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone = request.form['phone']
            email = request.form['email']
            status = request.form['status']

            lead = Lead(first_name=first_name, last_name=last_name, phone=phone, email=email, status=status)
            db.session.add(lead)
            db.session.commit()
        elif request.form['action'] == 'delete_lead':
            lead_id = request.form['lead_id']
            lead = Lead.query.get(lead_id)
            db.session.delete(lead)
            db.session.commit()
            return redirect('/')
    if sort_by == 'last_name':
        leads = Lead.query.order_by(Lead.last_name).all()
    elif sort_by == 'status':
        leads = Lead.query.order_by(Lead.status).all()
    else:
        leads = Lead.query.all()

    bk_link = url_for('bestandskunden')
    bk_link_text = 'Bestandskunden'
    return render_template('index.html', leads=leads, bk_link=bk_link, bk_link_text=bk_link_text)

@app.route('/delete_lead/<int:id>/<string:reason>', methods=['POST'])
def delete_lead(id, reason):
    lead = Lead.query.get_or_404(id)
    db.session.delete(lead)
    db.session.commit()

    # You can use the 'reason' variable to store or log the reason for deletion
    print("Deleted lead with ID:", id, "Reason:", reason)

    return redirect(url_for('index'))




@app.route('/add_lead', methods=['POST'])
def add_lead():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    email = request.form['email']
    status = request.form['status']
    status_options = ['1. Infogespräch fehlt noch',
                      '2. Infogespräch geführt, EB fehlt',
                      '3. Infogespräch geführt, warten auf SA Erlaubnis',
                      '4. SA kann geschalten werden',
                      '5. SA geschalten, warten auf PV',
                      '6. PV vorgestellt, warten auf Feedback',
                      '7. PV akzeptiert, warten auf Vertrag',
                      '8. Vertrag an Kunden gesendet',
                      '9. Warten auf Reisedaten',
                      '10. Warten auf Anreise',
                      '11. Anreise erfolgt']
    lead = Lead(first_name=first_name, last_name=last_name, phone=phone, email=email, status=status)
    db.session.add(lead)
    db.session.commit()

    return redirect(url_for('index'))

    
@app.route('/bestandskunden')
def bestandskunden():
    customers = Customer.query.all()
    return render_template('bestandskunden.html', bestandskunden=bestandskunden)


status_stages = [
        '1. Infogespräch fehlt noch',
        '2. Infogespräch geführt, EB fehlt',
        '3. Infogespräch geführt, warten auf SA Erlaubnis',
        '4. SA kann geschalten werden',
        '5. SA geschalten, warten auf PV',
        '6. PV vorgestellt, warten auf Feedback',
        '7. PV akzeptiert, warten auf Vertrag',
        '8. Vertrag an Kunden gesendet',
        '9. Warten auf Reisedaten',
        '10. Warten auf Anreise',
        '11. Anreise erfolgt'
]

@app.route('/change_status/<int:id>', methods=['POST'])
def change_status(id):
    lead = Lead.query.get_or_404(id)
    next_status = get_next_status(lead.status)
    if next_status:
        lead.status = next_status
        lead.last_changed = datetime.utcnow()
        db.session.commit()
        response = jsonify(success=True, message="Status updated successfully.")
    else:
        response = jsonify(success=False, message="Error changing the status. No next status found.")
    
    print("Lead ID:", id)
    print("Current Status:", lead.status)
    print("Next Status:", next_status)
    
    return response

def get_next_status(current_status):
    status_options = [
        '1. Infogespräch fehlt noch',
        '2. Infogespräch geführt, EB fehlt',
        '3. Infogespräch geführt, warten auf SA Erlaubnis',
        '4. SA kann geschalten werden',
        '5. SA geschalten, warten auf PV',
        '6. PV vorgestellt, warten auf Feedback',
        '7. PV akzeptiert, warten auf Vertrag',
        '8. Vertrag an Kunden gesendet',
        '9. Warten auf Reisedaten',
        '10. Warten auf Anreise',
        '11. Anreise erfolgt'
    ]
    try:
        current_index = status_options.index(current_status)
        if current_index < len(status_options) - 1:
            return status_options[current_index + 1]
        else:
            return None
    except ValueError:
        return None





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8080)

    

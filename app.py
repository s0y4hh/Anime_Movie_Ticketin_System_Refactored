from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from fpdf import FPDF
import os
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime_ticketing.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    receipts = db.relationship('Receipt', backref='user', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Snack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_title = db.Column(db.String(150), nullable=False)
    ticket_quantity = db.Column(db.Integer, nullable=False)
    snacks = db.Column(db.String(200), nullable=True)
    drinks = db.Column(db.String(200), nullable=True)
    total_price = db.Column(db.Float, nullable=False)
    seat = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    payment_status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Utility Functions
def validate_name(name):
    if not re.match('^[a-zA-Z ]+$', name):
        return False
    return True

def generate_pdf(receipt):
    pdf = FPDF()
    pdf.add_page()
    
    # Add a TTF font that supports the '₱' character
    pdf.add_font('DejaVu', '', os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf'), uni=True)
    pdf.set_font('DejaVu', '', 12)

    pdf.cell(200, 10, txt="Anime Movie Ticket Receipt", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Receipt ID: {receipt.id}", ln=True)
    pdf.cell(200, 10, txt=f"Name: {receipt.user.name}", ln=True)
    pdf.cell(200, 10, txt=f"Movie: {receipt.movie_title}", ln=True)
    pdf.cell(200, 10, txt=f"Tickets: {receipt.ticket_quantity}", ln=True)
    pdf.cell(200, 10, txt=f"Seat: {receipt.seat}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {receipt.date}", ln=True)
    pdf.cell(200, 10, txt=f"Time: {receipt.time}", ln=True)
    if receipt.snacks:
        pdf.cell(200, 10, txt=f"Snacks: {receipt.snacks}", ln=True)
    else:
        pdf.cell(200, 10, txt="Snacks: None selected", ln=True)
    if receipt.drinks:
        pdf.cell(200, 10, txt=f"Drinks: {receipt.drinks}", ln=True)
    else:
        pdf.cell(200, 10, txt="Drinks: None selected", ln=True)
    pdf.cell(200, 10, txt=f"Total Price: {receipt.total_price:.2f}₱", ln=True)
    pdf.cell(200, 10, txt=f"Date of Issue: {receipt.created_at.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Payment Status: {receipt.payment_status}", ln=True)

    pdf_file = f"receipt_{receipt.id}.pdf"
    pdf.output(pdf_file)
    return pdf_file


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy_ticket', methods=['GET', 'POST'])
def buy_ticket():
    if request.method == 'POST':
        name = request.form['name']
        if not validate_name(name):
            flash('Invalid name. Only letters and spaces are allowed.', 'danger')
            return redirect(url_for('buy_ticket'))

        user = User(name=name)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('select_movie', user_id=user.id))

    return render_template('buy_ticket.html')

@app.route('/select_movie/<int:user_id>', methods=['GET', 'POST'])
def select_movie(user_id):
    user = User.query.get_or_404(user_id)
    movies = Movie.query.all()
    snacks = Snack.query.all()
    drinks = Drink.query.all()

    if request.method == 'POST':
        movie_id = request.form['movie']
        ticket_quantity = int(request.form['quantity'])
        seat = request.form['seat']
        date = request.form['date']
        time = request.form['time']

        movie = Movie.query.get_or_404(movie_id)
        total_price = movie.price * ticket_quantity

        selected_snacks = request.form.getlist('snacks')
        selected_drinks = request.form.getlist('drinks')

        snacks_details = []
        drinks_details = []

        for snack_id in selected_snacks:
            snack = Snack.query.get(snack_id)
            snacks_details.append(f"{snack.name} (₱{snack.price:.2f})")
            total_price += snack.price

        for drink_id in selected_drinks:
            drink = Drink.query.get(drink_id)
            drinks_details.append(f"{drink.name} (₱{drink.price:.2f})")
            total_price += drink.price

        receipt = Receipt(
            user_id=user.id,
            movie_title=movie.title,
            ticket_quantity=ticket_quantity,
            seat=seat,
            date=date,
            time=time,
            snacks=', '.join(snacks_details),
            drinks=', '.join(drinks_details),
            total_price=total_price
        )
        db.session.add(receipt)
        db.session.commit()

        return redirect(url_for('receipt', receipt_id=receipt.id))

    return render_template('select_movie.html', user=user, movies=movies, snacks=snacks, drinks=drinks)

@app.route('/receipt/<int:receipt_id>', methods=['GET', 'POST'])
def receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)

    if request.method == 'POST':
        payment = float(request.form['payment'])
        if payment < receipt.total_price:
            flash('Payment amount must be greater than or equal to the total price.', 'danger')
            return redirect(url_for('receipt', receipt_id=receipt.id))

        receipt.payment_status = 'Paid'
        db.session.commit()
        flash('Payment successful! You can now download your receipt.', 'success')

        return redirect(url_for('receipt', receipt_id=receipt.id))

    return render_template('receipt.html', receipt=receipt)

@app.route('/download_receipt/<int:receipt_id>')
def download_receipt(receipt_id):
    receipt = Receipt.query.get_or_404(receipt_id)
    if receipt.payment_status != 'Paid':
        flash('Receipt can only be downloaded after payment is successful.', 'danger')
        return redirect(url_for('receipt', receipt_id=receipt.id))

    pdf_file = generate_pdf(receipt)
    return send_file(pdf_file, as_attachment=True)


if __name__ == '__main__':
    # Ensure database setup is within the application context
    with app.app_context():
        if not os.path.exists('anime_ticketing.db'):
            db.create_all()  # Create all tables
    app.run(debug=True)
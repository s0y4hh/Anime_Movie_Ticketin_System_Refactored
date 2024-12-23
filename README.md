# Anime Movie Ticketing System

This refactored project is a Flask-based web application that allows users to purchase anime movie tickets, along with optional snacks and drinks. Users can select their preferred movie, seats, viewing date, and time, and proceed to payment. A PDF receipt is generated upon successful payment.

---

## Features

1. **User-Friendly Interface**: Simple and responsive design using Bootstrap.
2. **Dynamic Movie Selection**: Displays a list of movies fetched from a database.
3. **Snack and Drink Options**: Users can select optional snacks and drinks.
4. **Seat, Date, and Time Selection**: Users specify their preferred seat, viewing date, and time.
5. **Payment System**: Ensures payment is greater than or equal to the total amount before proceeding.
6. **PDF Receipt Generation**: Receipts can only be downloaded after successful payment.
7. **Flash Messages**: Displays success and error messages for user interactions.
8. **Defensive Programming**: Input validation and error handling are implemented to ensure robustness.

---

## Technologies Used

- **Python**
- **Flask** (Web Framework)
- **SQLite** (Database)
- **Bootstrap** (Frontend Styling)
- **FPDF** (PDF Generation)

---

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/s0y4hh/Anime_Movie_Ticketing_System_Refactored.git
   cd Anime_Movie_Ticketing_System_Refactored
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Populate the database with initial data:
   ```bash
   python populate_db.py
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## How to Use

1. **Homepage**:
   - Start by clicking on "Buy Tickets." or "Get Started"

2. **User Information**:
   - Enter your name and proceed to the movie selection.

3. **Movie Selection**:
   - Choose a movie, seat, date, and time.
   - Optionally, select snacks and drinks.

4. **Payment**:
   - Enter the payment amount (greater than or equal to the total price).
   - Confirm the payment.

5. **Receipt**:
   - After successful payment, download the receipt as a PDF.

---

## Project Structure

```
.
├── app.py               # Main application file
├── populate_db.py       # Script to populate database with initial data
├── templates/           # HTML templates
│   ├── base.html        # Base template with flash messages
│   ├── index.html       # Homepage
│   ├── buy_ticket.html  # Ticket buying form
│   ├── select_movie.html# Movie, seat, date, and snack selection
│   └── receipt.html     # Payment and receipt download page
├── static/              # Static assets (CSS, JS, etc.)
├── anime_ticketing.db   # SQLite database file "This will automatically Create when you run the app.py"
└── requirements.txt     # Python dependencies
```

---

## Defensive Programming Features

- **Input Validation**:
  - Name field only accepts letters and spaces.
  - Seat, date, and time are mandatory inputs.
  - Payment amount is validated to ensure sufficiency.

- **Error Handling**:
  - Flash messages for invalid inputs and unsuccessful actions.
  - Restriction on receipt download until payment is completed.

---

## Future Enhancements

1. Add user authentication and account management.
2. Implement real-time seat availability.
3. Extend payment system to integrate with external payment gateways.

---

## License

This project is open-source and available under the MIT License.

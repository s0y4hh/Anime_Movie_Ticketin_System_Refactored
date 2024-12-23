from app import app, db, Movie, Snack, Drink

# Add sample movies
movies = [
    Movie(title="Jujutsu Kaisen 0: The Movie", genre="Action", price=240.0),
    Movie(title="Your Name", genre="Romance", price=200.0),
    Movie(title="Spirited Away", genre="Drama", price=300.0),
    Movie(title="My Hero Academia: Heroes Rising", genre="Action", price=500.0),
    Movie(title="Weathering with You", genre="Romance", price=200.0),
]

# Add sample snacks
snacks = [
    Snack(name="Popcorn", price=50.0),
    Snack(name="Cookies", price=65.0),
    Snack(name="Chocolates", price=45.0),
    Snack(name="Chips", price=35.0),
]

# Add sample drinks
drinks = [
    Drink(name="Coke", price=35.0),
    Drink(name="Apple Juice", price=45.0),
    Drink(name="Water", price=20.0),
    Drink(name="Tea", price=30.0),
]

# Populate the database inside the application context
with app.app_context():
    db.create_all()  # Ensure tables exist
    db.session.add_all(movies)
    db.session.add_all(snacks)
    db.session.add_all(drinks)
    db.session.commit()

print("Database populated successfully!")
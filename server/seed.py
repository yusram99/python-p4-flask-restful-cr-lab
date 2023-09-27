from app import app
from models import db, Plant

with app.app_context():
    db.create_all()

    # Delete existing data (optional)
    db.session.query(Plant).delete()

    # Create sample Plant objects
    aloe = Plant(
        name="Aloe",
        image="./images/aloe.jpg",
        price=11.50,
    )

    zz_plant = Plant(
        name="ZZ Plant",
        image="./images/zz-plant.jpg",
        price=25.98,
    )

    # Add the Plant objects to the session and commit the changes
    db.session.add_all([aloe, zz_plant])
    db.session.commit()

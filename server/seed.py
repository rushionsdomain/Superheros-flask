from random import choice as rc
from app import app
from models import db, Hero, Power, HeroPower

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        HeroPower.query.delete()
        Hero.query.delete()
        Power.query.delete()

        print("Seeding powers...")
        powers = [
            Power(name="super strength", description="Superhuman strength."),
            Power(name="flight", description="Ability to fly."),
            Power(name="super senses", description="Enhanced senses."),
            Power(name="elasticity", description="Stretchable body."),
        ]
        db.session.add_all(powers)

        print("Seeding heroes...")
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)

        print("Associating powers with heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = [HeroPower(hero=rc(heroes), power=rc(powers), strength=rc(strengths)) for _ in range(10)]
        db.session.add_all(hero_powers)

        db.session.commit()
        print("Done seeding!")

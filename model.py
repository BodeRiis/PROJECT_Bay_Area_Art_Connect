"""BayArt - Bay Area Art Connection Project: db.Model classes"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()

from flask import Flask

from random import randint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from faker import Faker

fake = Faker()


class User(UserMixin, db.Model):
    """User class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(50), unique=True)
    display_email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(30))
    is_artist = db.Column(db.Boolean, unique=False, default=False)
    last_active = db.Column(db.DateTime, nullable=True)
    hourly_rate = db.Column(db.Integer, nullable=True)
    show_unpaid = db.Column(db.Boolean, unique=False, default=False)
    link_to_website = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    daysweek = db.Column(db.String(7), default="ttttttt")
    paid_confirm = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, unique=False, default=False)
    img_route = db.Column(db.String(200), default="default_user_icon.png")
    veri_code = db.Column(db.String(50), default="A123456")
    img_port_one = db.Column(db.String(200), default="default_user_icon.png")
    img_port_two = db.Column(db.String(200), default="default_user_icon.png")
    img_port_three = db.Column(db.String(200), default="default_user_icon.png")

    def __repr__(self):
        """Provides the representaion of a User instance when printed"""

        return f"<User id={self.id} user_name={self.user_name}>"

    posts = db.relationship("Post", backref=db.backref("users"))

    tags = db.relationship("Tag", secondary="users_tags", backref="users")


class Post(db.Model):
    """Post class, to create a new post ("listing") on the website."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_title = db.Column(db.String(200))
    description = db.Column(db.String(1500))
    creation_date = db.Column(db.DateTime)
    gig_date_start = db.Column(db.DateTime)
    gig_date_end = db.Column(db.DateTime)
    ishourly = db.Column(db.Boolean, default=False)
    unpaid = db.Column(db.Boolean, default=True)
    pay = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, default=True)

    zipcode = db.Column(
        db.Integer, db.ForeignKey("zipcodes.valid_zipcode"), nullable=False
    )

    def __repr__(self):
        """Provides the representaion of a Post instance when printed"""

        return f"<Post post_id={self.post_id} post_title={self.post_title} user_id={self.user_id}>"

    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")

    zipcodes = db.relationship("Zipcode", backref=db.backref("posts"))


class Tag(db.Model):
    """Tag class, creates new tags to be used in posts & users."""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag_name = db.Column(db.String(50))

    def __repr__(self):
        """Provides the representaion of a Tag instance when printed"""

        return f"<Tag tag_id={self.tag_id} tag_name={self.tag_name}>"


class Unavailability(db.Model):
    """Takes a user id and dates objects for unavailable"""

    __tablename__ = "unavailability"

    un_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    start_range_date = db.Column(db.DateTime)
    end_range_date = db.Column(db.DateTime)

    def __repr__(self):
        """Provides the representaion of an Unavailability instance when printed"""

        return f"<Unvailabilty tag_id={self.user_id} tag_name={self.date_ranges}>"

    users = db.relationship("User", backref=db.backref("unavailabilty"))


class Zipcode(db.Model):
    """Contains a list of all valid zipcodes in the Bay Area."""

    __tablename__ = "zipcodes"

    valid_zipcode = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100))
    region = db.Column(db.String(100))

    def __repr__(self):
        """Provides the representaion of a Zipcode instance when printed"""

        return f"<Zipcode valid_zipcode={self.valid_zipcode} region={self.region}>"


posts_tags = db.Table(
    "posts_tags",
    db.metadata,
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.tag_id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.post_id")),
)

users_tags = db.Table(
    "users_tags",
    db.metadata,
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.tag_id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
)

#####################################################################
# Database Seed Functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///bayart"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


def seed_users():
    """Creates a series of fake posts. Must seed BEFORE posts."""

    # tagsls = Tag.query.all()

    # for i in range(1, 100):

    #     fname = fake.name()

    #     fpassword = generate_password_hash(
    #         "hello", method="pbkdf2:sha256", salt_length=8
    #     )

    #     fbio = fake.sentence() + " " + fake.text() + " " + fake.sentence()
    #     fhourly_rate = randint(16, 125)
    #     fartistnum = randint(0, 1)

    #     fphone_list = str(randint(1111111111, 9999999999))
    #     count = 0
    #     fphone = "("
    #     for num in fphone_list:
    #         if count == 3:
    #             fphone += ") "
    #             fphone += num
    #             count += 1
    #         elif count == 6:
    #             fphone += "-"
    #             fphone += num
    #             count += 1
    #         else:
    #             fphone += num
    #             count += 1

    #     if fartistnum == 0:
    #         fartist = False
    #     else:
    #         fartist = True

    #     if i % 2 == 0:
    #         daysweek = "ttttttt"
    #     elif i % 3 == 0:
    #         daysweek = "tffffft"
    #     else:
    #         daysweek = "fttttff"

    #     link_to_website = fake.url()

    #     verified = True

    #     img_route = "fakeuser" + str(randint(1, 34)) + ".jpg"

    #     display_email = fname[:3] + fname[-2:] + str(i) + "@gmail.com"
    #     femail = display_email.lower()
    #     flast_active = fake.date_between(start_date="-1y", end_date="today")
    #     fuser = User(
    #         user_name=fname,
    #         is_artist=fartist,
    #         password=fpassword,
    #         bio=fbio,
    #         hourly_rate=fhourly_rate,
    #         phone=fphone,
    #         email=femail,
    #         last_active=flast_active,
    #         display_email=display_email,
    #         img_route=img_route,
    #         verified=verified,
    #         daysweek=daysweek,
    #         link_to_website=link_to_website,
    #     )

    #     db.session.add(fuser)
    #     fuser.tags.append(tagsls[randint(0, (len(tagsls) - 1))])

    fpassword = generate_password_hash(
        "temppwforseedonly", method="pbkdf2:sha256", salt_length=8
    )

    buser = User(
        user_name="Bode Riis",
        password=fpassword,
        bio="Bode Riis. I created this site. Awesome!",
        email="riisbode@gmail.com",
        display_email="RiisBode@gmail.com",
        verified=True,
        link_to_website="www.BodeRiis.com",
    )

    db.session.add(buser)

    print("Commiting all new users.")
    db.session.commit()


def seed_posts():
#     """Creates a series of fake posts. Must seed AFTER zipcodes and users."""
#     tags = Tag.query.all()

#     for i in range(1, 80):
#         fuser_id = randint(1, 50)
    fpost_date = fake.date_between(start_date="-3y", end_date="today")
    is_pay = randint(0, 1)

    if is_pay == 0:
        fpay = 0
    else:
        fpay = randint(30, 2000)
#         fpone = fake.name()

    gig_date_start = fake.date_between(start_date="-1y", end_date="+1y")

    if (randint(0, 1)) == 1:
        gig_date_end = gig_date_start
    else:
        gig_date_end = fake.date_between(start_date="-1y", end_date="+1y")

    if fpay == 0:
        unpaid = True
    else:
        unpaid = False

    if (randint(0, 1)) == 1:
        ishourly = False
    else:
        ishourly = True

#         fpost_title = fake.sentence()
#         fdescription = (
#             fake.sentence()
#             + " "
#             + fake.text()
#             + " "
#             + fake.text()
#             + " "
#             + fake.sentence()
#             + " "
#             + fake.text()
#         )
#         fzipcodes = db.session.query(Zipcode.valid_zipcode).all()
#         fzipcode = fzipcodes[randint(1, 350)]
    fpost = Post(
        user_id=1,
        description="First Temp Post",
        zipcode=94608,
        post_title="First Temp Post",
        creation_date=fpost_date,
        pay=fpay,
        gig_date_end=gig_date_end,
        gig_date_start=gig_date_start,
        unpaid=unpaid,
        ishourly=ishourly,
    )

    db.session.add(fpost)

#         fpost.tags.append(tags[randint(0, (len(tags) - 1))])

    print("Commiting all new posts.")
    db.session.commit()


def seed_tags():
    """Seeds tags as listed below:"""
    
    tag_list = [
        "Photography",
        "Cinematography",
        "Video Editing",
        "Music",
        "Audio Recording",
        "Dance",
        "Acting",
        "Graphic Design",
        "Wedding",
        "Painting",
        "Sculpture",
        "Film Crew",
        "Drone Operator",
        "Choreographer",
        "MUA Makeup Artist",
        "Hairstyist",
        "Tattoo",
    ]

    for category in tag_list:
        tag_to_add = Tag(tag_name=category)
        db.session.add(tag_to_add)

    db.session.commit()


def seed_zipcodes():
    """Strips zipcodes from raw html txt file and adds to database.
    Must seed BEFORE posts."""
    file = open("non_server_files/raw_zipcodes.txt")
    text = file.read()
    file.close()
    words = text.split(">")
    shorter_list = []
    final_list = set()

    for word in words:
        try:
            to_add = word[0].isdigit()
        except:
            to_add = False
        if to_add:
            shorter_list.append(word[:5])

    for code in shorter_list:
        if code.isdigit():
            final_list.add(code)

    names_file = open("non_server_files/zip_code_database_placenames.csv")
    names_text = names_file.readlines()
    names_file.close()
    zip_dict = {}

    for names_line in names_text:
        names_line_split = names_line.split(",")
        zip_dict[names_line_split[0]] = names_line_split[3]

    zip_list = list(final_list)

    final_dict = {}

    for k, v in zip_dict.items():
        if k in zip_list:
            final_dict[k] = v

    for k, v in final_dict.items():
        nv = v.replace('"', "")
        new_zcode = Zipcode(valid_zipcode=k, location_name=nv)
        db.session.add(new_zcode)

    remote = Zipcode(valid_zipcode=00000, location_name="Remote")
    db.session.add(remote)

    db.session.commit()


def seed_all():
    db.create_all()
    seed_zipcodes()
    seed_tags()
    seed_users()
    # seed_posts()

    zips = Zipcode.query.all()

    san_francisco = {"San Francisco"}
    peninsula = {
        "Belmont",
        "Brisbane",
        "Burlingame",
        "El Granada",
        "Half Moon Bay",
        "La Honda",
        "Loma Mar",
        "Los Altos",
        "Daly City",
        "Menlo Park",
        "Atherton",
        "Portola Valley",
        "Millbrae",
        "Montara",
        "Moss Beach",
        "Mountain View",
        "Pacifica",
        "Pescadero",
        "Redwood City",
        "San Bruno",
        "San Carlos",
        "San Gregorio",
        "South San Francisco",
        "Sunnyvale",
        "Palo Alto",
        "Stanford",
        "San Mateo",
    }
    north_bay_and_northland = {
        "American Canyon",
        "Angwin",
        "Calistoga",
        "Fairfield",
        "Napa",
        "Oakville",
        "Pope Valley",
        "Deer Park",
        "Rio Vista",
        "Rutherford",
        "Saint Helena",
        "Suisun City",
        "Suisun City",
        "Vallejo",
        "Yountville",
        "San Rafael",
        "Greenbrae",
        "Belvedere Tiburon",
        "Bodega",
        "Bodega Bay",
        "Bolinas",
        "Corte Madera",
        "Rohnert Park",
        "Dillon Beach",
        "Fairfax",
        "Cotati",
        "Forest Knolls",
        "Inverness",
        "Lagunitas",
        "Larkspur",
        "Marshall",
        "Mill Valley",
        "Novato",
        "Nicasio",
        "Olema",
        "Penngrove",
        "Petaluma",
        "Point Reyes Station",
        "Ross",
        "San Anselmo",
        "San Geronimo",
        "San Quentin",
        "Sausalito",
        "Stinson Beach",
        "Tomales",
        "Valley Ford",
        "Woodacre",
        "Jenner",
        "The Sea Ranch",
        "Windsor",
        "Villa Grande",
        "Stewarts Point",
        "Sonoma",
        "Sebastopol",
        "Rio Nido",
        "Occidental",
        "Monte Rio",
        "Middletown",
        "Kenwood",
        "Healdsburg",
        "Guerneville",
        "Gualala",
        "Graton",
        "Glen Ellen",
        "Geyserville",
        "Fulton",
        "Forestville",
        "El Verano",
        "Duncans Mills",
        "Cloverdale",
        "Clearlake",
        "Cazadero",
        "Camp Meeker",
        "Boyes Hot Springs",
        "Annapolis",
        "Santa Rosa",
    }
    east_bay = {
        "Alameda",
        "Discovery Bay",
        "Danville",
        "Alamo",
        "Antioch",
        "Benicia",
        "Bethel Island",
        "Birds Landing",
        "Brentwood",
        "Byron",
        "Canyon",
        "Concord",
        "Pleasant Hill",
        "Crockett",
        "Diablo",
        "El Cerrito",
        "Fremont",
        "Hayward",
        "Castro Valley",
        "Hercules",
        "Knightsen",
        "Lafayette",
        "Livermore",
        "Martinez",
        "Moraga",
        "Newark",
        "Oakley",
        "Orinda",
        "Pinole",
        "Pittsburg",
        "Pleasanton",
        "Dublin",
        "Port Costa",
        "Moraga",
        "Rodeo",
        "San Leandro",
        "San Ramon",
        "San Lorenzo",
        "Sunol",
        "Union City",
        "Oakland",
        "Emeryville",
        "Berkeley",
        "Albany",
        "Richmond",
        "El Sobrante",
        "Richmond",
        "San Pablo",
        "Clayton",
        "Walnut Creek",
    }
    south_bay = {
        "Alviso",
        "Aptos",
        "Ben Lomond",
        "Boulder Creek",
        "Brookdale",
        "Campbell",
        "Capitola",
        "Castroville",
        "Coyote",
        "Cupertino",
        "Davenport",
        "Felton",
        "Freedom",
        "Gilroy",
        "Hollister",
        "Los Gatos",
        "Milpitas",
        "Morgan Hill",
        "Mount Hermon",
        "Paicines",
        "San Juan Bautista",
        "San Martin",
        "Santa Clara",
        "Santa Cruz",
        "Scotts Valley",
        "Saratoga",
        "Soquel",
        "Tres Pinos",
        "Watsonville",
        "San Jose",
        "Mount Hamilton",
        "Aromas",
    }
    sacramento_stockon = {
        "Stockton",
        "Acampo",
        "Travis Afb",
        "Clements",
        "Farmington",
        "French Camp",
        "Holt",
        "Linden",
        "Lockeford",
        "Lodi",
        "Valley Springs",
        "Victor",
        "Wallace",
        "Woodbridge",
        "Tracy",
        "Escalon",
        "Lathrop",
        "Manteca",
        "Modesto",
        "Oakdale",
        "Ripon",
        "Sacramento",
        "Winters",
        "Walnut Grove",
        "Thornton",
        "Pioneer",
        "Loomis",
        "Lincoln",
        "Galt",
        "Fair Oaks",
        "Elmira",
        "Dixon",
        "Davis",
        "Auburn",
        "Vernalis",
        "Riverbank",
        "Vacaville",
    }

    for zipco in zips:
        if zipco.location_name in san_francisco:
            zipco.region = "San Francisco"
        elif zipco.location_name in peninsula:
            zipco.region = "Peninsula"
        elif zipco.location_name in north_bay_and_northland:
            zipco.region = "North Bay and Northland"
        elif zipco.location_name in east_bay:
            zipco.region = "East Bay"
        elif zipco.location_name in south_bay:
            zipco.region = "South Bay"
        elif zipco.location_name in sacramento_stockon:
            zipco.region = "Sacramento and Stockton"
        else:
            zipco.region = "Remote"

    db.session.commit()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("Connected to the database!")
    seed_all()

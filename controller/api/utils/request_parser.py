from flask_restful import reqparse

create_sponsor_parser = reqparse.RequestParser()
create_sponsor_parser.add_argument("name", type = str)
create_sponsor_parser.add_argument("industry", type = str)
create_sponsor_parser.add_argument("budget", type = float)

create_influencer_parser = reqparse.RequestParser()
create_influencer_parser.add_argument("name", type = str)
create_influencer_parser.add_argument("category", type = str)
create_influencer_parser.add_argument("budget", type = float)


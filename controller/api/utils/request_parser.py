from flask_restful import reqparse

create_sponsor_parser = reqparse.RequestParser()
create_sponsor_parser.add_argument("name", type = str)
create_sponsor_parser.add_argument("industry", type = str)
create_sponsor_parser.add_argument("budget", type = float)

create_influencer_parser = reqparse.RequestParser()
create_influencer_parser.add_argument("name", type = str)
create_influencer_parser.add_argument("category", type = str)
create_influencer_parser.add_argument("budget", type = float)

create_campaign_parser = reqparse.RequestParser()
create_campaign_parser.add_argument("name", type = str)
create_campaign_parser.add_argument("description",type = str)
create_campaign_parser.add_argument("start_date",type = str)
create_campaign_parser.add_argument("end_date",type = str)
create_campaign_parser.add_argument("budget",type = float)
create_campaign_parser.add_argument("visibility",type = bool)
create_campaign_parser.add_argument("goals",type = str)

create_ad_request_parser = reqparse.RequestParser()
create_ad_request_parser.add_argument("campaign_id", type = int)
create_ad_request_parser.add_argument("influencer_id", type = int)
create_ad_request_parser.add_argument("messages", type = str)
create_ad_request_parser.add_argument("requirements", type = str)
create_ad_request_parser.add_argument("payment_amount", type = float)
create_ad_request_parser.add_argument("status", type = int)

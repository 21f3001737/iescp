from model.db import db, Admin, AdRequests, Campaigns, Influencers, Sponsors
from datetime import datetime


def add_dummy_data():
    add_dummy_admin()
    add_dummy_influencers()
    add_dummy_sponsors()
    add_dummy_campaigns()
    add_dummy_ad_requests()

def add_dummy_admin():
    admins = [
        Admin(username="admin1", password="1234"),
        Admin(username="admin2", password="1234")
    ]

    for admin in admins:
        real = Admin.query.filter(Admin.username == admin.username).first()
        if not real:
            db.session.add(admin)
            db.session.commit()

def add_dummy_influencers():
    influencers = [
        Influencers(name="Jane Doe", username= "jdoe123", password= "securepass123", category= "Fashion", niche="Sustainable Fashion", followers=1200,budget= 10000.50),
        Influencers(name="John Smith", username= "influencerJS", password= "strongpassword", category="Gaming", niche = "Competitive Gaming", followers=26000,budget=  25000.00),
        Influencers(name="Maria Garcia", username= "mariag_fitness", password= "fitlife2024",category= "Fitness", niche= "Home Workouts", followers=7900 ,budget=  7895.23), 
        Influencers(name="Aditya Roy", username= "tech_adi", password= "innovation1",category= "Technology", niche="Gadgets Review", followers=7000,budget=  15000.75),
        Influencers(name="Chloe Dupont", username= "makeupbychloe", password= "beautyguru2023",category= "Beauty", niche="Vegan Makeup", followers=880,budget=  8562.99),
    ]
        
    for influencer in influencers:
        real = Influencers.query.filter(Influencers.username == influencer.username).first()
        if not real:
            db.session.add(influencer)
            db.session.commit()

def add_dummy_sponsors():
    sponsors = [
        Sponsors(name="Acme Corp", username= "acme_sponsors", password= "secure_sponsor", industry="Tech",budget= 500000.00),
        Sponsors(name="Green Beauty", username= "greenbeauty2023", password= "ecofriendly123",industry= "Cosmetics",budget= 200000.75),
        Sponsors(name="FitLife Inc", username= "fitlife_strong", password= "activelifestyle",industry= "Fitness",budget= 125000.99),
        Sponsors(name="Global Games", username= "globalgames2024", password= "esportschamp",industry= "Gaming",budget= 300000.00),
        Sponsors(name="Melody Music", username= "melodymusic", password= "soundwaves2023",industry= "Entertainment",budget= 750000.50),
    ]    
    for sponsor in sponsors:
        real = Sponsors.query.filter(Sponsors.username == sponsor.username).first()
        if not real:
            db.session.add(sponsor)
            db.session.commit()

def add_dummy_campaigns():
    campaigns = [
        Campaigns(name= "New Gaming Tech Launch",sponsor_id = 1,description= "Promote the release of our latest cutting-edge gaming hardware",start_date=datetime.strptime("2024-08-01", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-08-31", '%Y-%m-%d').date(),budget=150000.00,visibility=True,goals="Increase brand awareness and pre-orders for new gaming products", niche= "Competitive Gaming, Gadget Reviews"),
        Campaigns(name= "Sponsor Major Esports Tournament",sponsor_id = 1,description= "Partner with a major esports tournament to showcase our brand and reach a large audience of gamers",start_date=datetime.strptime("2024-09-15", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-09-30", '%Y-%m-%d').date(),budget=200000.00,visibility=True,goals="Generate brand loyalty and positive associations with competitive gaming", niche="Competitive Gaming"),
        Campaigns(name= "Sustainable Beauty Influencer Collaboration",sponsor_id = 2,description="Partner with eco-conscious beauty influencers to promote our new line of organic makeup products",start_date=datetime.strptime("2024-07-25", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-08-25", '%Y-%m-%d').date(),budget=75000.00,visibility=True,goals="Increase brand awareness and sales of our sustainable beauty products", niche="Vegan Makeup, Sustainable Fashion"),
        Campaigns(name= "Eco-Friendly Packaging Initiative",sponsor_id = 2,description="Raise awareness about our commitment to sustainable packaging solutions through social media campaigns",start_date=datetime.strptime("2024-10-01", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-10-31", '%Y-%m-%d').date(),budget=50000.00,visibility=True,goals="Educate consumers about our eco-friendly practices and build brand trust", niche="Sustainable Fashion"),
        Campaigns(name= "National Fitness Challenge",sponsor_id = 3,description="Organize a nationwide fitness challenge with influencer partnerships and social media engagement",start_date=datetime.strptime("2024-09-01", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-10-31", '%Y-%m-%d').date(),budget=85000.00,visibility=True,goals="Increase brand awareness, promote our fitness products, and generate user-created content", niche="Home Workouts"),
        Campaigns(name= "Fitness App Launch Campaign",sponsor_id = 3,description="Generate excitement and downloads for our new mobile fitness app through influencer marketing and targeted advertising",start_date=datetime.strptime("2024-11-01", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-11-30", '%Y-%m-%d').date(),budget=40000.00,visibility=True,goals="Drive app downloads, user engagement, and subscriptions", niche="-"),
        Campaigns(name= "Pro Gamer Sponsorship Program",sponsor_id = 4,description="Sponsor professional gamers to wear our branded apparel and equipment during tournaments and streams",start_date=datetime.strptime("2024-08-10", '%Y-%m-%d').date(),end_date=datetime.strptime("2025-02-28", '%Y-%m-%d').date(),budget=100000.00,visibility=True,goals="Increase brand exposure within the gaming community and establish ourselves as a leading esports supporter", niche="Competitive Gaming"),
        Campaigns(name= "Develop Global Games E-sports League",sponsor_id = 4,description="Establish and host our own esports league featuring popular games and competitive play",start_date=datetime.strptime("2024-12-01", '%Y-%m-%d').date(),end_date=datetime.strptime("2025-05-31", '%Y-%m-%d').date(),budget=150000.00,visibility=True,goals="Generate excitement for esports and our brand, attract new audiences, and establish dominance in the competitive gaming landscape", niche="Competitive Gaming"),
        Campaigns(name= "Rising Star Talent Search",sponsor_id = 5,description="Host a nationwide talent search to discover and promote up-and-coming musicians",start_date=datetime.strptime("2024-08-01", '%Y-%m-%d').date(),end_date=datetime.strptime("2024-10-31", '%Y-%m-%d').date(),budget=200000.00,visibility=True,goals="Discover new musical talent, generate brand awareness among young audiences, and build excitement for the future of music",niche="AV Artist" ),
        Campaigns(name= "Exclusive Music Streaming Partnership",sponsor_id = 5,description="Partner with a major music streaming platform to offer exclusive content and early access to new releases",start_date=datetime.strptime("2024-11-15", '%Y-%m-%d').date(),end_date=datetime.strptime("2025-02-28", '%Y-%m-%d').date(),budget=350000.00,visibility=True,goals="Increase brand loyalty and user engagement with the streaming platform, drive subscriptions, and promote our commitment to supporting artists", niche="AV Artist"),
    ]

    for campaign in campaigns:
        real = Campaigns.query.filter(Campaigns.name == campaign.name).first()
        if not real:
            db.session.add(campaign)
            db.session.commit()

def add_dummy_ad_requests():
    ad_requests = [
    # Acme Corp - New Gaming Tech Launch Campaign (Campaign ID 1)
    AdRequests(campaign_id=1, influencer_id=2,  # Replace 3 with influencer ID (Technology)
               messages="Promote Acme Corp's latest cutting-edge gaming hardware through engaging content (videos, reviews, etc.) on your channels.",
               requirements="Target audience: Gamers interested in high-performance hardware. Content must be informative, engaging, and showcase the benefits of our new products.",
               payment_amount=25000.00, status=0),
    AdRequests(campaign_id=1, influencer_id=2,  # Replace 2 with influencer ID (Gaming)
               messages="Partner with Acme Corp to create a sponsored stream/video showcasing the new gaming hardware and gameplay experiences.",
               requirements="High-quality gameplay footage with commentary highlighting the features and performance of our products. Active engagement with viewers in the chat.",
               payment_amount=30000.00, status=0),

    # Acme Corp - Sponsor Major Esports Tournament Campaign (Campaign ID 1)
    AdRequests(campaign_id=1, influencer_id=4,  # Replace 1 with influencer with large social media following
               messages="Create social media content (posts, videos) promoting the Acme Corp-sponsored esports tournament and generate excitement among your followers.",
               requirements="Engaging content about the tournament with a clear call to action to watch or participate.",
               payment_amount=15000.00, status=0),
    AdRequests(campaign_id=1, influencer_id=2,  # Replace 2 with influencer ID (Gaming)
               messages="Become an official streamer/caster for the Acme Corp-sponsored esports tournament. Provide live commentary and analysis of the competition.",
               requirements="In-depth knowledge of the game and professional casting skills. Promote Acme Corp branding throughout the tournament stream.",
               payment_amount=40000.00, status=0),

    # Green Beauty - Sustainable Beauty Influencer Collaboration (Campaign ID 2)
    AdRequests(campaign_id=2, influencer_id=1,  # Replace 4 with influencer (Beauty)
               messages="Promote Green Beauty's new line of organic makeup products through engaging content (tutorials, reviews) on your channels.",
               requirements="Showcase the products and their benefits, targeting eco-conscious beauty enthusiasts. Content should be informative and visually appealing.",
               payment_amount=18000.00, status=0),
    AdRequests(campaign_id=2, influencer_id=5,  # Replace 1 with influencer with large social media following
               messages="Partner with Green Beauty to raise awareness about their commitment to sustainable packaging solutions through social media posts.",
               requirements="Create engaging content (photos, videos) highlighting Green Beauty's eco-friendly practices and encouraging followers to support sustainable brands.",
               payment_amount=12000.00, status=0),

    # FitLife Inc. - National Fitness Challenge (Campaign ID 3)
    AdRequests(campaign_id=3, influencer_id=3,  # Replace 2 with influencer (Fitness)
               messages="Participate in the FitLife Inc. National Fitness Challenge and document your journey on social media, inspiring others to join.",
               requirements="Create engaging content (videos, photos) showcasing your workouts and using FitLife Inc. products. Encourage followers to use a specific hashtag for the challenge.",
               payment_amount=22000.00, status=0),
    AdRequests(campaign_id=3, influencer_id=5,  # Replace 5 with influencer with large social media following
               messages="Promote the FitLife Inc. National Fitness Challenge on your social media channels and encourage participation.",
               requirements="Create engaging content (posts, stories) highlighting the benefits of the challenge and motivating followers to join the movement.",
               payment_amount=18000.00, status=0)
    ]

    for ad_request in ad_requests:
        real = AdRequests.query.filter(AdRequests.messages == ad_request.messages).first()
        if not real:
            db.session.add(ad_request)
            db.session.commit()
        

            
    

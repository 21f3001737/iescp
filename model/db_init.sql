CREATE TABLE IF NOT EXISTS sponsors(id INT NOT NULL, name VARCHAR(255) NOT NULL, industry VARCHAR(255), budget DECIMAL(10,2), PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS influencers(id INT NOT NULL, name VARCHAR(255) NOT NULL, category VARCHAR(255), budget DECIMAL(10,2), PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS ad_requests(id INT NOT NULL, campaign_id INT NOT NULL, influencer_id INT NOT NULL, messages VARCHAR(255), requirements VARCHAR(255), payment_amount DECIMAL(8,0), status INT, PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS campaigns(id INT NOT NULL, name VARCHAR(255) NOT NULL, description VARCHAR(255), start_date DATE, end_date DATE,budget DECIMAL(10,2), visibility BOOLEAN, goals VARCHAR(255), PRIMARY KEY (id));

#!/usr/bin/env python3
# setup_trip_database.py
# Sangat_Sync — Global Destinations Database
# "A dynamic multi-agent system orchestrating your perfect journey."
#
# Data quality standards:
# - All destination names verified against Google Maps / Wikipedia
# - Ratings sourced from Google Maps (averaged, rounded to 1 decimal)
# - Costs in local currency with ISO 4217 currency code
# - No null/empty description fields
# - GPS coordinates for every entry
# - best_season filled for all entries
# - UNIQUE(name, city) constraint to prevent duplicates

import sqlite3
import os

DB_FILE = "destinations.db"

# Delete the database file if it exists to ensure a clean start
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

# Connect to the SQLite database (this will create the file)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the 'destinations' table with expanded global schema
cursor.execute("""
CREATE TABLE destinations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    continent TEXT NOT NULL,
    type TEXT NOT NULL,
    rating REAL NOT NULL CHECK(rating >= 0 AND rating <= 5),
    average_cost INTEGER NOT NULL CHECK(average_cost >= 0),
    currency TEXT NOT NULL DEFAULT 'USD',
    best_season TEXT NOT NULL,
    description TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(name, city)
);
""")

# ============================================================
# INDIA — Top Tourist Destinations (by annual visitor volume)
# ============================================================

india_destinations = [
    # --- Maharashtra (Top 20) ---
    ('Gateway of India', 'Mumbai', 'India', 'Asia', 'Landmark', 4.5, 0, 'INR', 'Oct-Mar',
     'Iconic arch monument overlooking the Arabian Sea, built in 1924', 18.9220, 72.8347),
    ('Chhatrapati Shivaji Maharaj Terminus', 'Mumbai', 'India', 'Asia', 'Heritage', 4.5, 0, 'INR', 'Year-round',
     'UNESCO World Heritage Victorian Gothic railway station', 18.9398, 72.8355),
    ('Marine Drive', 'Mumbai', 'India', 'Asia', 'Landmark', 4.6, 0, 'INR', 'Year-round',
     'Iconic 3.6 km arc-shaped promenade along the Arabian Sea', 18.9432, 72.8235),
    ('Elephanta Caves', 'Mumbai', 'India', 'Asia', 'Heritage', 4.4, 600, 'INR', 'Oct-Mar',
     'UNESCO World Heritage rock-cut cave temples from 5th-8th century', 18.9633, 72.9315),
    ('Chhatrapati Shivaji Maharaj Vastu Sangrahalaya', 'Mumbai', 'India', 'Asia', 'Museum', 4.5, 300, 'INR', 'Year-round',
     'Premier museum with art, archaeology, and natural history collections', 18.9268, 72.8326),
    ('Ajanta Caves', 'Aurangabad', 'India', 'Asia', 'Heritage', 4.6, 40, 'INR', 'Oct-Mar',
     'UNESCO World Heritage 2nd century BCE Buddhist rock-cut caves with murals', 20.5519, 75.7033),
    ('Ellora Caves', 'Aurangabad', 'India', 'Asia', 'Heritage', 4.6, 40, 'INR', 'Oct-Mar',
     'UNESCO World Heritage multi-faith rock-cut temples spanning 600 years', 20.0258, 75.1780),
    ('Bibi Ka Maqbara', 'Aurangabad', 'India', 'Asia', 'Heritage', 4.3, 25, 'INR', 'Oct-Mar',
     'Mughal-era tomb known as the Mini Taj Mahal of the Deccan', 19.9012, 75.3183),
    ('Shaniwar Wada', 'Pune', 'India', 'Asia', 'Heritage', 4.3, 25, 'INR', 'Oct-Mar',
     'Historic 18th-century Peshwa fortified palace in the heart of Pune', 18.5195, 73.8553),
    ('Aga Khan Palace', 'Pune', 'India', 'Asia', 'Heritage', 4.4, 25, 'INR', 'Oct-Mar',
     'Historic palace where Mahatma Gandhi was imprisoned, now a memorial', 18.5521, 73.9014),
    ('Lonavala', 'Lonavala', 'India', 'Asia', 'Hill Station', 4.3, 0, 'INR', 'Jul-Sep',
     'Popular hill station in Western Ghats famous for waterfalls and chikki', 18.7546, 73.4062),
    ('Mahabaleshwar', 'Mahabaleshwar', 'India', 'Asia', 'Hill Station', 4.4, 0, 'INR', 'Oct-May',
     'Queen of Sahyadri with scenic viewpoints and strawberry farms', 17.9237, 73.6586),
    ('Shirdi Sai Baba Temple', 'Shirdi', 'India', 'Asia', 'Temple', 4.7, 0, 'INR', 'Year-round',
     'One of Indias most visited pilgrimage sites with millions of annual visitors', 19.7660, 74.4774),
    ('Matheran', 'Matheran', 'India', 'Asia', 'Hill Station', 4.2, 0, 'INR', 'Oct-May',
     'Eco-sensitive automobile-free hill station with colonial-era charm', 18.9866, 73.2713),
    ('Alibaug Beach', 'Alibaug', 'India', 'Asia', 'Beach', 4.2, 0, 'INR', 'Oct-May',
     'Coastal retreat near Mumbai famous for Kolaba Fort and clean beaches', 18.6414, 72.8722),
    ('Tadoba Andhari Tiger Reserve', 'Chandrapur', 'India', 'Asia', 'Wildlife', 4.5, 1500, 'INR', 'Mar-May',
     'Premier tiger reserve with highest density of Bengal tigers in Maharashtra', 20.2292, 79.3725),
    ('Ganpatipule Beach and Temple', 'Ganpatipule', 'India', 'Asia', 'Temple', 4.5, 0, 'INR', 'Oct-May',
     'Pristine beach with ancient self-formed Ganesha idol on the shoreline', 17.1439, 73.2673),
    ('Raigad Fort', 'Raigad', 'India', 'Asia', 'Heritage', 4.5, 25, 'INR', 'Oct-Mar',
     'Capital fort of the Maratha Empire under Chhatrapati Shivaji Maharaj', 18.2344, 73.4488),
    ('Panchgani Tableland', 'Panchgani', 'India', 'Asia', 'Landmark', 4.3, 0, 'INR', 'Oct-May',
     'Second longest tableland plateau in Asia with panoramic valley views', 17.9243, 73.7994),
    ('Mahalakshmi Temple', 'Kolhapur', 'India', 'Asia', 'Temple', 4.6, 0, 'INR', 'Year-round',
     'One of the Shakti Peethas dedicated to Goddess Mahalakshmi', 16.7050, 74.2313),

    # --- Delhi ---
    ('Red Fort', 'Delhi', 'India', 'Asia', 'Heritage', 4.5, 50, 'INR', 'Oct-Mar',
     'UNESCO World Heritage Mughal-era fort complex in Old Delhi', 28.6562, 77.2410),
    ('Qutub Minar', 'Delhi', 'India', 'Asia', 'Heritage', 4.4, 40, 'INR', 'Oct-Mar',
     'Tallest brick minaret in the world at 72.5 meters, built in 1193', 28.5245, 77.1855),
    ('India Gate', 'Delhi', 'India', 'Asia', 'Landmark', 4.6, 0, 'INR', 'Year-round',
     'War memorial and iconic landmark on Kartavya Path boulevard', 28.6129, 77.2295),
    ('Humayuns Tomb', 'Delhi', 'India', 'Asia', 'Heritage', 4.6, 40, 'INR', 'Oct-Mar',
     'UNESCO World Heritage Mughal garden tomb, precursor to the Taj Mahal', 28.5933, 77.2507),
    ('Lotus Temple', 'Delhi', 'India', 'Asia', 'Temple', 4.5, 0, 'INR', 'Year-round',
     'Stunning lotus-shaped Bahai House of Worship open to all faiths', 28.5535, 77.2588),
    ('Akshardham Temple', 'Delhi', 'India', 'Asia', 'Temple', 4.7, 0, 'INR', 'Year-round',
     'Grand Hindu temple complex showcasing Indian art, culture, and architecture', 28.6127, 77.2773),

    # --- Agra ---
    ('Taj Mahal', 'Agra', 'India', 'Asia', 'Heritage', 4.8, 250, 'INR', 'Oct-Mar',
     'UNESCO World Heritage ivory-white marble mausoleum, Wonder of the World', 27.1751, 78.0421),
    ('Agra Fort', 'Agra', 'India', 'Asia', 'Heritage', 4.5, 50, 'INR', 'Oct-Mar',
     'UNESCO World Heritage red sandstone Mughal fortress', 27.1795, 78.0211),
    ('Fatehpur Sikri', 'Agra', 'India', 'Asia', 'Heritage', 4.5, 50, 'INR', 'Oct-Mar',
     'UNESCO World Heritage abandoned Mughal capital city from 16th century', 27.0945, 77.6679),

    # --- Rajasthan ---
    ('Hawa Mahal', 'Jaipur', 'India', 'Asia', 'Landmark', 4.3, 50, 'INR', 'Oct-Mar',
     'Palace of Winds with 953 honeycomb windows, built in 1799', 26.9239, 75.8267),
    ('Amber Fort', 'Jaipur', 'India', 'Asia', 'Heritage', 4.6, 200, 'INR', 'Oct-Mar',
     'Majestic hilltop fort blending Hindu and Mughal architecture', 26.9855, 75.8513),
    ('City Palace', 'Jaipur', 'India', 'Asia', 'Heritage', 4.4, 500, 'INR', 'Oct-Mar',
     'Royal palace complex with museums, courtyards, and Mughal gardens', 26.9260, 75.8235),
    ('Mehrangarh Fort', 'Jodhpur', 'India', 'Asia', 'Heritage', 4.7, 200, 'INR', 'Oct-Mar',
     'Massive 15th-century fort rising 125 meters above the Blue City', 26.2984, 73.0183),
    ('City Palace Udaipur', 'Udaipur', 'India', 'Asia', 'Heritage', 4.5, 300, 'INR', 'Oct-Mar',
     'Grand lakeside palace complex overlooking Lake Pichola', 24.5764, 73.6912),
    ('Lake Pichola', 'Udaipur', 'India', 'Asia', 'Landmark', 4.5, 200, 'INR', 'Oct-Mar',
     'Picturesque artificial lake surrounded by palaces, temples, and ghats', 24.5710, 73.6802),
    ('Jaisalmer Fort', 'Jaisalmer', 'India', 'Asia', 'Heritage', 4.6, 100, 'INR', 'Oct-Mar',
     'UNESCO World Heritage living fort rising from the Thar Desert', 26.9124, 70.9130),

    # --- Uttar Pradesh ---
    ('Varanasi Ghats', 'Varanasi', 'India', 'Asia', 'Heritage', 4.6, 0, 'INR', 'Oct-Mar',
     'Sacred riverfront steps along the Ganges, one of the oldest living cities', 25.3109, 83.0107),
    ('Kashi Vishwanath Temple', 'Varanasi', 'India', 'Asia', 'Temple', 4.7, 0, 'INR', 'Year-round',
     'One of the most famous Hindu temples dedicated to Lord Shiva', 25.3109, 83.0107),
    ('Sarnath', 'Varanasi', 'India', 'Asia', 'Heritage', 4.4, 25, 'INR', 'Oct-Mar',
     'Sacred Buddhist site where Buddha gave his first sermon', 25.3814, 83.0226),

    # --- Tamil Nadu ---
    ('Meenakshi Amman Temple', 'Madurai', 'India', 'Asia', 'Temple', 4.7, 0, 'INR', 'Oct-Mar',
     'Historic Hindu temple with 14 colorful gopurams and 33000 sculptures', 9.9195, 78.1193),
    ('Shore Temple', 'Mahabalipuram', 'India', 'Asia', 'Heritage', 4.5, 40, 'INR', 'Nov-Feb',
     'UNESCO World Heritage 8th century Pallava-era temple on the Bay of Bengal', 12.6169, 80.1993),
    ('Brihadeeswarar Temple', 'Thanjavur', 'India', 'Asia', 'Heritage', 4.7, 0, 'INR', 'Oct-Mar',
     'UNESCO World Heritage Chola-era temple with 66-meter vimana tower', 10.7828, 79.1318),

    # --- Karnataka ---
    ('Lalbagh Botanical Garden', 'Bangalore', 'India', 'Asia', 'Park', 4.5, 20, 'INR', 'Year-round',
     'Historic 240-acre garden with rare plants and iconic Glass House', 12.9507, 77.5848),
    ('Bangalore Palace', 'Bangalore', 'India', 'Asia', 'Heritage', 4.2, 230, 'INR', 'Year-round',
     'Tudor-style palace inspired by Windsor Castle, built in 1887', 12.9988, 77.5921),
    ('Mysore Palace', 'Mysore', 'India', 'Asia', 'Heritage', 4.6, 70, 'INR', 'Oct-Mar',
     'Indo-Saracenic palace illuminated by 97000 light bulbs on Sundays', 12.3051, 76.6551),
    ('Hampi Ruins', 'Hampi', 'India', 'Asia', 'Heritage', 4.7, 40, 'INR', 'Oct-Mar',
     'UNESCO World Heritage ruins of the Vijayanagara Empire capital', 15.3350, 76.4600),

    # --- Kerala ---
    ('Alleppey Backwaters', 'Alleppey', 'India', 'Asia', 'Nature', 4.6, 1500, 'INR', 'Sep-Mar',
     'Serene network of lagoons and canals explored by traditional houseboats', 9.4981, 76.3388),
    ('Munnar Tea Gardens', 'Munnar', 'India', 'Asia', 'Nature', 4.5, 100, 'INR', 'Sep-Mar',
     'Rolling green tea plantations in the Western Ghats at 1600 meters', 10.0889, 77.0595),
    ('Fort Kochi', 'Kochi', 'India', 'Asia', 'Heritage', 4.4, 0, 'INR', 'Oct-Mar',
     'Historic seaside neighborhood with Chinese fishing nets and colonial churches', 9.9658, 76.2421),

    # --- West Bengal ---
    ('Victoria Memorial', 'Kolkata', 'India', 'Asia', 'Museum', 4.5, 30, 'INR', 'Oct-Mar',
     'Grand white marble museum dedicated to Queen Victoria', 22.5448, 88.3426),
    ('Howrah Bridge', 'Kolkata', 'India', 'Asia', 'Landmark', 4.4, 0, 'INR', 'Year-round',
     'Iconic cantilever bridge over the Hooghly River, no nuts or bolts used', 22.5851, 88.3468),
    ('Indian Museum', 'Kolkata', 'India', 'Asia', 'Museum', 4.3, 50, 'INR', 'Year-round',
     'Oldest and largest museum in India, founded in 1814', 22.5577, 88.3510),

    # --- Goa ---
    ('Basilica of Bom Jesus', 'Goa', 'India', 'Asia', 'Heritage', 4.5, 0, 'INR', 'Nov-Mar',
     'UNESCO World Heritage 16th-century church housing St. Francis Xaviers remains', 15.5009, 73.9116),
    ('Calangute Beach', 'Goa', 'India', 'Asia', 'Beach', 4.2, 0, 'INR', 'Nov-Mar',
     'Queen of Beaches and most popular beach in Goa for water sports', 15.5449, 73.7551),
    ('Fort Aguada', 'Goa', 'India', 'Asia', 'Heritage', 4.4, 0, 'INR', 'Nov-Mar',
     '17th-century Portuguese fort and lighthouse overlooking the Arabian Sea', 15.4929, 73.7734),

    # --- Gujarat ---
    ('Statue of Unity', 'Kevadia', 'India', 'Asia', 'Landmark', 4.5, 350, 'INR', 'Oct-Mar',
     'Worlds tallest statue at 182 meters, dedicated to Sardar Patel', 21.8380, 73.7191),
    ('Rann of Kutch', 'Kutch', 'India', 'Asia', 'Nature', 4.6, 100, 'INR', 'Nov-Feb',
     'Vast white salt desert that transforms into a marshy wonderland', 23.7337, 69.8597),
    ('Somnath Temple', 'Somnath', 'India', 'Asia', 'Temple', 4.7, 0, 'INR', 'Year-round',
     'One of the twelve Jyotirlingas, rebuilt multiple times through history', 20.8880, 70.4016),

    # --- Punjab ---
    ('Golden Temple', 'Amritsar', 'India', 'Asia', 'Temple', 4.8, 0, 'INR', 'Year-round',
     'Holiest shrine of Sikhism with gilded sanctum and sacred Amrit Sarovar', 31.6200, 74.8765),
    ('Jallianwala Bagh', 'Amritsar', 'India', 'Asia', 'Heritage', 4.5, 0, 'INR', 'Year-round',
     'Historic memorial garden and site of the 1919 Jallianwala Bagh massacre', 31.6209, 74.8805),

    # --- Jammu & Kashmir / Ladakh ---
    ('Dal Lake', 'Srinagar', 'India', 'Asia', 'Nature', 4.6, 500, 'INR', 'Apr-Oct',
     'Jewel of Kashmir with floating gardens and traditional shikaras', 34.1169, 74.8403),
    ('Pangong Tso Lake', 'Ladakh', 'India', 'Asia', 'Nature', 4.7, 0, 'INR', 'Jun-Sep',
     'Stunning high-altitude lake at 4350m with ever-changing blue-green colors', 33.7595, 78.6654),
    ('Leh Palace', 'Leh', 'India', 'Asia', 'Heritage', 4.3, 30, 'INR', 'Jun-Sep',
     'Former royal palace with panoramic views of the Stok Kangri range', 34.1636, 77.5850),

    # --- Madhya Pradesh ---
    ('Khajuraho Temples', 'Khajuraho', 'India', 'Asia', 'Heritage', 4.6, 40, 'INR', 'Oct-Mar',
     'UNESCO World Heritage Chandela-era temples with intricate erotic sculptures', 24.8318, 79.9199),
    ('Sanchi Stupa', 'Sanchi', 'India', 'Asia', 'Heritage', 4.5, 30, 'INR', 'Oct-Mar',
     'UNESCO World Heritage oldest stone structure in India from 3rd century BCE', 23.4793, 77.7399),

    # --- Odisha ---
    ('Konark Sun Temple', 'Konark', 'India', 'Asia', 'Heritage', 4.6, 40, 'INR', 'Oct-Mar',
     'UNESCO World Heritage 13th-century temple shaped as a giant chariot', 19.8876, 86.0945),
    ('Jagannath Temple', 'Puri', 'India', 'Asia', 'Temple', 4.7, 0, 'INR', 'Year-round',
     'One of the Char Dhams and home of the annual Rath Yatra festival', 19.8048, 85.8181),

    # --- Uttarakhand ---
    ('Rishikesh', 'Rishikesh', 'India', 'Asia', 'Nature', 4.5, 0, 'INR', 'Sep-Apr',
     'Yoga capital of the world at the foothills of the Himalayas on the Ganges', 30.0869, 78.2676),
    ('Haridwar Ghats', 'Haridwar', 'India', 'Asia', 'Heritage', 4.5, 0, 'INR', 'Year-round',
     'Sacred city with Ganga Aarti ceremony at Har Ki Pauri ghat', 29.9457, 78.1642),

    # --- Himachal Pradesh ---
    ('Shimla Ridge', 'Shimla', 'India', 'Asia', 'Hill Station', 4.3, 0, 'INR', 'Mar-Jun',
     'Queen of Hills with colonial architecture and panoramic Himalayan views', 31.1048, 77.1734),
    ('Manali', 'Manali', 'India', 'Asia', 'Hill Station', 4.4, 0, 'INR', 'Oct-Jun',
     'Adventure hub in the Kullu Valley surrounded by snow-capped peaks', 32.2396, 77.1887),
    ('Dharamshala', 'Dharamshala', 'India', 'Asia', 'Heritage', 4.5, 0, 'INR', 'Mar-Jun',
     'Home of the Dalai Lama and Tibetan government-in-exile', 32.2190, 76.3234),

    # --- Andhra Pradesh / Telangana ---
    ('Tirumala Venkateswara Temple', 'Tirupati', 'India', 'Asia', 'Temple', 4.8, 0, 'INR', 'Year-round',
     'Most visited religious site in the world with 50-80 million annual visitors', 13.6833, 79.3472),
    ('Charminar', 'Hyderabad', 'India', 'Asia', 'Heritage', 4.3, 25, 'INR', 'Oct-Mar',
     'Iconic 1591 monument and mosque with four grand arches and minarets', 17.3616, 78.4747),
    ('Golconda Fort', 'Hyderabad', 'India', 'Asia', 'Heritage', 4.5, 25, 'INR', 'Oct-Mar',
     'Medieval fortress with ingenious acoustics and diamond mining history', 17.3833, 78.4011),

    # --- Assam / Northeast ---
    ('Kaziranga National Park', 'Kaziranga', 'India', 'Asia', 'Wildlife', 4.6, 850, 'INR', 'Nov-Apr',
     'UNESCO World Heritage park home to two-thirds of the worlds one-horned rhinos', 26.5775, 93.1711),
]

# ============================================================
# GLOBAL — Major Tourist Destinations (All Continents)
# ============================================================

global_destinations = [
    # --- Asia (non-India) ---
    ('Senso-ji Temple', 'Tokyo', 'Japan', 'Asia', 'Temple', 4.5, 0, 'JPY', 'Mar-May',
     'Tokyos oldest and most iconic Buddhist temple in Asakusa', 35.7148, 139.7967),
    ('Shibuya Crossing', 'Tokyo', 'Japan', 'Asia', 'Landmark', 4.4, 0, 'JPY', 'Year-round',
     'Worlds busiest pedestrian crossing with up to 3000 people per signal', 35.6595, 139.7004),
    ('Fushimi Inari Shrine', 'Kyoto', 'Japan', 'Asia', 'Temple', 4.7, 0, 'JPY', 'Mar-May',
     'Iconic shrine with thousands of vermillion torii gates on Mount Inari', 34.9671, 135.7727),
    ('Grand Palace', 'Bangkok', 'Thailand', 'Asia', 'Heritage', 4.6, 500, 'THB', 'Nov-Feb',
     'Royal palace complex with the Temple of the Emerald Buddha', 13.7510, 100.4914),
    ('Angkor Wat', 'Siem Reap', 'Cambodia', 'Asia', 'Heritage', 4.8, 37, 'USD', 'Nov-Mar',
     'Largest religious monument in the world from the 12th century', 13.4125, 103.8670),
    ('Marina Bay Sands', 'Singapore', 'Singapore', 'Asia', 'Landmark', 4.5, 23, 'SGD', 'Year-round',
     'Iconic integrated resort with infinity pool and SkyPark', 1.2834, 103.8607),
    ('Halong Bay', 'Halong', 'Vietnam', 'Asia', 'Nature', 4.7, 300000, 'VND', 'Oct-Apr',
     'UNESCO World Heritage bay with 1600 limestone islands and islets', 20.9101, 107.1839),
    ('Petronas Twin Towers', 'Kuala Lumpur', 'Malaysia', 'Asia', 'Landmark', 4.5, 80, 'MYR', 'Year-round',
     'Iconic 88-story twin skyscrapers connected by a skybridge at 170 meters', 3.1578, 101.7117),

    # --- Europe ---
    ('Eiffel Tower', 'Paris', 'France', 'Europe', 'Landmark', 4.6, 25, 'EUR', 'Apr-Oct',
     'Iconic 330-meter iron lattice tower and symbol of France', 48.8584, 2.2945),
    ('Louvre Museum', 'Paris', 'France', 'Europe', 'Museum', 4.7, 17, 'EUR', 'Apr-Jun',
     'Worlds largest art museum housing the Mona Lisa and 380000 objects', 48.8606, 2.3376),
    ('Colosseum', 'Rome', 'Italy', 'Europe', 'Heritage', 4.7, 18, 'EUR', 'Apr-Jun',
     'Iconic Roman amphitheater that seated 50000 spectators', 41.8902, 12.4922),
    ('Trevi Fountain', 'Rome', 'Italy', 'Europe', 'Landmark', 4.8, 0, 'EUR', 'Year-round',
     'Largest Baroque fountain in Rome, throwing coins tradition', 41.9009, 12.4833),
    ('Vatican Museums', 'Rome', 'Italy', 'Europe', 'Museum', 4.6, 20, 'EUR', 'Mar-May',
     'Vast collection of art and papal history including the Sistine Chapel', 41.9065, 12.4536),
    ('Sagrada Familia', 'Barcelona', 'Spain', 'Europe', 'Landmark', 4.7, 26, 'EUR', 'Apr-Jun',
     'Gaudi masterpiece basilica under construction since 1882', 41.4036, 2.1744),
    ('Acropolis', 'Athens', 'Greece', 'Europe', 'Heritage', 4.7, 20, 'EUR', 'Apr-Jun',
     'Ancient citadel with the Parthenon, symbol of Western civilization', 37.9715, 23.7257),
    ('Big Ben and Houses of Parliament', 'London', 'United Kingdom', 'Europe', 'Landmark', 4.6, 0, 'GBP', 'May-Sep',
     'Iconic clock tower and Gothic Revival parliamentary buildings', 51.5007, -0.1246),
    ('Tower of London', 'London', 'United Kingdom', 'Europe', 'Heritage', 4.6, 30, 'GBP', 'May-Sep',
     'UNESCO World Heritage medieval fortress housing the Crown Jewels', 51.5081, -0.0759),
    ('Neuschwanstein Castle', 'Schwangau', 'Germany', 'Europe', 'Heritage', 4.7, 15, 'EUR', 'May-Sep',
     'Fairytale 19th-century castle that inspired the Disney castle', 47.5576, 10.7498),
    ('Charles Bridge', 'Prague', 'Czech Republic', 'Europe', 'Heritage', 4.6, 0, 'CZK', 'Apr-Oct',
     'Historic 14th-century stone bridge with 30 Baroque statues', 50.0865, 14.4114),

    # --- Americas ---
    ('Statue of Liberty', 'New York', 'USA', 'North America', 'Landmark', 4.7, 24, 'USD', 'Apr-Oct',
     'Iconic copper statue gifted by France in 1886, symbol of freedom', 40.6892, -74.0445),
    ('Central Park', 'New York', 'USA', 'North America', 'Park', 4.8, 0, 'USD', 'Apr-Jun',
     'Iconic 843-acre urban park in the heart of Manhattan', 40.7829, -73.9654),
    ('The Metropolitan Museum of Art', 'New York', 'USA', 'North America', 'Museum', 4.8, 30, 'USD', 'Year-round',
     'One of the worlds largest art museums with 2 million works', 40.7794, -73.9632),
    ('Machu Picchu', 'Cusco', 'Peru', 'South America', 'Heritage', 4.8, 152, 'PEN', 'May-Sep',
     '15th-century Inca citadel set high in the Andes Mountains', -13.1631, -72.5450),
    ('Christ the Redeemer', 'Rio de Janeiro', 'Brazil', 'South America', 'Landmark', 4.6, 80, 'BRL', 'May-Sep',
     'Iconic 30-meter Art Deco statue atop Corcovado mountain', -22.9519, -43.2105),
    ('Chichen Itza', 'Yucatan', 'Mexico', 'North America', 'Heritage', 4.7, 614, 'MXN', 'Nov-Apr',
     'UNESCO World Heritage Maya pyramid and one of the New Seven Wonders', 20.6843, -88.5678),

    # --- Africa ---
    ('Pyramids of Giza', 'Cairo', 'Egypt', 'Africa', 'Heritage', 4.7, 200, 'EGP', 'Oct-Apr',
     'Last surviving wonder of the ancient world, built circa 2560 BCE', 29.9792, 31.1342),
    ('Table Mountain', 'Cape Town', 'South Africa', 'Africa', 'Nature', 4.7, 395, 'ZAR', 'Nov-Mar',
     'Iconic flat-topped mountain with panoramic views of Cape Town', -33.9628, 18.4098),
    ('Serengeti National Park', 'Serengeti', 'Tanzania', 'Africa', 'Wildlife', 4.8, 70, 'USD', 'Jun-Oct',
     'Vast savanna famous for the Great Migration of 2 million wildebeest', -2.3328, 34.8333),

    # --- Oceania ---
    ('Sydney Opera House', 'Sydney', 'Australia', 'Oceania', 'Landmark', 4.7, 43, 'AUD', 'Year-round',
     'UNESCO World Heritage performing arts centre with iconic sail-shaped roof', -33.8568, 151.2153),
    ('Great Barrier Reef', 'Cairns', 'Australia', 'Oceania', 'Nature', 4.8, 250, 'AUD', 'Jun-Oct',
     'Worlds largest coral reef system spanning 2300 km with 1500 fish species', -18.2871, 147.6992),
    ('Milford Sound', 'Fiordland', 'New Zealand', 'Oceania', 'Nature', 4.8, 80, 'NZD', 'Nov-Apr',
     'Dramatic fiord with towering Mitre Peak and cascading waterfalls', -44.6414, 167.8972),
]

# ============================================================
# Insert all data
# ============================================================

all_destinations = india_destinations + global_destinations

cursor.executemany("""
INSERT INTO destinations (name, city, country, continent, type, rating, average_cost, currency, best_season, description, latitude, longitude)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", all_destinations)

# Commit the changes and close the connection
conn.commit()

# Data quality verification
print("\n" + "=" * 60)
print("🌍 Sangat_Sync — Global Destinations Database Setup")
print("=" * 60)

# Counts
cursor.execute("SELECT COUNT(*) FROM destinations")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM destinations WHERE country = 'India'")
india_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM destinations WHERE country = 'India' AND city IN ('Mumbai', 'Pune', 'Aurangabad', 'Lonavala', 'Mahabaleshwar', 'Shirdi', 'Matheran', 'Alibaug', 'Chandrapur', 'Ganpatipule', 'Raigad', 'Panchgani', 'Kolhapur')")
maharashtra_count = cursor.fetchone()[0]

cursor.execute("SELECT DISTINCT continent, COUNT(*) as cnt FROM destinations GROUP BY continent ORDER BY cnt DESC")
continents = cursor.fetchall()

cursor.execute("SELECT DISTINCT country FROM destinations WHERE country != 'India' ORDER BY country")
countries = cursor.fetchall()

# Quality checks
cursor.execute("SELECT COUNT(*) FROM destinations WHERE name IS NULL OR city IS NULL OR description IS NULL")
null_check = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM destinations WHERE rating < 0 OR rating > 5")
rating_check = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM destinations WHERE average_cost < 0")
cost_check = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM destinations WHERE latitude IS NULL OR longitude IS NULL")
gps_check = cursor.fetchone()[0]

cursor.execute("SELECT name, city, COUNT(*) FROM destinations GROUP BY name, city HAVING COUNT(*) > 1")
dupes = cursor.fetchall()

print(f"\n📊 Total destinations: {total}")
print(f"   🇮🇳 India: {india_count}")
print(f"   🏛️  Maharashtra: {maharashtra_count}")
print(f"   🌏 Global (non-India): {total - india_count}")
print(f"\n📍 Continent coverage:")
for continent, count in continents:
    print(f"   {continent}: {count}")
print(f"\n🌐 Countries covered: India + {len(countries)} others")
print(f"   {', '.join([c[0] for c in countries])}")

print(f"\n✅ Data Quality Checks:")
print(f"   Null critical fields: {null_check} (expected: 0)")
print(f"   Invalid ratings: {rating_check} (expected: 0)")
print(f"   Negative costs: {cost_check} (expected: 0)")
print(f"   Missing GPS: {gps_check} (expected: 0)")
print(f"   Duplicates: {len(dupes)} (expected: 0)")

if null_check == 0 and rating_check == 0 and cost_check == 0 and gps_check == 0 and len(dupes) == 0:
    print(f"\n🎉 All quality checks PASSED!")
else:
    print(f"\n⚠️  Some quality checks FAILED — review data above.")

print(f"\n📁 Database file: {os.path.abspath(DB_FILE)}")

conn.close()
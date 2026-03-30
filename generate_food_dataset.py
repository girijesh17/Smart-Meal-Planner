import pandas as pd
import random

# Tamil Nadu Cuisine Dataset
# Format: (Food Name, DietType, min_cal, max_cal, min_prot, max_prot, min_fat, max_fat, min_price, max_price)

food_data = {
    "Breakfast": [
        # Veg
        ("Idly (2 pcs) + Sambar + Chutney",    "Veg", 180, 280, 6, 12, 2, 8,   30, 70),
        ("Idly (4 pcs) + Sambar + Chutney",    "Veg", 320, 450, 10, 18, 3, 10,  50, 100),
        ("Plain Dosai + Chutney",              "Veg", 200, 320, 5, 10, 5, 14,  40, 80),
        ("Masala Dosai",                       "Veg", 280, 420, 8, 14, 8, 18,  60, 130),
        ("Ghee Dosai",                         "Veg", 320, 480, 6, 12, 14, 28, 70, 140),
        ("Onion Dosai",                        "Veg", 240, 380, 6, 12, 6, 16,  50, 110),
        ("Rava Dosai",                         "Veg", 250, 380, 5, 10, 6, 16,  60, 120),
        ("Set Dosai + Sambar",                 "Veg", 300, 460, 8, 14, 6, 14,  60, 120),
        ("Pongal + Sambar + Chutney",          "Veg", 300, 460, 8, 15, 8, 18,  50, 110),
        ("Poori + Kurma",                      "Veg", 400, 600, 8, 14, 18, 32, 60, 130),
        ("Chappatti + Kurma",                  "Veg", 350, 520, 10, 18, 8, 18,  60, 130),
        ("Parotta + Kurma",                    "Veg", 450, 650, 10, 18, 18, 32, 70, 150),
        ("Parotta + Veg Salna",                "Veg", 480, 700, 10, 18, 20, 36, 80, 160),
        ("Upma + Chutney",                     "Veg", 200, 320, 5, 10, 5, 14,  40, 90),
        ("Paal Pongal",                        "Veg", 320, 480, 8, 15, 10, 22, 60, 130),
        ("Puttu + Kadala Curry",               "Veg", 350, 520, 12, 20, 6, 16,  70, 150),
        ("Idiyappam + Coconut Milk",           "Veg", 280, 420, 5, 10, 4, 12,  60, 130),
        ("Ven Pongal",                         "Veg", 300, 450, 8, 15, 10, 22, 50, 110),
        ("Medu Vada + Sambar",                 "Veg", 250, 380, 7, 13, 10, 22, 50, 110),
        ("Kara Pongal + Chutney",              "Veg", 320, 480, 8, 15, 10, 20, 50, 110),
        ("Aappam + Stew",                      "Veg", 300, 450, 6, 12, 6, 16,  70, 150),
        ("Bread + Omelette",                   "Veg", 280, 420, 8, 14, 8, 20,  50, 110),  # Egg-free
        ("Keerai Dosai",                       "Veg", 220, 360, 6, 12, 5, 14,  50, 110),
        ("Thengai Paal Dosai",                 "Veg", 280, 430, 6, 12, 10, 22, 60, 130),
        ("Paniyaram + Chutney",                "Veg", 280, 420, 7, 13, 8, 18,  50, 110),
        ("Fresh Fruit Juice",                  "Veg", 80,  180,  1,  3,  0,  2,  40, 100),
        ("Mango Juice",                        "Veg", 120, 220,  1,  3,  0,  2,  50, 120),
        ("Sugarcane Juice",                    "Veg", 80,  150,  0,  2,  0,  1,  20, 60),
        ("Nannari Sherbet",                    "Veg", 80,  150,  0,  1,  0,  1,  30, 70),
        ("Filter Coffee",                      "Veg", 40,  120,  1,  3,  2,  6,  20, 60),
        ("Thaen Kaapi (Honey Coffee)",         "Veg", 60,  140,  1,  3,  2,  6,  40, 80),
        # Non-Veg
        ("Omelette + Bread",                   "Non-Veg", 280, 450, 18, 28, 14, 24, 60, 130),
        ("Masala Omelette + Parotta",          "Non-Veg", 450, 650, 22, 34, 20, 35, 90, 180),
        ("Egg Dosai",                          "Non-Veg", 300, 450, 18, 28, 10, 22, 70, 150),
        ("Egg Pongal",                         "Non-Veg", 350, 520, 18, 28, 12, 24, 70, 150),
        ("Keema Parotta",                      "Non-Veg", 550, 800, 30, 45, 22, 38, 120, 250),
        ("Chicken Kadai + Idly",               "Non-Veg", 420, 620, 30, 45, 14, 26, 120, 250),
    ],
    "Lunch": [
        # Veg
        ("Meals (Sambar, Rasam, Kootu, Rice, Papad, Pickle)", "Veg", 500, 750, 15, 25, 8, 18,  80, 180),
        ("Meals (Full Thali)",                "Veg", 700, 1000, 18, 30, 12, 24, 120, 250),
        ("Curd Rice + Pickle",                "Veg", 300, 450,  8, 15, 6, 14,  50, 120),
        ("Sambar Rice",                        "Veg", 350, 520, 12, 20, 6, 14,  60, 130),
        ("Rasam Rice",                         "Veg", 280, 420, 8, 15, 4, 10,  50, 110),
        ("Lemon Rice",                         "Veg", 320, 480, 6, 12, 8, 18,  60, 120),
        ("Tamarind Rice (Puliyodharai)",       "Veg", 320, 480, 6, 12, 8, 18,  60, 120),
        ("Coconut Rice",                       "Veg", 350, 520, 6, 12, 10, 22, 60, 130),
        ("Tomato Rice",                        "Veg", 320, 480, 6, 12, 8, 18,  50, 120),
        ("Variety Rice (Festival Special)",    "Veg", 380, 560, 8, 15, 10, 22, 80, 160),
        ("Parotta + Veg Salna",                "Veg", 500, 750, 10, 18, 22, 38, 80, 160),
        ("Chappatti + Dal Fry",               "Veg", 380, 560, 14, 22, 8, 18,  70, 150),
        ("Poriyal + Rice + Dal",               "Veg", 400, 600, 12, 20, 6, 14,  70, 140),
        ("Kottu Parotta (Veg)",               "Veg", 450, 680, 10, 18, 14, 28, 100, 200),
        ("Veg Briyani",                        "Veg", 450, 680, 10, 18, 10, 22, 100, 220),
        ("Peas Pulao + Raita",                 "Veg", 400, 600, 10, 18, 8, 18,  80, 180),
        # Non-Veg
        ("Chicken Biryani (Ambur Style)",      "Non-Veg", 600, 900, 35, 55, 18, 32, 150, 300),
        ("Chicken Biryani (Dindigul Style)",   "Non-Veg", 650, 950, 38, 58, 20, 36, 180, 360),
        ("Mutton Biryani",                     "Non-Veg", 700, 1000, 42, 62, 25, 45, 250, 500),
        ("Fish Biryani",                       "Non-Veg", 600, 880, 38, 58, 18, 32, 200, 400),
        ("Prawn Biryani",                      "Non-Veg", 620, 900, 40, 60, 18, 34, 250, 500),
        ("Egg Biryani",                        "Non-Veg", 500, 750, 22, 35, 15, 28, 120, 240),
        ("Chicken Meals (Full)",               "Non-Veg", 700, 1000, 40, 60, 20, 36, 150, 300),
        ("Mutton Meals (Full)",               "Non-Veg", 800, 1100, 45, 65, 28, 48, 200, 400),
        ("Fish Curry + Rice",                  "Non-Veg", 450, 680, 32, 50, 14, 26, 120, 260),
        ("Chettinad Chicken Curry + Rice",     "Non-Veg", 550, 800, 38, 58, 18, 34, 150, 300),
        ("Mutton Kuzhambu + Rice",             "Non-Veg", 600, 880, 42, 62, 22, 40, 200, 400),
        ("Parotta + Chicken Salna",            "Non-Veg", 600, 850, 32, 50, 22, 40, 120, 250),
        ("Parotta + Mutton Salna",            "Non-Veg", 700, 1000, 38, 58, 28, 50, 180, 360),
        ("Kottu Parotta (Chicken)",           "Non-Veg", 550, 800, 35, 55, 18, 34, 150, 300),
        ("Kottu Parotta (Mutton)",            "Non-Veg", 650, 950, 40, 60, 22, 40, 200, 380),
        ("Fish Fry + Rice",                   "Non-Veg", 500, 750, 35, 55, 16, 30, 150, 300),
        ("Crab Curry + Rice",                 "Non-Veg", 480, 720, 30, 50, 12, 24, 300, 600),
        ("Prawn Masala + Rice",               "Non-Veg", 480, 720, 35, 55, 14, 26, 250, 500),
        ("Squid Fry + Rice",                  "Non-Veg", 450, 680, 30, 50, 14, 26, 200, 400),
    ],
    "Dinner": [
        # Veg
        ("Idly + Sambar",                     "Veg", 200, 320, 7, 14, 2, 8,  40, 90),
        ("Plain Dosai + Chutney",             "Veg", 200, 320, 5, 10, 5, 14, 40, 80),
        ("Parotta + Veg Salna",               "Veg", 480, 700, 10, 18, 20, 36, 80, 160),
        ("Chappatti + Kurma",                 "Veg", 350, 520, 10, 18, 8, 18, 60, 130),
        ("Pongal + Chutney",                  "Veg", 300, 460, 8, 15, 8, 18, 50, 110),
        ("Curd Rice + Pickle",                "Veg", 300, 450, 8, 15, 6, 14, 50, 120),
        ("Meals (Light)",                     "Veg", 450, 680, 12, 20, 8, 16, 70, 150),
        ("Sambar Rice",                       "Veg", 350, 520, 12, 20, 6, 14, 60, 130),
        ("Idiyappam + Kurma",                 "Veg", 320, 480, 8, 15, 6, 16, 80, 170),
        ("Aappam + Veg Stew",                 "Veg", 320, 480, 7, 14, 6, 16, 80, 170),
        ("Kottu Parotta (Veg)",               "Veg", 450, 680, 10, 18, 14, 28, 100, 200),
        ("Pongal + Vada + Sambar",            "Veg", 400, 600, 12, 20, 12, 26, 80, 160),
        ("Pesarattu + Ginger Chutney",        "Veg", 280, 420, 10, 18, 5, 14, 60, 130),
        ("Tomato Rice",                       "Veg", 320, 480, 6, 12, 8, 18, 50, 120),
        # Non-Veg
        ("Chicken Biryani",                   "Non-Veg", 600, 900, 35, 55, 18, 32, 150, 300),
        ("Mutton Biryani",                    "Non-Veg", 700, 1000, 42, 62, 25, 45, 250, 500),
        ("Fish Biryani",                      "Non-Veg", 600, 880, 38, 58, 18, 32, 200, 400),
        ("Parotta + Chicken Salna",           "Non-Veg", 600, 850, 32, 50, 22, 40, 120, 250),
        ("Parotta + Mutton Salna",            "Non-Veg", 700, 1000, 38, 58, 28, 50, 180, 360),
        ("Kottu Parotta (Chicken)",           "Non-Veg", 550, 800, 35, 55, 18, 34, 150, 300),
        ("Idly + Chicken Kurma",              "Non-Veg", 400, 600, 28, 45, 12, 24, 120, 250),
        ("Dosai + Chicken Curry",             "Non-Veg", 450, 670, 28, 45, 14, 26, 120, 250),
        ("Fish Curry + Rice",                 "Non-Veg", 450, 680, 32, 50, 14, 26, 120, 260),
        ("Chettinad Chicken + Rice",          "Non-Veg", 550, 800, 38, 58, 18, 34, 150, 300),
        ("Prawn Masala + Rice",               "Non-Veg", 480, 720, 35, 55, 14, 26, 250, 500),
        ("Egg Curry + Rice",                  "Non-Veg", 420, 620, 22, 34, 14, 26, 100, 200),
    ],
    "Snacks": [
        # Veg
        ("Bonda + Chutney",                   "Veg", 200, 320,  5, 10, 10, 22, 20, 60),
        ("Bajji (Onion/Plantain)",            "Veg", 200, 350,  4,  9, 10, 22, 20, 70),
        ("Murukku",                           "Veg", 250, 400,  4,  8, 12, 24, 20, 60),
        ("Sundal (Kadala/Peas)",              "Veg", 150, 250,  8, 15,  3, 10, 20, 60),
        ("Poha (Aval) + Chutney",             "Veg", 200, 320,  5, 10,  5, 14, 30, 80),
        ("Vada + Sambar",                     "Veg", 250, 380,  7, 14, 10, 22, 40, 100),
        ("Pani Puri (TN Style)",              "Veg", 150, 280,  3,  7,  4, 12, 30, 80),
        ("Samosa",                            "Veg", 200, 350,  4,  8, 10, 22, 20, 60),
        ("Aloo Bonda",                        "Veg", 220, 360,  4,  8, 10, 22, 25, 65),
        ("Corn Chaat",                        "Veg", 180, 300,  4,  8,  3, 10, 40, 100),
        ("Kozhukattai",                       "Veg", 180, 300,  4,  8,  3, 10, 30, 80),
        ("Kadalai Mittai (Peanut Chikki)",    "Veg", 200, 320,  6, 12,  8, 18, 10, 40),
        ("Fresh Sugarcane Juice",             "Veg",  80, 150,  0,  2,  0,  1, 20, 60),
        ("Fresh Lemon Juice",                 "Veg",  40, 100,  0,  1,  0,  1, 20, 50),
        ("Tender Coconut Water",              "Veg",  45, 100,  1,  2,  0,  1, 30, 80),
        ("Rose Milk",                         "Veg", 180, 280,  5, 10,  4, 10, 30, 70),
        ("Jigarthanda",                       "Veg", 300, 450,  6, 12,  8, 18, 60, 140),
        ("Paneer Roll",                       "Veg", 380, 560, 16, 26, 12, 24, 80, 180),
        # Non-Veg
        ("Chicken 65",                        "Non-Veg", 350, 520, 28, 42, 16, 30, 100, 220),
        ("Chicken Lollipop",                  "Non-Veg", 300, 480, 22, 36, 14, 28, 120, 260),
        ("Egg Puff",                          "Non-Veg", 250, 400, 10, 18, 14, 26, 30, 80),
        ("Chicken Puff",                      "Non-Veg", 300, 450, 18, 30, 16, 30, 50, 120),
        ("Mutton Samosa",                     "Non-Veg", 280, 430, 14, 24, 14, 28, 30, 80),
        ("Prawn Bajji",                       "Non-Veg", 300, 450, 18, 30, 14, 28, 80, 180),
        ("Fish Bajji",                        "Non-Veg", 280, 430, 18, 30, 12, 24, 60, 140),
    ],
    "Fast Food": [
        # Veg
        ("Veg Burger",                        "Veg", 350, 550, 10, 18, 14, 26, 100, 220),
        ("Cheese Veg Burger",                 "Veg", 450, 680, 14, 22, 18, 34, 150, 300),
        ("Margherita Pizza",                  "Veg", 600, 900, 18, 28, 22, 38, 200, 500),
        ("Paneer Tikka Pizza",                "Veg", 700, 1000, 22, 35, 24, 42, 280, 600),
        ("French Fries",                      "Veg", 300, 500,  4,  8, 14, 28, 100, 200),
        ("Veg Momos",                         "Veg", 250, 400,  8, 14,  6, 14, 80, 180),
        ("Veg Noodles",                       "Veg", 380, 560,  8, 15, 10, 22, 100, 220),
        ("Veg Fried Rice",                    "Veg", 400, 600,  8, 15, 10, 22, 100, 220),
        ("Paneer Roll",                       "Veg", 400, 600, 18, 28, 14, 26, 120, 260),
        ("Masala Vada Pav",                   "Veg", 300, 450,  6, 12, 10, 22, 50, 120),
        # Non-Veg
        ("Chicken Burger",                    "Non-Veg", 450, 700, 28, 45, 14, 28, 130, 280),
        ("Chicken Zinger Burger",             "Non-Veg", 550, 800, 30, 48, 20, 38, 160, 340),
        ("Chicken Tikka Pizza",               "Non-Veg", 800, 1100, 32, 52, 28, 48, 320, 680),
        ("Chicken Momos",                     "Non-Veg", 320, 500, 22, 36, 10, 22, 120, 260),
        ("Chicken Noodles",                   "Non-Veg", 480, 720, 28, 45, 14, 26, 150, 320),
        ("Chicken Fried Rice",                "Non-Veg", 500, 750, 28, 44, 14, 28, 150, 320),
        ("Chicken Roll / Kathi Roll",         "Non-Veg", 480, 720, 30, 48, 14, 28, 130, 280),
        ("Fish and Chips",                    "Non-Veg", 550, 820, 28, 45, 22, 40, 220, 480),
        ("Egg Fried Rice",                    "Non-Veg", 450, 670, 20, 32, 12, 24, 120, 260),
        ("Mutton Seekh Roll",                 "Non-Veg", 550, 800, 32, 52, 18, 34, 180, 380),
    ],
}

data = []
for _ in range(2500):
    meal = random.choice(list(food_data.keys()))
    item = random.choice(food_data[meal])
    fname, diet, mn_c, mx_c, mn_p, mx_p, mn_f, mx_f, mn_pr, mx_pr = item
    data.append([
        fname, meal, diet,
        random.randint(mn_c, mx_c),
        random.randint(mn_p, mx_p),
        random.randint(mn_f, mx_f),
        random.randint(mn_pr, mx_pr),
    ])

df = pd.DataFrame(data, columns=["Food","MealType","DietType","Calories","Protein","Fat","Price"])
df.to_csv("food_dataset_v6.csv", index=False)
print(f"Tamil Nadu cuisine dataset saved → food_dataset_v6.csv")
print(f"  Records : {len(df)}")
print(f"  Unique dishes : {df['Food'].nunique()}")
print(df.groupby(["MealType","DietType"])["Food"].nunique().to_string())

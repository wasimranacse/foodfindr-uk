from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from apps.locations.models import Area, City, Country, Cuisine
from apps.menus.models import MenuCategory, MenuItem
from apps.offers.models import Offer
from apps.restaurants.models import Restaurant
from apps.restaurants.utils import calculate_trust_score
from apps.reviews.models import Review

User = get_user_model()


DEV_PASSWORD = "FoodFindrDev123!"


CITY_NAMES = [
    "London",
    "Manchester",
    "Birmingham",
    "Leeds",
    "Glasgow",
    "Edinburgh",
    "Cardiff",
    "Bristol",
    "Liverpool",
]

LONDON_AREAS = [
    ("Whitechapel", "E1", 51.5196, -0.0594),
    ("Aldgate", "EC3", 51.5143, -0.0755),
    ("Shoreditch", "E2", 51.5260, -0.0780),
    ("London Bridge", "SE1", 51.5055, -0.0877),
    ("Tower Bridge", "SE1", 51.5057, -0.0754),
    ("Canary Wharf", "E14", 51.5054, -0.0235),
    ("Soho", "W1", 51.5136, -0.1365),
    ("Camden", "NW1", 51.5390, -0.1426),
    ("Brixton", "SW9", 51.4613, -0.1156),
    ("Stratford", "E20", 51.5438, -0.0076),
    ("Westminster", "SW1", 51.4975, -0.1357),
]

CUISINES = [
    "Bengali",
    "Indian",
    "Pakistani",
    "Turkish",
    "Italian",
    "Thai",
    "Japanese",
    "Chinese",
    "British",
    "Vegan",
    "Dessert",
    "Coffee",
    "Middle Eastern",
    "African",
    "Caribbean",
]

RESTAURANTS = [
    ("Brick Lane Garden Kitchen", "Whitechapel", ["Bengali", "Indian"], 2, 5, 4.6, 42, 32, True, False, "Lunch saver: 15% off curries"),
    ("Aldgate Spice House", "Aldgate", ["Pakistani", "Indian"], 2, 4, 4.3, 31, 35, True, False, "Family biryani bundle"),
    ("Shoreditch Noodle Lab", "Shoreditch", ["Thai", "Chinese"], 2, 5, 4.5, 28, 24, False, False, "Student noodle bowl deal"),
    ("London Bridge Bento Works", "London Bridge", ["Japanese"], 3, 5, 4.7, 38, 22, False, False, "Lunch bento and drink"),
    ("Tower Mezze Room", "Tower Bridge", ["Middle Eastern", "Turkish"], 2, 4, 4.2, 19, 28, True, False, "Mezze sharer for two"),
    ("Canary Wharf Green Bowl", "Canary Wharf", ["Vegan"], 3, 5, 4.4, 24, 20, False, True, "Plant-powered lunch deal"),
    ("Soho Pasta Social", "Soho", ["Italian"], 3, 4, 4.1, 36, 26, False, False, "Student pasta night"),
    ("Camden Jerk Yard", "Camden", ["Caribbean"], 2, 3, 4.0, 22, 30, True, False, "Family grill box"),
    ("Brixton Pepper Pot", "Brixton", ["African", "Caribbean"], 2, 5, 4.8, 44, 34, True, False, "Weekend stew special"),
    ("Stratford Sushi Street", "Stratford", ["Japanese"], 3, 4, 4.2, 27, 25, False, False, "Roll combo lunch"),
    ("Westminster Roast & Roots", "Westminster", ["British"], 3, 5, 4.3, 33, 29, False, False, "Sunday family roast deal"),
    ("Whitechapel Chai & Bakes", "Whitechapel", ["Coffee", "Dessert"], 1, 4, 4.5, 18, 18, False, False, "Coffee and cake saver"),
    ("Aldgate Kebab Corner", "Aldgate", ["Turkish"], 1, 3, 3.8, 16, 21, True, False, "Late-night wrap deal"),
    ("Shoreditch Vegan Slice", "Shoreditch", ["Vegan", "Italian"], 2, 5, 4.6, 29, 23, False, True, "Two-slice student deal"),
    ("London Bridge Dumpling Studio", "London Bridge", ["Chinese"], 2, 4, 4.4, 25, 27, False, False, "Lunch dumpling tray"),
    ("Canary Wharf Curry Dock", "Canary Wharf", ["Indian", "Bengali"], 3, 5, 4.1, 21, 31, True, False, "Office curry bundle"),
    ("Camden Dessert Foundry", "Camden", ["Dessert", "Coffee"], 2, 5, 4.7, 35, 19, False, False, "Family waffle box"),
    ("Brixton Thai Orchard", "Brixton", ["Thai"], 2, 4, 4.3, 23, 26, False, False, "Green curry lunch"),
    ("Stratford Family Tandoor", "Stratford", ["Pakistani", "Indian"], 2, 5, 4.5, 30, 33, True, False, "Family tandoor feast"),
    ("Soho Midnight Bao", "Soho", ["Chinese", "Japanese"], 2, 2, 3.4, 12, 20, False, False, "Bao snack deal"),
]


MENU_TEMPLATES = {
    "Bengali": [("Mustard Fish Bowl", "A warming rice bowl with mustard-spiced fish.", "12.95"), ("Lentil Comfort Plate", "Slow cooked lentils, greens, and fragrant rice.", "10.50")],
    "Indian": [("Tandoori Paneer Plate", "Charred paneer, salad, and house chutney.", "11.95"), ("Chicken Masala Box", "A rich tomato masala with pilau rice.", "12.50")],
    "Pakistani": [("Lahori Grill Plate", "Spiced grilled chicken with naan and salad.", "13.50"), ("Chana Rice Bowl", "Chickpeas, herbs, and steamed basmati rice.", "9.95")],
    "Turkish": [("Charcoal Kofte Wrap", "Kofte, pickles, salad, and garlic yoghurt.", "9.95"), ("Falafel Mezze Plate", "Falafel, hummus, grains, and salad.", "10.95")],
    "Italian": [("Roasted Tomato Rigatoni", "Rigatoni with basil-rich tomato sauce.", "11.50"), ("Mushroom White Pizza", "Garlic mushrooms, mozzarella, and rocket.", "13.95")],
    "Thai": [("Green Curry Bowl", "Coconut curry with vegetables and jasmine rice.", "12.25"), ("Tamarind Noodle Box", "Rice noodles with tamarind, lime, and herbs.", "10.95")],
    "Japanese": [("Teriyaki Rice Bento", "Teriyaki chicken, rice, pickles, and greens.", "13.25"), ("Miso Aubergine Don", "Roasted aubergine with miso glaze and rice.", "11.95")],
    "Chinese": [("Ginger Dumpling Tray", "Handmade dumplings with ginger dipping sauce.", "9.95"), ("Crisp Chilli Noodles", "Stir-fried noodles with crisp vegetables.", "10.50")],
    "British": [("Herb Roast Chicken", "Roast chicken, potatoes, greens, and gravy.", "14.95"), ("Root Veg Pie", "Vegetable pie with mash and seasonal greens.", "12.95")],
    "Vegan": [("Rainbow Grain Bowl", "Grains, seasonal veg, seeds, and citrus dressing.", "10.95"), ("Smoky Bean Burger", "Bean patty, slaw, and chips.", "11.75")],
    "Dessert": [("Warm Cookie Skillet", "Soft baked cookie with vanilla cream.", "6.95"), ("Berry Waffle Stack", "Waffles, berries, and whipped cream.", "7.50")],
    "Coffee": [("House Flat White", "Double espresso with steamed milk.", "3.40"), ("Cardamom Cold Brew", "Cold brew with a cardamom finish.", "3.95")],
    "Middle Eastern": [("Lemon Chicken Shawarma", "Chicken shawarma with salad and tahini.", "10.95"), ("Roasted Cauliflower Plate", "Cauliflower, grains, herbs, and sauce.", "11.25")],
    "African": [("Pepper Stew Bowl", "Tomato pepper stew with rice and greens.", "12.95"), ("Plantain Market Plate", "Plantain, beans, salad, and spiced sauce.", "10.95")],
    "Caribbean": [("Jerk Chicken Rice Box", "Jerk chicken, rice, peas, and slaw.", "12.50"), ("Coconut Veg Curry", "Vegetable curry with coconut rice.", "10.95")],
}


class Command(BaseCommand):
    help = "Seed development data for FoodFindr."

    @transaction.atomic
    def handle(self, *args, **options):
        country = self.seed_locations()
        cuisines = self.seed_cuisines()
        users = self.seed_users()
        restaurants = self.seed_restaurants(country, cuisines, users["owner"])
        self.seed_menus(restaurants)
        self.seed_offers(restaurants)
        self.seed_reviews(restaurants, users["customer"])
        self.stdout.write(self.style.SUCCESS("FoodFindr development seed data created."))
        self.stdout.write(f"Seed users use password: {DEV_PASSWORD}")

    def seed_locations(self):
        country, _ = Country.objects.update_or_create(
            code="GB",
            defaults={"name": "United Kingdom"},
        )
        for name in CITY_NAMES:
            City.objects.update_or_create(
                country=country,
                slug=slugify(name),
                defaults={"name": name},
            )

        london = City.objects.get(country=country, slug="london")
        for name, postcode_prefix, latitude, longitude in LONDON_AREAS:
            Area.objects.update_or_create(
                city=london,
                slug=slugify(name),
                defaults={
                    "name": name,
                    "postcode_prefix": postcode_prefix,
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )
        return country

    def seed_cuisines(self):
        cuisines = {}
        for name in CUISINES:
            cuisine, _ = Cuisine.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "icon": slugify(name)},
            )
            cuisines[name] = cuisine
        return cuisines

    def seed_users(self):
        return {
            "customer": self.create_user("customer@foodfindr.local", "FoodFindr Customer", User.Role.CUSTOMER),
            "owner": self.create_user("owner@foodfindr.local", "FoodFindr Owner", User.Role.RESTAURANT_OWNER),
            "admin": self.create_user("admin@foodfindr.local", "FoodFindr Admin", User.Role.ADMIN, is_staff=True),
            "super_admin": self.create_user(
                "superadmin@foodfindr.local",
                "FoodFindr Super Admin",
                User.Role.SUPER_ADMIN,
                is_staff=True,
                is_superuser=True,
            ),
        }

    def create_user(self, email, full_name, role, **flags):
        user, created = User.objects.update_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "role": role,
                "is_email_verified": True,
                "is_active": True,
                **flags,
            },
        )
        if created or not user.has_usable_password():
            user.set_password(DEV_PASSWORD)
            user.save(update_fields=["password"])
        return user

    def seed_restaurants(self, country, cuisines, owner):
        london = City.objects.get(country=country, slug="london")
        restaurants = []
        for index, data in enumerate(RESTAURANTS, start=1):
            name, area_name, cuisine_names, price, hygiene, rating, review_count, prep_time, halal, vegan, offer_title = data
            area = Area.objects.get(city=london, slug=slugify(area_name))
            restaurant, _ = Restaurant.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "owner": owner,
                    "name": name,
                    "description": f"A fictional development listing for {name}, created for FoodFindr demos.",
                    "country": country,
                    "city": london,
                    "area": area,
                    "address": f"{index} Demo Street",
                    "postcode": f"{area.postcode_prefix} {index}FF",
                    "latitude": area.latitude,
                    "longitude": area.longitude,
                    "phone": f"+44207946{1000 + index}",
                    "website": f"https://example.com/{slugify(name)}",
                    "email": f"hello+{slugify(name)}@example.com",
                    "price_level": price,
                    "average_rating": Decimal(str(rating)),
                    "review_count": review_count,
                    "food_hygiene_rating": hygiene,
                    "food_hygiene_rating_date": timezone.now().date(),
                    "food_hygiene_source": "Manual development seed",
                    "local_authority_name": "Demo London Authority",
                    "fsa_business_id": f"DEMO-FSA-{index:04d}",
                    "delivery_fee": Decimal("2.49") + Decimal(index % 3),
                    "minimum_order": Decimal("10.00") + Decimal(index % 4),
                    "average_preparation_time_minutes": prep_time,
                    "service_radius_km": Decimal("4.50"),
                    "is_open": index % 5 != 0,
                    "is_busy": index % 6 == 0,
                    "delivery_available": True,
                    "collection_available": True,
                    "dine_in_available": index % 3 == 0,
                    "phone_order_available": index % 4 == 0,
                    "halal_available": halal,
                    "vegan_available": vegan,
                    "vegetarian_available": True,
                    "gluten_free_available": index % 4 == 0,
                    "uber_eats_url": "https://www.ubereats.com/store/example" if index % 4 == 0 else "",
                    "deliveroo_url": "https://deliveroo.co.uk/menu/example" if index % 5 == 0 else "",
                    "just_eat_url": "https://www.just-eat.co.uk/restaurants/example" if index % 6 == 0 else "",
                    "direct_order_url": f"https://example.com/{slugify(name)}/order" if index % 3 == 0 else "",
                    "is_verified": index % 2 == 0,
                    "is_approved": True,
                    "is_featured": index in {1, 4, 9, 14},
                    "is_premium": index in {4, 6, 10, 17},
                    "featured_until": timezone.now() + timezone.timedelta(days=30) if index in {1, 4, 9, 14} else None,
                    "sponsored_rank_boost": Decimal("4.00") if index in {3, 11, 18} else Decimal("0.00"),
                    "subscription_plan": Restaurant.SubscriptionPlan.PREMIUM if index in {4, 6, 10, 17} else Restaurant.SubscriptionPlan.FREE,
                },
            )
            restaurant.cuisine_types.set(cuisines[cuisine_name] for cuisine_name in cuisine_names)
            restaurant.trust_score = calculate_trust_score(restaurant)
            restaurant.save(update_fields=["trust_score"])
            restaurant.seed_offer_title = offer_title
            restaurant.seed_cuisine_names = cuisine_names
            restaurants.append(restaurant)
        return restaurants

    def seed_menus(self, restaurants):
        for restaurant in restaurants:
            categories = [
                ("House Favourites", "Popular fictional dishes for development demos.", 1),
                ("Lunch & Deals", "Quick plates and weekday-friendly options.", 2),
                ("Drinks & Sides", "Simple sides and drinks.", 3),
            ]
            category_objects = []
            for name, description, display_order in categories:
                category, _ = MenuCategory.objects.update_or_create(
                    restaurant=restaurant,
                    name=name,
                    defaults={
                        "description": description,
                        "display_order": display_order,
                        "is_active": True,
                    },
                )
                category_objects.append(category)

            primary_cuisine = restaurant.seed_cuisine_names[0]
            items = MENU_TEMPLATES.get(primary_cuisine, MENU_TEMPLATES["British"])
            for item_name, description, price in items:
                MenuItem.objects.update_or_create(
                    restaurant=restaurant,
                    category=category_objects[0],
                    name=item_name,
                    defaults={
                        "description": description,
                        "price": Decimal(price),
                        "is_available": True,
                        "is_halal": restaurant.halal_available,
                        "is_vegan": restaurant.vegan_available or "Vegan" in restaurant.seed_cuisine_names,
                        "is_vegetarian": True,
                        "is_gluten_free": restaurant.gluten_free_available,
                        "allergens": ["sesame"] if primary_cuisine in {"Middle Eastern", "Turkish"} else [],
                        "calories": 450,
                        "spicy_level": 2 if primary_cuisine in {"Indian", "Pakistani", "Thai", "Caribbean"} else 1,
                        "preparation_time_minutes": restaurant.average_preparation_time_minutes,
                    },
                )
            MenuItem.objects.update_or_create(
                restaurant=restaurant,
                category=category_objects[1],
                name="Demo Lunch Box",
                defaults={
                    "description": "A fictional lunch set with a main, side, and drink.",
                    "price": Decimal("9.95"),
                    "is_available": True,
                    "is_vegetarian": True,
                    "preparation_time_minutes": 18,
                },
            )
            MenuItem.objects.update_or_create(
                restaurant=restaurant,
                category=category_objects[2],
                name="House Lemonade",
                defaults={
                    "description": "Sparkling lemonade with citrus and mint.",
                    "price": Decimal("3.50"),
                    "is_available": True,
                    "is_vegan": True,
                    "is_vegetarian": True,
                    "is_gluten_free": True,
                    "preparation_time_minutes": 3,
                },
            )

    def seed_offers(self, restaurants):
        now = timezone.now()
        for restaurant in restaurants:
            if not getattr(restaurant, "seed_offer_title", ""):
                continue
            Offer.objects.update_or_create(
                restaurant=restaurant,
                title=restaurant.seed_offer_title,
                defaults={
                    "description": f"Development demo offer for {restaurant.name}.",
                    "offer_type": Offer.OfferType.PERCENTAGE,
                    "discount_value": Decimal("15.00"),
                    "minimum_spend": Decimal("12.00"),
                    "start_date": now - timezone.timedelta(days=1),
                    "end_date": now + timezone.timedelta(days=30),
                    "terms": "Demo data only. Not a real offer.",
                    "is_active": True,
                    "is_featured": restaurant.is_featured,
                },
            )

    def seed_reviews(self, restaurants, customer):
        for restaurant in restaurants:
            Review.objects.update_or_create(
                customer=customer,
                restaurant=restaurant,
                defaults={
                    "rating": round(float(restaurant.average_rating)),
                    "food_quality_rating": round(float(restaurant.average_rating)),
                    "service_rating": 4,
                    "value_rating": 4,
                    "delivery_rating": 4 if restaurant.delivery_available else None,
                    "comment": f"Development review for {restaurant.name}. Friendly service and useful demo data.",
                    "is_approved": True,
                },
            )

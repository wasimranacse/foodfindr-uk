from __future__ import annotations

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

from django.db.models import Q
from django.utils import timezone


AVERAGE_CITY_TRAVEL_SPEED_KMH = 22


def calculate_distance_km(origin_latitude, origin_longitude, target_latitude, target_longitude) -> float | None:
    if None in {origin_latitude, origin_longitude, target_latitude, target_longitude}:
        return None

    try:
        origin_latitude = radians(float(origin_latitude))
        origin_longitude = radians(float(origin_longitude))
        target_latitude = radians(float(target_latitude))
        target_longitude = radians(float(target_longitude))
    except (TypeError, ValueError):
        return None

    latitude_delta = target_latitude - origin_latitude
    longitude_delta = target_longitude - origin_longitude
    haversine = (
        sin(latitude_delta / 2) ** 2
        + cos(origin_latitude) * cos(target_latitude) * sin(longitude_delta / 2) ** 2
    )
    return round(6371 * 2 * asin(sqrt(haversine)), 2)


def estimate_delivery_time_minutes(restaurant, customer_latitude=None, customer_longitude=None) -> int:
    preparation_time = restaurant.average_preparation_time_minutes or 30
    distance_km = calculate_distance_km(
        customer_latitude,
        customer_longitude,
        restaurant.latitude,
        restaurant.longitude,
    )
    if distance_km is None:
        return preparation_time

    travel_minutes = (distance_km / AVERAGE_CITY_TRAVEL_SPEED_KMH) * 60
    busy_buffer = 10 if restaurant.is_busy else 0
    return round(preparation_time + travel_minutes + busy_buffer)


def calculate_trust_score(restaurant) -> int:
    score = 35

    if restaurant.is_verified:
        score += 15
    if restaurant.is_approved:
        score += 10
    if restaurant.food_hygiene_rating is not None:
        score += int(restaurant.food_hygiene_rating) * 6
    if restaurant.average_rating:
        score += float(restaurant.average_rating) * 4
    if restaurant.review_count:
        score += min(10, restaurant.review_count // 10)
    if restaurant.phone and restaurant.email and restaurant.address and restaurant.postcode:
        score += 5
    if restaurant.delivery_available or restaurant.collection_available or restaurant.dine_in_available:
        score += 5

    if restaurant.food_hygiene_rating is not None and restaurant.food_hygiene_rating <= 2:
        score -= 20
    if restaurant.average_rating and float(restaurant.average_rating) < 3:
        score -= 15

    return max(0, min(100, round(score)))


def restaurant_has_active_offer(restaurant) -> bool:
    now = timezone.now()
    return restaurant.offers.filter(
        is_active=True,
    ).filter(
        Q(start_date__isnull=True) | Q(start_date__lte=now),
        Q(end_date__isnull=True) | Q(end_date__gte=now),
    ).exists()


@dataclass(frozen=True)
class RankedRestaurant:
    restaurant: object
    score: float
    distance_km: float | None
    estimated_delivery_time_minutes: int


def smart_rank_restaurants(restaurants, customer_latitude=None, customer_longitude=None) -> list[RankedRestaurant]:
    ranked_restaurants = []

    for restaurant in restaurants:
        distance_km = calculate_distance_km(
            customer_latitude,
            customer_longitude,
            restaurant.latitude,
            restaurant.longitude,
        )
        delivery_time = estimate_delivery_time_minutes(
            restaurant,
            customer_latitude,
            customer_longitude,
        )
        score = 0.0

        if distance_km is not None:
            score += max(0, 30 - min(distance_km * 4, 30))

        score += min(float(restaurant.average_rating or 0) * 8, 40)
        score += min(10, (restaurant.review_count or 0) / 20)
        score += min(20, (restaurant.trust_score or calculate_trust_score(restaurant)) / 5)

        if restaurant.food_hygiene_rating is not None:
            score += int(restaurant.food_hygiene_rating) * 3
        if restaurant_has_active_offer(restaurant):
            score += 6
        score += max(0, 15 - min(delivery_time / 4, 15))
        if restaurant.is_open:
            score += 12
        if restaurant.is_verified:
            score += 8
        if restaurant.is_premium:
            score += 5

        promotional_boost = 0.0
        if restaurant.is_featured:
            promotional_boost += 8
        promotional_boost += min(float(restaurant.sponsored_rank_boost or 0), 10)
        score += promotional_boost

        # Paid placement can help a restaurant surface, but it cannot erase weak trust signals.
        if restaurant.food_hygiene_rating is not None and restaurant.food_hygiene_rating <= 2:
            score -= 25
        if restaurant.average_rating and float(restaurant.average_rating) < 3:
            score -= 20

        ranked_restaurants.append(
            RankedRestaurant(
                restaurant=restaurant,
                score=round(score, 2),
                distance_km=distance_km,
                estimated_delivery_time_minutes=delivery_time,
            )
        )

    return sorted(ranked_restaurants, key=lambda item: item.score, reverse=True)

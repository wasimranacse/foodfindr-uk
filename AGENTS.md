# FoodFindr Agent Instructions

These instructions apply to all future work in the FoodFindr repository.

## Product Context

FoodFindr is a UK-first restaurant discovery, trust, offers, and restaurant promotion platform. It starts in London, expands across the UK, and is designed for later global rollout.

The first product is a web app only, but the mobile web experience must feel like an app.

Use UK English for all user-facing content.

## Non-Negotiables

- Build a real working MVP, not a throwaway prototype.
- Use clean architecture and modular boundaries.
- Do not scrape Deliveroo, Uber Eats, Just Eat, Google, or any third-party platform.
- Use owner-submitted restaurant, menu, offer, and order links for the MVP.
- Keep future official API integrations backend-only.
- Never expose API keys or secrets in frontend code.
- Never return OTP codes from the API.
- Never log OTP codes.
- Store OTP codes hashed only.
- Keep permissions strict from the start.

## Tech Stack

Backend:

- Python.
- Django.
- Django REST Framework.
- PostgreSQL.
- JWT authentication.
- Django admin.
- Environment variables.
- Redis-ready structure.
- Celery-ready structure.

Frontend:

- React.
- Vite.
- Tailwind CSS.
- React Router.
- Axios.
- Mobile-first responsive UI.
- PWA-ready structure.

## Roles

MVP roles:

- `customer`
- `restaurant_owner`
- `admin`
- `super_admin`

Future roles:

- `restaurant_staff`
- `moderator`
- `sales_manager`
- `delivery_partner`

## Security Requirements

Implement and preserve:

- JWT authentication.
- Refresh token rotation and blacklist.
- 6-digit email verification before login.
- OTP expiry after 10 minutes.
- Maximum 5 failed OTP attempts.
- 60-second OTP resend cooldown.
- Hashed OTP storage only.
- Rate limiting and throttling.
- Account lockout after repeated failed login attempts.
- Strong password validation.
- Role-based permissions.
- Admin-only approval actions.
- Owner-only restaurant management.
- Customer-only review and favourite management.
- Security audit logs.
- Secure CORS.
- Environment variables for all secrets and environment-specific settings.

## Backend Architecture Rules

- Keep Django settings split by environment.
- Keep app boundaries clear and modular.
- Put business logic in services/selectors where appropriate, not only in views.
- Use serializers for validation and response shaping.
- Version API routes from the beginning, for example `/api/v1/`.
- Prefer explicit permissions per view/viewset.
- Add tests for authentication, permissions, ownership, and analytics events.
- Do not add third-party integrations directly to frontend code.
- Treat `integrations` as backend-only boundaries for future official APIs.
- Do not introduce scraping logic.
- Use PostgreSQL-compatible model fields and indexes.
- Keep analytics event tracking server-side and explicit.

## Frontend Architecture Rules

- Build mobile-first.
- The phone layout should feel like a mobile app.
- Use bottom navigation on mobile.
- Use sticky search for discovery.
- Use a mobile filter drawer.
- Make buttons large and touch-friendly.
- Use responsive layouts for desktop without compromising mobile.
- Keep API access behind an Axios client module.
- Do not place secrets or privileged configuration in frontend code.
- Keep route-level pages and reusable components separate.
- Build PWA readiness through manifest and icon structure.

## User-Facing Content

- Use UK English.
- Use clear restaurant/customer language.
- Avoid US spelling such as "favorite", "zipcode", or "neighborhood" in user-facing UI.
- Use "favourite", "postcode", and "neighbourhood" or "area" where appropriate.
- Do not overpromise delivery or ordering features in the MVP; make it clear that external ordering links are restaurant-provided.

## MVP Restaurant Ordering Rules

FoodFindr is not a full ordering or delivery platform in the MVP.

Restaurants may provide:

- Uber Eats URL.
- Deliveroo URL.
- Just Eat URL.
- Direct order URL.
- Phone order availability.
- Collection availability.
- Delivery availability.

Track CTA clicks for:

- View Menu.
- Call Restaurant.
- Get Directions.
- Claim Offer.
- Order on Uber Eats.
- Order on Deliveroo.
- Order on Just Eat.
- Order Directly.

## Location Rules

Never hardcode London-only assumptions.

Support:

- Country.
- City.
- Area.
- Borough or district.
- Postcode.
- Latitude.
- Longitude.

London seed data is acceptable for MVP, but schemas and UI copy must support other UK cities and future international rollout.

## Trust and Analytics

FoodFindr's key product advantages include:

- Restaurant Trust Score.
- Smart nearby ranking.
- UK postcode/city/area search.
- Food Hygiene Rating support.
- Allergen and dietary information.
- Smart offers engine.
- Delivery estimate engine.
- Restaurant owner analytics.
- Premium, featured, and sponsored placements.

Design these as extensible services rather than hardcoded one-off logic.

## Permissions Rules

- Admins approve restaurant listings and sensitive changes.
- Owners can only manage restaurants they own.
- Customers can only manage their own reviews and favourites.
- Super admins can manage platform-wide settings.
- Future staff roles must be scoped to assigned restaurants only.

## Repository Hygiene

- Keep commits focused.
- Do not commit secrets, `.env` files, local database files, or generated build output.
- Provide `.env.example` files when environment variables are introduced.
- Prefer clear, boring names over clever abstractions.
- Add documentation when adding a new app, integration boundary, or security-sensitive flow.

## Testing Expectations

Prioritise tests for:

- Registration and email verification.
- Login, refresh, and blacklist behaviour.
- OTP expiry, failed attempts, and resend cooldown.
- Permission and ownership checks.
- Restaurant approval workflow.
- CTA analytics event creation.
- Offer claims.
- Favourite and review ownership.

## Implementation Sequence

1. Repository documentation and skeleton.
2. Django project foundation.
3. Authentication and verification.
4. Location and restaurant models.
5. Offers, menus, favourites, reviews, and analytics.
6. React/Vite frontend foundation.
7. Customer discovery experience.
8. Owner dashboard.
9. Admin workflows.
10. Trust Score, hygiene support, promotions, and analytics refinement.

## Decision Principle

When choosing between speed and future safety, prefer the smallest implementation that is real, secure, and extensible. FoodFindr should be able to grow from London MVP to UK-wide platform without rewriting the foundations.

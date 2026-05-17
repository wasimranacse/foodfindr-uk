# FoodFindr

FoodFindr is a UK-first restaurant discovery, trust, offers, and restaurant promotion platform. The MVP starts in London, expands across the UK, and is designed for later global rollout. The first release is web-only, with a mobile-first experience that should feel app-like on phones.

This repository is currently in the planning and scaffolding stage. The initial implementation will be split into a Django REST API backend and a React/Vite frontend.

## Product Direction

FoodFindr helps customers discover restaurants they can trust and helps restaurants promote themselves without relying on scraping third-party platforms.

The MVP will focus on:

- Restaurant discovery by location, cuisine, dietary needs, offers, and trust signals.
- Owner-submitted restaurant profiles, menus, offers, and external ordering links.
- Trust Score foundations using profile completeness, verification, hygiene data support, review signals, and owner responsiveness.
- CTA analytics for calls, directions, menu views, offer claims, favourites, and external order clicks.
- Restaurant owner tools for managing listings, offers, links, and basic analytics.
- Admin approval and moderation workflows.

FoodFindr must not scrape Deliveroo, Uber Eats, Just Eat, Google, or any third-party platform. All restaurant, menu, offer, and ordering links in the MVP are owner-submitted.

## Target Roles

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

## Business Model

FoodFindr should support the following monetisation paths:

- Free restaurant listing.
- Premium restaurant profile.
- Featured restaurant placement.
- Sponsored search results.
- Offer promotion packages.
- Analytics dashboard subscription.
- Lead generation from calls, directions, menu views, offer claims, favourites, and external order clicks.
- Future direct ordering.
- Future table booking.
- Future mobile app.
- Future global expansion.

## MVP Ordering Strategy

FoodFindr is not starting as a full ordering or delivery platform.

For MVP, restaurant owners can add:

- Uber Eats URL.
- Deliveroo URL.
- Just Eat URL.
- Direct order URL.
- Phone order availability.
- Collection availability.
- Delivery availability.

Customer CTA buttons:

- View Menu.
- Call Restaurant.
- Get Directions.
- Claim Offer.
- Order on Uber Eats.
- Order on Deliveroo.
- Order on Just Eat.
- Order Directly.

Every CTA click must be tracked as an analytics event.

## Architecture Overview

The project will use a modular backend and frontend structure.

```text
FoodFindr/
  README.md
  AGENTS.md
  backend/
    .gitkeep
  frontend/
    .gitkeep
```

Planned backend structure:

```text
backend/
  manage.py
  requirements/
    base.txt
    dev.txt
    prod.txt
  config/
    settings/
      base.py
      dev.py
      prod.py
    urls.py
    asgi.py
    wsgi.py
    celery.py
  apps/
    accounts/
    locations/
    restaurants/
    menus/
    offers/
    reviews/
    favourites/
    analytics/
    trust/
    hygiene/
    promotions/
    audit/
    integrations/
  tests/
  static/
  media/
```

Planned frontend structure:

```text
frontend/
  index.html
  package.json
  vite.config.js
  tailwind.config.js
  postcss.config.js
  public/
    manifest.webmanifest
    icons/
  src/
    app/
    api/
    auth/
    components/
    features/
      discovery/
      restaurants/
      offers/
      favourites/
      owner-dashboard/
      admin/
    layouts/
    pages/
    routes/
    styles/
    utils/
```

## Backend Plan

### Core Stack

- Python.
- Django.
- Django REST Framework.
- PostgreSQL.
- JWT authentication.
- Refresh token rotation and blacklist.
- 6-digit email verification.
- Django admin.
- Redis-ready structure.
- Celery-ready structure.
- Environment-based configuration.

### Django Apps

`accounts`

- Custom user model.
- Role-based permissions.
- JWT login and refresh.
- Email verification using 6-digit OTPs.
- Password validation.
- Account lockout tracking.
- Owner/customer profile data.

`locations`

- Countries, cities, areas, boroughs or districts, postcodes, latitude, and longitude.
- UK-first seed data starting with London.
- Future-ready structure for global expansion.

`restaurants`

- Restaurant profiles.
- Ownership and approval status.
- Contact details.
- Cuisine, dietary, allergen, opening-hours, and service availability data.
- External ordering URLs.
- Premium, featured, and sponsored flags.

`menus`

- Owner-submitted menu links and structured menu sections for future use.
- No third-party scraping.

`offers`

- Offer creation and claim tracking.
- Validity windows.
- Offer promotion package support.

`reviews`

- Customer reviews.
- Owner responses.
- Moderation state.
- Customer-only ownership controls.

`favourites`

- Customer favourites.
- Signals for ranking and analytics.

`analytics`

- CTA click event tracking.
- Lead generation events.
- Restaurant owner analytics summaries.
- Future event pipeline support.

`trust`

- Restaurant Trust Score calculation service.
- Inputs from verification state, profile completeness, hygiene support, review health, owner responsiveness, and moderation history.

`hygiene`

- Food Hygiene Rating support.
- Manual/admin-entered MVP data.
- Future official API integration boundary.

`promotions`

- Featured placements.
- Sponsored search result configuration.
- Premium profile state.

`audit`

- Security audit logs.
- Admin action logs.
- Authentication and permission-sensitive events.

`integrations`

- Backend-only integration boundaries for official APIs later.
- No frontend API secrets.
- No scraping connectors.

## Frontend Plan

### Core Stack

- React.
- Vite.
- Tailwind CSS.
- React Router.
- Axios.
- PWA-ready public assets.
- Mobile-first responsive UI.

### Mobile-First Experience

The mobile website should feel like an installable app:

- Mobile bottom navigation.
- Sticky search.
- Mobile filter drawer.
- Large touch-friendly CTA buttons.
- Responsive restaurant cards.
- Fast search and discovery flows.
- PWA manifest.
- Mobile-friendly owner dashboard.

### Main Frontend Areas

- Customer discovery home.
- Search results.
- Restaurant detail page.
- Offer claim flow.
- Favourites.
- Login, register, verify email, and password flows.
- Restaurant owner dashboard.
- Restaurant profile editor.
- Menu and ordering link editor.
- Offer manager.
- Analytics dashboard.
- Admin approval views.

## Location Model

The app must not hardcode London-only assumptions.

The planned location hierarchy is:

- Country.
- City.
- Area.
- Borough or district.
- Postcode.
- Latitude.
- Longitude.

The MVP should seed London data while keeping the schema suitable for all UK cities and future global locations.

## Security Plan

Security is part of the product architecture, not a bolt-on.

### Authentication

- JWT authentication.
- Refresh token rotation.
- Refresh token blacklist.
- Email verification required before login.
- OTP expiry: 10 minutes.
- Maximum OTP failed attempts: 5.
- Resend cooldown: 60 seconds.
- OTP codes stored hashed only.
- No OTP code in API responses.
- Never log OTP codes.

### Account Protection

- Strong password validation.
- Login throttling.
- Account lockout after repeated failed login attempts.
- Rate limiting for sensitive endpoints.
- Secure password reset flow.

### Authorisation

- Role-based permissions.
- Admin-only approval actions.
- Owners can only manage their own restaurants.
- Customers can only manage their own reviews and favourites.
- Super admin reserved for platform-wide privileged operations.

### Platform Security

- Secure environment variables.
- No secrets in frontend code.
- Secure CORS allowlist.
- CSRF-aware admin configuration.
- Security audit logs.
- Production-safe Django settings.
- Dependency review before adding packages.

## API Design Principles

- Version API routes from the beginning, for example `/api/v1/`.
- Keep frontend and backend contracts explicit.
- Use serializers for validation and output shaping.
- Avoid exposing internal model fields by default.
- Track analytics events server-side through explicit endpoints.
- Keep future direct ordering and booking APIs separate from MVP external-link CTAs.

## Data Seed Plan

MVP seed data should include London examples for:

- Country: United Kingdom.
- City: London.
- Boroughs or districts.
- Areas.
- Example restaurants.
- Example cuisines.
- Example offers.

Seed data must be clearly marked as demo or development data.

## Development Phases

### Phase 0: Planning and Structure

- Create repository documentation.
- Create backend and frontend root folders.
- Define project instructions and architecture.

### Phase 1: Backend Foundation

- Create Django project.
- Configure environment variables.
- Add PostgreSQL configuration.
- Add custom user model.
- Add JWT auth with refresh rotation and blacklist.
- Add hashed email verification OTP flow.
- Add throttling and lockout foundations.
- Add audit logging app.

### Phase 2: Restaurant Discovery API

- Add location models.
- Add restaurant models.
- Add menu and external order link fields.
- Add offer models.
- Add approval workflows.
- Add seed data.

### Phase 3: Frontend Foundation

- Create Vite React app.
- Add Tailwind CSS.
- Add routing and layouts.
- Add Axios client with token refresh handling.
- Add PWA manifest.
- Add mobile bottom navigation and sticky search shell.

### Phase 4: Customer MVP

- Search and filters.
- Restaurant cards.
- Restaurant detail page.
- CTA buttons and analytics tracking.
- Favourites.
- Offer claims.

### Phase 5: Owner MVP

- Owner registration and verification.
- Restaurant profile management.
- Menu and ordering link management.
- Offer management.
- Basic analytics dashboard.

### Phase 6: Admin MVP

- Admin approval flows.
- Restaurant moderation.
- Review moderation.
- Audit log visibility.

### Phase 7: Trust and Growth

- Trust Score service.
- Hygiene support.
- Sponsored and featured ranking.
- Premium profile features.
- Analytics subscriptions.

## Definition of Done for MVP

- Customers can register, verify email, log in, search restaurants, view details, claim offers, favourite restaurants, and use CTA buttons.
- Restaurant owners can register, verify email, create and manage their restaurant profile, add menu/order links, publish offers, and view analytics.
- Admins can approve restaurants and review sensitive activity.
- CTA analytics are captured.
- Permissions prevent cross-account data access.
- Secrets are environment-only.
- The frontend works well on mobile and desktop.
- The structure is ready for official backend-only integrations later.
# foodfindr-uk

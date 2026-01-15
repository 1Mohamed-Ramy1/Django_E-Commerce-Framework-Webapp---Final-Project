# API & Endpoint Reference

This document lists all public routes (template pages and JSON APIs) in the project and describes how they work.

Notes:
- Routes shown are relative to the site root.
- If a view accepts POST/GET both are noted where applicable.

---

**Root**:
- `/` : Redirects to dashboard (`dashboard:home`) if staff, to shop home (`shop:shop_home`) if authenticated, otherwise to login. (See `accounts.views.home_redirect`)

**Accounts** (`/accounts/`)
- `/accounts/profile/` (GET): User profile page; requires login. Shows profile, recent orders, recent gift redemptions. (`accounts.views.profile`)
- `/accounts/register/` (GET, POST): Registration form; POST creates a new `User`. (`accounts.views.RegisterView`)
- `/accounts/login/` (GET, POST): Login form; POST authenticates and redirects (staff -> dashboard, others -> shop). (`accounts.views.LoginView`)
- `/accounts/logout/` (GET): Logs out and redirects to login. (`accounts.views.LogoutView`)
- `/accounts/forgot-password/` (GET, POST): Request password reset; sends a time-limited activation code email. (`accounts.views.ForgotPassword`)
- `/accounts/enter-activation-code/` (GET, POST): Enter 6-digit code sent by email; validates and redirects to reset. (`accounts.views.EnterActivationCode`)
- `/accounts/reset-password/<activation_code>/` (GET, POST): Reset password with valid activation code (expires ~5 minutes). (`accounts.views.ResetPassword`)
- `/accounts/edit-profile/` (GET, POST): Edit profile and basic user fields; requires login. (`accounts.views.edit_profile`)

**Blog** (`/blog/`)
- `/blog/` (GET): Public blog feed (one generated 'post' per product in a shuffled order). (`blog.views.public_blog_list`)
- `/blog/post/<slug>/` (GET): Public blog post detail by slug (real blog posts). (`blog.views.public_blog_detail`)
- `/blog/post/<int:id>/` (GET): Product-news detail page generated from a product (product id). (`blog.views.public_blog_detail_by_id`)

- Dashboard CRUD (staff-only): all under `/blog/dashboard/` paths (create/update/delete/list) — require staff. (`blog.views.blog_list`, `blog_create`, `blog_update`, `blog_delete`)

**Shop** (`/shop/`)
- `/shop/` (GET): Shop homepage template; shows random products and recent blog items. (`shop.views.shop_home`)
- `/shop/product/<int:pk>/` (GET): Product detail page. (`shop.views.product_detail`)

- Cart (login required):
  - `/shop/cart/` (GET): View cart. (`shop.views.view_cart`)
  - `/shop/cart/add/<int:product_id>/` (POST): Add product to cart (requires login). For clothing items a `size` POST field is required; quantity optional. (`shop.views.add_to_cart`)
  - `/shop/cart/update/<int:item_id>/` (POST): Update quantity for a cart item; enforces available stock. (`shop.views.update_cart`)
  - `/shop/cart/remove/<int:item_id>/` (POST): Remove item. Returns JSON `{'message': 'Item removed'}`. (`shop.views.remove_from_cart`)

- Checkout & Orders (login required):
  - `/shop/checkout-page/` (GET, POST): Checkout page; GET renders cart totals, POST creates an `Order` with items then redirects to payments countdown. (`shop.views.checkout_page`)
  - `/shop/orders/` (GET): List of user's orders. (`shop.views.orders_list`)
  - `/shop/order/<int:order_id>/` (GET): Order detail for the current user. (`shop.views.order_detail`)

- Admin Product CRUD (staff-only):
  - `/shop/admin/products/create/` (GET, POST) create product
  - `/shop/admin/products/<int:pk>/edit/` (GET, POST) edit product
  - `/shop/admin/products/<int:pk>/delete/` (POST) delete product

- JSON APIs (shop):
  - `/shop/api/orders/` (GET): Returns the authenticated user's orders as JSON (id, totals, payment method, status, created_at). (`shop.views.order_history_api`)
  - `/shop/api/random-products/` (GET): Returns a JSON list of random products for homepage. Query param: `count` (default 24). (`shop.views.random_products_api`)
  - `/shop/api/suggestions/` (GET): Search/autocomplete suggestions. Query params: `q` (query), optional `category`, `limit`. Returns suggestions for categories, subcategories, products (JSON). (`shop.views.suggestions_api`)

Note: `shop.views.PaymentWebhook` is implemented (class `PaymentWebhook`) to accept JSON POST webhooks (payload must contain `order_id`, `status`, `amount`, `currency`) and update order/payment/stock, but it is not mapped to a URL in the repo by default.

**Order Management** (`/orders/`)
- `/orders/order/<int:order_id>/` (GET): Order detail for the logged-in owner. (`order_management.views.order_detail`)
- `/orders/order/<int:order_id>/invoice/` (GET): Download invoice PDF for a completed order — this delegates to `payments.views.invoice_pdf`. Requires ownership and `status='completed'`. (`order_management.views.download_invoice`)

**Payments** (`/payments/`)
- `/payments/countdown/<int:order_id>/` (GET): Post-checkout countdown page while awaiting payment. (`payments.views.countdown`)
- `/payments/confirm/<int:order_id>/` (GET/POST): Confirm payment endpoint — marks `Payment.confirm()` and awards profile points; renders a thank-you page. (`payments.views.confirm_payment`)
- `/payments/invoice/<int:order_id>/` (GET): Returns a PDF `FileResponse` with the invoice/receipt (created using ReportLab). (`payments.views.invoice_pdf`)

**Gift** (`/gifts/`)
- `/gifts/` (GET): List available gifts and user points if authenticated. (`gift.views.gift_list`)
- `/gifts/redeem/<uuid:uid>/` (GET, POST): Gift redemption flow. POST attempts to redeem (requires login), checks points and stock, deducts points, reduces stock, creates `GiftRedemption`, and sends confirmation email. (`gift.views.redeem_gift`)
- `/gifts/my-redemptions/` (GET): User's gift redemption history (requires login). (`gift.views.my_redemptions`)

**Events** (`/events/`)
- `/events/` (GET): Public event list. (`events.views.event_list`)
- `/events/create/` (GET, POST): Create an event (basic user-facing create function present). (`events.views.create_event`)
- `/events/<int:event_id>/edit/` (GET, POST): Admin edit (if mapped to admin view). (`events.views.edit_event` and `create_event_admin` exist for admin flows)
- `/events/detail/<uuid:uid>/` (GET): Event detail by UID. (`events.views.event_detail`)
- `/events/api/featured/` (GET): JSON API returning featured/active events for homepage. Query param: `count` (default 6). (`events.views.api_featured_events`)

**Dashboard** (`/dashboard/`) — admin/staff-only UI
- `/dashboard/` (GET): Dashboard home — summary counts. (`dashboard.views.dashboard_home`)
- Products CRUD: `/dashboard/products/`, `/dashboard/products/add/`, `/dashboard/products/edit/<int:pk>/`, `/dashboard/products/delete/<int:pk>/` (staff-only)
- Users management: `/dashboard/users/`, `/dashboard/users/create/`, `/dashboard/users/update/<int:pk>/`, `/dashboard/users/delete/<int:pk>/`, `/dashboard/users/warn/<int:pk>/` (staff-only)
- Events, Weather, Blog management: corresponding CRUD endpoints under `/dashboard/` (staff-only)
- Orders management: `/dashboard/orders/`, `/dashboard/orders/<int:pk>/`, `/dashboard/orders/<int:pk>/status/` (POST), `/dashboard/orders/<int:pk>/cancel/` (staff-only)

**Weather** (`/weather/`)
- `/weather/` (GET, POST): Weather search widget/page; POST submits `city` and queries OpenWeatherMap (saves search history). Requires `WEATHER_API_KEY` in settings for the newer `weather_search` view. (`weather.views.weather_search`)

---

Implementation notes & behavior details
- Authentication: many pages require login (`@login_required`) and admin pages require staff (`user_passes_test(lambda u: u.is_staff)` or `@staff_member_required`).
- Payments: the repo contains both an interactive payment flow (redirect to `/payments/countdown/`, then `/payments/confirm/`) and a webhook handler `PaymentWebhook` (in `shop.views`) intended for asynchronous gateway notifications — add a URL for the webhook in production (and secure it with a secret/signature).
- PDF invoices: generated with ReportLab in `payments.views.invoice_pdf` and returned as `FileResponse`.
- JSON APIs: `random-products`, `suggestions`, `order_history_api`, `events/api/featured/`, and `cart/remove` are JSON endpoints; most others render templates.

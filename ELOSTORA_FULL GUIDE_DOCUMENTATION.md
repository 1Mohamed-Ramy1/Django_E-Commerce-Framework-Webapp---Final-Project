# ELOSTORA — Complete Project Documentation (English)

Version: 1.0.0
Date: January 2026
Status: Production-ready

This single-file document consolidates the entire project's information: architecture, how to build and run, environment variables, endpoints and APIs, UI/design system, component references, deployment and QA checklists, bug fixes, and the password-reset activation-code system. The content is entirely in English and contains the combined, cleaned, and organized information from the repository documentation.

Note: "To go to Admin panel with Superuser in login page (http://127.0.0.1:8000/accounts/login/): Username: ELOSTORA
         Password: admin@8080"
--

## 1. Project Overview

- Project: ELOSTORA E-Commerce Platform (Django)
- Purpose: Production-grade e-commerce with a premium responsive UI and admin dashboard
- Main apps: `accounts`, `shop`, `blog`, `events`, `payments`, `gift`, `dashboard`, `order_management`, `weather`, `coupons`
- Repo root highlights: `manage.py`, `core/` (project + apps), `templates/`, `static/`, `media/`, `db.sqlite3`

---

## 2. Prerequisites & System Requirements

Before starting, ensure you have the following installed:

### Required Software:
- **Python 3.8+** (recommended: Python 3.10 or higher)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Virtual Environment** tool (venv or virtualenv)

### Optional (for Production):
- **PostgreSQL** (recommended for production database)
- **Nginx** (reverse proxy)
- **Gunicorn** (WSGI server)

### API Keys Required:
1. **Gmail App Password** - For email functionality (password reset, order confirmations)
   - Go to: https://myaccount.google.com/apppasswords
   - Generate a new app password for "Mail"
   
2. **OpenWeatherMap API Key** - For weather feature
   - Sign up at: https://openweathermap.org/api
   - Get your free API key from the dashboard

---

## 3. Quick Start (Complete Setup Guide)

Follow these steps **in order** to set up the project from scratch:

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Final-Project-E-Commerce
```

### Step 2: Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install All Dependencies

```bash
pip install -r requirements.txt
```

**Main dependencies that will be installed:**
- Django 6.0
- python-decouple (environment variables)
- django-crispy-forms (form styling)
- crispy-bootstrap4 (Bootstrap 4 support)
- ReportLab (PDF invoice generation)
- Pillow (image processing)
- requests (API calls)

### Step 4: Configure Environment Variables

1. **Copy the example environment file:**

```bash
cp .env.example core/.env
```

2. **Edit `core/.env` with your actual credentials:**

```env
# Django Core Settings
SECRET_KEY=your-super-secret-django-key-here-change-this
DEBUG=True

# Email Configuration (Gmail SMTP)
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password-here

# External APIs
WEATHER_API_KEY=your-openweathermap-api-key-here
```

**⚠️ Important Notes:**
- Generate a secure SECRET_KEY (you can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Use Gmail App Password (NOT your regular Gmail password)
- Keep DEBUG=True for development only

### Step 5: Set Up the Database

Run migrations to create all database tables:

```bash
cd core
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, blog, contenttypes, coupons, events, gift, order_management, payments, sessions, shop, weather
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 6: Load Initial Data (ONE COMMAND!)

**🚀 This is the magic command - it loads EVERYTHING:**

```bash
python manage.py load_initial_data
```

✅ **What gets loaded automatically:**
- ✓ 1000+ Products with images
- ✓ Categories and Subcategories
- ✓ Product sizes and variations
- ✓ Discount coupons
- ✓ Gift rewards for loyalty points
- ✓ Events and promotions
- ✓ Blog posts and articles

**Expected output:**
```
Loading initial data fixtures...

Loading Shop data (categories, products, sizes)... ✓
Loading Coupons... ✓
Loading Gifts... ✓
Loading Events... ✓
Loading Blog posts... ✓

Initial data loaded successfully!

Next steps:
  1. Create a superuser: python manage.py createsuperuser
  2. Run the server: python manage.py runserver
```

**No need to run multiple commands!** Everything loads in the correct order automatically. ⚡

### Step 7: Create Admin Superuser

Create your admin account to access the admin panel:

```bash
python manage.py createsuperuser
```

**You'll be prompted to enter:**
- Username (e.g., admin)
- Email address
- Password (must be strong)

### Step 8: Start the Development Server

```bash
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 9: Access the Application

Open your browser and visit:

- **🏠 Frontend Homepage:** http://127.0.0.1:8000/
- **👤 User Login:** http://127.0.0.1:8000/accounts/login/
- **⚙️ Admin Panel:** http://127.0.0.1:8000/admin/
- **🛍️ Shop:** http://127.0.0.1:8000/shop/
- **📝 Blog:** http://127.0.0.1:8000/blog/

**Test Login Credentials Superuser (if you loaded fixtures):**
- Admin Username: `ELOSTORA`
- Admin Password: `admin@8080`

---

## 4. Verification Checklist

After setup, verify everything is working:

- [ ] Server starts without errors
- [ ] Homepage loads with products
- [ ] Can browse shop and view product details
- [ ] Can add products to cart
- [ ] Admin panel accessible at `/admin/`
- [ ] Static files (CSS/images) loading correctly
- [ ] No 404 errors in browser console

**If you see any errors:**
1. Check that all migrations ran successfully
2. Verify `.env` file is in the `core/` directory
3. Ensure virtual environment is activated
4. Check terminal for error messages

---

## 5. Database & Fixtures

### Why Fixtures?

The `db.sqlite3` file is **not included** in the repository (listed in `.gitignore`) to avoid committing sensitive data and large binary files. Instead, we use **fixtures** to provide initial data that anyone can load after cloning the project.

### Available Fixtures

All fixtures are stored in the `fixtures/` directory within each app:

- **shop_data** → Products, categories, subcategories, and product sizes
- **blog_data** → Blog posts and categories
- **events_data** → Events and promotions
- **gift_data** → Gift rewards for loyalty points
- **coupons_data** → Discount coupons

### Loading Fixtures

**🚀 Quick Setup (Recommended for New Users):**

After running `migrate`, load all data with **ONE simple command**:

```bash
python core/manage.py load_initial_data
```

✅ **This automatically loads everything:**
- All products, categories, and subcategories
- All coupons and discounts
- All gifts and loyalty rewards
- All events and promotions
- All blog posts and articles

**Output example:**
```
Loading initial data fixtures...

Loading Shop data (categories, products, sizes)... ✓
Loading Coupons... ✓
Loading Gifts... ✓
Loading Events... ✓
Loading Blog posts... ✓

Initial data loaded successfully!
```

**That's it! Your database is now fully populated and ready to use.** 🎉

---

**Advanced: Load individually (optional)**

If you prefer to load specific fixtures only:

```bash
python core/manage.py loaddata shop_data
python core/manage.py loaddata blog_data
python core/manage.py loaddata events_data
python core/manage.py loaddata gift_data
python core/manage.py loaddata coupons_data
```

### Exporting New Fixtures (For Developers)

If you add new products or data and want to update the fixtures:

```bash
# Export shop data
python manage.py dumpdata shop.Category shop.SubCategory shop.Product shop.ProductSize --indent 2 --output shop/fixtures/shop_data.json

# Export blog data
python manage.py dumpdata blog --indent 2 --output blog/fixtures/blog_data.json

# Export events data
python manage.py dumpdata events --indent 2 --output events/fixtures/events_data.json

# Export gifts data
python manage.py dumpdata gift --indent 2 --output gift/fixtures/gift_data.json

# Export coupons data
python manage.py dumpdata coupons --indent 2 --output coupons/fixtures/coupons_data.json
```

**Note:** Always use `--indent 2` to make the JSON files readable and easy to review in version control.

---

## 3. Important Configuration

Key settings (file: `core/core/settings.py`):

- SECRET_KEY: from env via `python-decouple` `config('SECRET_KEY')`
- DEBUG: from env `DEBUG` (cast to bool)
- DATABASES: SQLite by default (`BASE_DIR / 'db.sqlite3'`)
- EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
- MEDIA_URL = `/media/` and MEDIA_ROOT = BASE_DIR / `media`
- STATIC_URL = `/static/`, STATICFILES_DIRS includes `staticfiles`, STATIC_ROOT set for production
- WEATHER_API_KEY from env (used by weather app)
- ALLOWED_HOSTS includes `127.0.0.1`, `localhost`, `ELOSTORA_Shop.com`

Security: when `DEBUG=False`, HSTS and HTTPS enforcement flags are enabled in `settings.py`.

---

## 4. How the System Works (High-level)

- Users browse products in the `shop` app and can add to a DB-backed cart.
- Checkout creates an `Order` and `OrderItem` records and a `Payment` object; user is redirected to `/payments/countdown/<order_id>/`.
- Payments are finalized via `/payments/confirm/<order_id>/` (user flow). The project also contains a `PaymentWebhook` class that can accept asynchronous webhooks (if mapped to a URL) to update order status and deduct stock.
- Accounts module handles registration/login/logout and a password-reset flow that uses a 6-digit activation code (email) instead of a UUID link.
- Dashboard (staff-only) provides CRUD for products, users, orders, events, weather entries, and blog posts.
- The `gift` app allows users to redeem gifts using loyalty points; these create `GiftRedemption` records and send confirmation emails.
- Weather uses OpenWeatherMap API to fetch weather and save `SearchHistory` records.

---

## 5. Endpoints & Routes (concise)

Root (`/`): redirects to dashboard home (staff), shop home (authenticated users), or login otherwise.

Accounts (`/accounts/`):
- `/accounts/profile/` (GET) — profile page (login required)
- `/accounts/register/` (GET, POST) — registration
- `/accounts/login/` (GET, POST) — login
- `/accounts/logout/` (GET) — logout
- `/accounts/forgot-password/` (GET, POST) — start password reset (sends activation code)
- `/accounts/enter-activation-code/` (GET, POST) — enter code
- `/accounts/reset-password/<activation_code>/` (GET, POST) — set new password
- `/accounts/edit-profile/` (GET, POST) — edit profile (login required)

Blog (`/blog/`): public feed and product-news endpoints, and staff CRUD under dashboard.

Shop (`/shop/`):
- `/shop/` (GET) — shop home
- `/shop/product/<pk>/` (GET) — product detail
- `/shop/cart/`, `/shop/cart/add/<product_id>/`, `/shop/cart/update/<item_id>/`, `/shop/cart/remove/<item_id>/` — cart operations
- `/shop/checkout-page/` (GET, POST) — checkout
- `/shop/orders/`, `/shop/order/<order_id>/` — user's orders
- `/shop/api/orders/`, `/shop/api/random-products/`, `/shop/api/suggestions/` — JSON APIs

Order Management (`/orders/`): order detail and invoice download (delegates to payments.invoice_pdf).

Payments (`/payments/`): countdown, confirm, and invoice PDF generation.

Gift (`/gifts/`): gift list, redeem (`/gifts/redeem/<uuid>/`), my redemptions.

Events (`/events/`): event list, create, edit, detail by UID, and `/events/api/featured/` JSON endpoint.

Dashboard (`/dashboard/`): staff-only CRUD and management pages.

Weather (`/weather/`): search widget form that queries OpenWeatherMap and stores history.

Note: For per-view parameter details and behavior, see `API_DOCUMENTATION.md` in repository root.

---

## 6. Password Reset — Activation Code Flow (detailed)

Overview: the reset flow uses a 6-digit activation code. Key properties:

- Activation code: 6-digit numeric string, generated and saved in `accounts.models.PasswordReset`.
- Expiration: code expires after ~5–10 minutes (views check creation time and enforce expiry).
- Flow:
  1. User requests password reset at `/accounts/forgot-password/` with email.
  2. System deletes old reset requests for that user, creates a new `PasswordReset` with activation code, and sends an email containing the code.
  3. User visits `/accounts/enter-activation-code/` and submits the code.
  4. If valid and not expired, user is redirected to `/accounts/reset-password/<activation_code>/`.
  5. User sets new password (POST) and reset record is deleted.

Security notes:
- Codes are unique per request and deleted after successful reset.
- Server-side expiration checks prevent reuse.
- Email sending is configured using SMTP settings in `settings.py`.

---

## 7. UI & Design System

The project includes a premium UI design system implemented in CSS with tokens, responsive utilities, components, and critical inline CSS for the navbar and footer to avoid FOUC.

Highlights:

- 50+ CSS variables (colors, spacing, shadows, radii, z-index)
- 6 responsive breakpoints: xs (320), sm (640), md (768), lg (1024), xl (1280), 2xl (1536)
- Components: navbar, footer, buttons, cards, forms, layout utilities
- Custom scrollbar implemented in CSS
- Accessibility: WCAG 2.1 AA compliance, ARIA labels, keyboard navigation
- Performance: mobile-first, minimal JS, GPU-accelerated transitions

Files:
- `core/static/css/design-system.css` — tokens and component classes
- `core/templates/partials/navbar.html` — premium navbar (inline critical CSS)
- `core/templates/partials/footer.html` — premium footer (inline critical CSS)

Design tokens examples (CSS variables):

```css
:root {
  --color-primary: #667eea;
  --color-secondary: #764ba2;
  --color-accent: #f093fb;
  --color-warm: #ff9800;
  --space-sm: 8px;
  --space-md: 16px;
  --radius-md: 12px;
}
```

---

## 8. Profiles & Account UI (summary)

Profile model (main fields):

- user (OneToOneField to User)
- phone (CharField)
- address (TextField)
- image (ImageField upload_to='profiles/' with a default image)
- warning (BooleanField)
- blocked (BooleanField)
- balance (DecimalField)
- total_spent (DecimalField)
- last_purchase (DateTimeField)
- loyalty_points / points (IntegerField)

Forms:
- `UserForm` (first_name, last_name, email)
- `ProfileForm` (phone, address, image)

Views:
- `profile(request)` — renders profile and recent orders, gift redemptions
- `edit_profile(request)` — GET renders forms; POST validates `UserForm` and `ProfileForm`, handles `request.FILES`, saves and redirects

Templates: `accounts/profile.html` and `accounts/edit_profile.html` — include profile card, info sections, order table, and image upload (multipart/form-data).

CSS: `static/css/profile.css` — grid layout, circular profile image, responsive rules.

---

## 9. PDF Invoice Generation

Invoices are created with ReportLab in `payments.views.invoice_pdf` and saved to `media/invoices/receipt_<order_id>.pdf`. The view then returns a `FileResponse` for downloading.

Key details:
- Page template built using ReportLab Platypus Table and Paragraphs
- Invoice includes order items, subtotal, delivery fee, final total
- Timezone and formatting applied (Cairo/UTC+2 example used in code)

---

## 10. Webhooks & Payment Handling

The project includes a `PaymentWebhook` class-based view in `shop.views` that parses JSON payloads with required fields `order_id`, `status`, `amount`, `currency`, updates the order, and reduces stock on successful payment. This handler is not mapped to a URL by default; add a secure endpoint and signature verification for production.

---

## 11. Notable Bug Fixes (history)

1. CSS 404: copied `design-system.css` to `staticfiles/css/` and added cache-busting query string `?v=1` in templates.
2. Search TypeError: fixed improper use of `list.count()` vs. `QuerySet.count()` in `shop.views.global_search`.
3. Cart/Checkout: server-side checks adjust cart quantities to available stock and remove items when out of stock.
4. Password reset flow: switched to 6-digit activation codes, added views and templates for entering codes.

---

## 12. Testing & QA

Run tests (if test suite exists):

```bash
python manage.py test
```

Manual checks included in the repository documentation:

- Visual checks: navbar, footer, profile, order table
- Functional: search, add-to-cart, checkout, payment confirm, gift redemption
- Responsive tests for breakpoints
- Accessibility audit (keyboard, ARIA, color contrast)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)

---

## 13. Deployment Checklist

Pre-deployment:

- Ensure `DEBUG=False` and set `SECRET_KEY` and `ALLOWED_HOSTS`.
- Configure production `DATABASES` (Postgres recommended).
- Configure an SMTP service for `EMAIL_HOST` settings.
- Add the payment webhook URL and secure it (HMAC or secret).
- Run `python manage.py collectstatic --noinput`.
- Ensure `MEDIA_ROOT` is served (Nginx or storage like S3).

Deployment steps:

1. Backup database and current assets.
2. Deploy code to the server.
3. Install dependencies and migrations: `pip install -r requirements.txt` (create file if absent), `python manage.py migrate`.
4. Collect static files: `python manage.py collectstatic --noinput`.
5. Restart application server (Gunicorn/Daphne) and reverse proxy (Nginx).
6. Smoke test main flows (home, product, cart, checkout, payment confirmation, profile).

Monitoring after deployment:

- Watch server logs for errors.
- Monitor payment webhook logs and order status transitions.
- Verify PDF invoice generation and media uploads.

---

## 14. File Inventory (high-level)

Key files and folders (workspace root `core/`):

- `manage.py` — Django CLI entry
- `core/core/settings.py` — settings
- `core/core/urls.py` — root urls
- `accounts/` — models, views, forms, urls, templates
- `shop/` — products, cart, checkout, APIs
- `payments/` — countdown, confirm, invoice_pdf
- `dashboard/` — staff admin UI
- `blog/`, `events/`, `gift/`, `weather/` — related functionality
- `static/` and `staticfiles/` — CSS and assets
- `media/` — uploaded files and generated invoices

For a complete file list and embedded source, see the auto-generated `PROJECT_DOCUMENTATION.md` at repository root.

---

## 15. Appendices

- Appendix A: Example JSON API calls (quick reference):

  - Random products:

  ```bash
  curl "http://localhost:8000/shop/api/random-products/?count=12"
  ```

  - Suggestions:

  ```bash
  curl "http://localhost:8000/shop/api/suggestions/?q=phone&limit=8"
  ```

  - Order history (requires session/auth cookie):

  ```bash
  curl -b cookies.txt "http://localhost:8000/shop/api/orders/"
  ```

- Appendix B: Password reset email template

  Subject: Password Reset — Activation Code

  Body:

  "Your password reset activation code is: <CODE>. This code expires in 5 minutes. Enter the code on the password reset page to continue."

---

## 17. Final Sign-off

Project: ELOSTORA E-Commerce Platform — Premium UI & Core Functionality

Completed: January 2026

"""
Visual representation of the Three-Tier User Hierarchy System
"""

# ════════════════════════════════════════════════════════════════════════════
#                    THREE-TIER USER HIERARCHY STRUCTURE
# ════════════════════════════════════════════════════════════════════════════

HIERARCHY = """
┌─────────────────────────────────────────────────────────────────────────┐
│                    👑 ADMIN (ELOSTORA) - Tier 1                        │
│                                                                         │
│  Username: admin                                                        │
│  Password: admin@8080@                                                  │
│  Email: admin@8080@                                                     │
│                                                                         │
│  📋 Permissions:                                                        │
│     ✓ Full system access                                              │
│     ✓ Create/Edit/Delete ALL users                                   │
│     ✓ Create/Edit/Delete managers                                    │
│     ✓ Access all admin features                                      │
│                                                                         │
│  🔒 Protections:                                                        │
│     • Cannot be edited by managers                                     │
│     • Cannot be deleted by managers                                    │
│     • Cannot be demoted by managers                                    │
│     • Read-only in manager's admin panel                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▲
                                    │
                          ┌─────────┴──────────┐
                          │                    │
                          │ (can promote)      │ (can demote)
                          │                    │
                          ▼                    ▼
┌──────────────────────────────────┐ ┌─────────────────────────────────────┐
│  ⭐ MANAGER - Tier 2             │ │  👤 USER - Tier 3                  │
│  (Staff user in 'managers' group)│ │  (Regular user)                    │
│                                  │ │                                     │
│  Properties:                     │ │  Properties:                        │
│  • is_staff = True              │ │  • is_staff = False                │
│  • is_superuser = False         │ │  • is_superuser = False            │
│  • groups = ['managers']        │ │  • groups = []                     │
│                                  │ │                                     │
│  📋 Permissions:                 │ │  📋 Permissions:                    │
│     ✓ View regular users         │ │     ✓ Use application normally      │
│     ✓ Create regular users       │ │     ✓ Browse shop                   │
│     ✓ Edit regular users         │ │     ✓ Make purchases                │
│     ✓ Delete regular users       │ │     ✓ Manage own profile            │
│     ✗ View admin user            │ │     ✓ View own orders               │
│     ✗ Edit admin user            │ │     ✓ Submit support tickets        │
│     ✗ Edit other managers        │ │                                     │
│     ✗ Delete admin user          │ │  🔒 Restrictions:                   │
│                                  │ │     • No access to admin panel       │
│  🔒 Protections:                 │ │     • Cannot manage users           │
│     • Can only edit regular users│ │     • Cannot view staff panel       │
│     • Cannot edit admin          │ │     • Cannot modify settings        │
│     • Cannot edit other managers │ │                                     │
│     • Views only regular users   │ │                                     │
│     • Uses filtered admin panel  │ │                                     │
└──────────────────────────────────┘ └─────────────────────────────────────┘
"""

# ════════════════════════════════════════════════════════════════════════════
#                         ADMIN PANEL VISIBILITY
# ════════════════════════════════════════════════════════════════════════════

ADMIN_PANEL_VIEW = """
┌─────────────────────────────────────────────────────────────────────────┐
│                    ADMIN PANEL VISIBILITY & ACTIONS                     │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────┬──────────────────────┐
│  👑 ADMIN Sees       │  ⭐ MANAGER Sees     │  👤 USER Sees        │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ • All admin users    │ • Regular users only │ • Nothing (blocked)  │
│ • All managers       │ • NOT admin users    │                      │
│ • All regular users  │ • NOT other managers │                      │
│ • All events         │ • Events (view only) │                      │
│ • All orders         │ • Orders (limited)   │                      │
│ • All products       │ • Products (limited) │                      │
│ • System settings    │ • Basic settings     │                      │
│                      │                      │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Can Do:              │ Can Do:               │ Cannot:              │
│ ✓ Add users          │ ✓ Add regular users  │ × Access admin       │
│ ✓ Edit all users     │ ✓ Edit regular users │ × Manage users       │
│ ✓ Delete all users   │ ✓ Delete reg users   │ × View settings      │
│ ✓ Promote to manager │ ✗ Edit admin         │ × Change policies    │
│ ✓ Manage everything  │ ✗ Edit managers      │ × Delete anything    │
│ ✓ Change settings    │ ✗ Delete admin       │                      │
│                      │ ✓ Basic management   │                      │
└──────────────────────┴──────────────────────┴──────────────────────┘

Database Query Results:
═════════════════════════════════════════════════════════════════════════════

👑 ADMIN Queries:
├─ User.objects.all() 
│  └─ Returns: [admin, manager1, manager2, user1, user2, ...]  ← ALL
├─ User.objects.filter(is_staff=True) 
│  └─ Returns: [admin, manager1, manager2]  ← All staff
└─ User.objects.filter(groups__name='managers') 
   └─ Returns: [manager1, manager2]  ← Only managers

⭐ MANAGER Queries (Filtered):
├─ User.objects.filter(is_superuser=False, groups__isnull=True)
│  └─ Returns: [user1, user2, user3, ...]  ← Only regular users
├─ Attempting to view admin → PROTECTED (readonly)
└─ Attempting to delete admin → DENIED (permission error)

👤 USER Queries (Blocked):
├─ User.objects.all() 
│  └─ Returns: No access (PermissionDenied)
├─ Admin panel access
│  └─ Blocked: Not staff member
└─ Any management feature
   └─ Blocked: Not in required groups
"""

# ════════════════════════════════════════════════════════════════════════════
#                      PERMISSION MATRIX
# ════════════════════════════════════════════════════════════════════════════

PERMISSION_MATRIX = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                    ROLE-BASED PERMISSION MATRIX                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Action                    │  👑 ADMIN  │  ⭐ MANAGER  │  👤 USER  │  Guest │
│  ────────────────────────  │  ─────────  │  ──────────  │  ────────  │  ─── │
│  Access Admin Panel        │     ✓      │      ✓       │     ✗      │   ✗  │
│  View all users            │     ✓      │      ✗       │     ✗      │   ✗  │
│  View managers             │     ✓      │      ✗       │     ✗      │   ✗  │
│  View regular users        │     ✓      │      ✓       │     ✗      │   ✗  │
│  Create user               │     ✓      │      ✓       │     ✗      │   ✗  │
│  Edit own profile          │     ✓      │      ✓       │     ✓      │   ✗  │
│  Edit other user           │     ✓      │      ✓*      │     ✗      │   ✗  │
│  Edit admin                │     ✓      │      ✗       │     ✗      │   ✗  │
│  Edit manager              │     ✓      │      ✗       │     ✗      │   ✗  │
│  Delete user               │     ✓      │      ✓*      │     ✗      │   ✗  │
│  Delete admin              │     ✓      │      ✗       │     ✗      │   ✗  │
│  Delete manager            │     ✓      │      ✗       │     ✗      │   ✗  │
│  Manage roles              │     ✓      │      ✗       │     ✗      │   ✗  │
│  View settings             │     ✓      │      ✓       │     ✗      │   ✗  │
│  Change settings           │     ✓      │      ✗       │     ✗      │   ✗  │
│  View events               │     ✓      │      ✓       │     ✓      │   ✓  │
│  Create event              │     ✓      │      ✗       │     ✗      │   ✗  │
│  Edit event                │     ✓      │      ✓       │     ✗      │   ✗  │
│  Delete event              │     ✓      │      ✗       │     ✗      │   ✗  │
│  View reports              │     ✓      │      ✓       │     ✗      │   ✗  │
│  Export data               │     ✓      │      ✗       │     ✗      │   ✗  │
│                                                                               │
│  * = Only regular users (not admin, not other managers)                      │
└──────────────────────────────────────────────────────────────────────────────┘
"""

# ════════════════════════════════════════════════════════════════════════════
#                      CODE FLOW DIAGRAMS
# ════════════════════════════════════════════════════════════════════════════

CODE_FLOW = """
When User Visits Admin Panel:
═════════════════════════════════════════════════════════════════════════════

1. User lands on /admin/auth/user/
   ↓
2. Django calls: CustomUserAdmin.has_view_permission(request)
   ├─ If not staff → PermissionDenied ✗
   └─ If staff → Continue ✓
   ↓
3. Django calls: CustomUserAdmin.get_queryset(request)
   ├─ If request.user is admin:
   │  └─ return User.objects.all() [ALL USERS]
   │
   ├─ If request.user is manager:
   │  └─ return User.objects.filter(
   │        is_superuser=False, 
   │        groups__isnull=True
   │     ) [ONLY REGULAR USERS]
   │
   └─ If request.user is regular user:
      └─ return User.objects.none() [NO USERS]
   ↓
4. Users list displayed filtered


When Manager Tries to Edit Admin:
═════════════════════════════════════════════════════════════════════════════

1. Manager clicks "Edit" on admin user
   ↓
2. Django calls: CustomUserAdmin.has_change_permission(request, admin_obj)
   ├─ Check: is_admin_user(admin_obj) → True
   │  └─ Can only edit if request.user is admin
   │     └─ Manager is NOT admin
   │        └─ Return False → DENIED ✗
   └─ Access Denied: "You don't have permission to edit this object"


When Manager Tries to Delete Admin:
═════════════════════════════════════════════════════════════════════════════

1. Manager clicks "Delete" on admin user
   ↓
2. Django calls: CustomUserAdmin.has_delete_permission(request, admin_obj)
   ├─ Check: is_admin_user(admin_obj) → True
   │  └─ Can delete only if request.user is admin
   │     └─ Manager is NOT admin
   │        └─ Return False → DENIED ✗
   └─ Access Denied: "You don't have permission to delete this object"


Promoting User to Manager:
═════════════════════════════════════════════════════════════════════════════

1. Call: make_user_manager(user_obj)
   ↓
2. Internal steps:
   ├─ user.is_staff = True
   ├─ user.save()
   ├─ managers_group = Group.objects.get(name='managers')
   ├─ user.groups.add(managers_group)
   └─ User now has manager tier
   ↓
3. Verify: get_user_tier(user_obj)
   └─ Returns: 'manager'
"""

print(HIERARCHY)
print("\n" + "="*80 + "\n")
print(ADMIN_PANEL_VIEW)
print("\n" + "="*80 + "\n")
print(PERMISSION_MATRIX)
print("\n" + "="*80 + "\n")
print(CODE_FLOW)

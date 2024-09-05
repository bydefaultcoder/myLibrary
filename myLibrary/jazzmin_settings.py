ui_settings = {
    "site_title": "Studyground Libray Manager",
    "site_header": "SLM",
    "site_brand": "SLM 1.0",
    # "site_brand": "MyCoolApp 2.0",  # Custom version name in the footer
    "site_logo": "logo/pathshala.png",
    "version": "v1.0",  # Custom version name
    # for login
    "welcome_sign": "Welcome to the Pathshala Library Manager",

    # Samartech PVT LTD
    "copyright": "SAMARJEET SINGH GAUTAM",
     "user_avatar": 'avatar',
    "order_with_respect_to": [
        "booking.Location",
        "booking.Seat",
        'booking.MonthlyPlan',
        'booking.Student',
        'booking.Booking'
        'booking.Payment'
        ],

    # "language_chooser": True,
    "show_ui_builder" : True,
    "show_ui_builder":True,
    'custom_template': 'admin/jazzmin/base_site.html',
    "icons": {
        # "auth": "fas fa-users-cog",
        "customAdmin.customUser": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "booking.Location": "fas fa-building",
        "booking.Seat": "fas fa-sharp fa-solid fa-chair",
        # "booking.MonthlyPlan": "fas icon-suitcase",
        'booking.Student':"fas fa-user",
        "booking.Booking":"fas  fa-check",
        'booking.Payment':"fas fa-money-bill",
    },

    "usermenu_links": [
        #  {"name": "Django Documentation", "url": "https://docs.djangoproject.com/en/stable/", "new_window": True},
         {"name": "Profile", "url": "/admin/user-profile/", "new_window": False},
         {"name": "About us", "url": "/about-us", "new_window": False},
        # {"name": "Support", "url": "https://support.example.com", "new_window": True},
        # {"model":  "django.contrib.admin.models.LogEntry"},  # Links directly to the user model in the admin panel
        # {"model":  "customAdmin.CustomUser"},  # Links directly to the user model in the admin panel
        # {"name": "Documentation", "url": "https://docs.example.com", "new_window": True},
        # {"app": "myapp"},  # Links to a specific app's list view in the admin panel
    ],

}


ui_tweaks_setting = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-info navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-info",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "united",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}
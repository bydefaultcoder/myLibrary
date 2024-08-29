ui_settings = {
    "site_title": "StudySphere Libray Manager",
    "site_header": "StudySphere",
    "site_brand": "StudySphere",
    "site_logo": "booking/images/StudySpherenew.png",
    # "site_logo": "booking/images/logo2.png",
    # for login
    "welcome_sign": "Welcome to the StudySphere Library Manager",

    # Samartech PVT LTD
    "copyright": "Acme Library Ltd",
     "user_avatar": 'avatar',
    "order_with_respect_to": ["booking.Location","booking.Seat",'booking.MonthlyPlan','booking.Student','booking.Payment'],

    "language_chooser": True,
    "show_ui_builder" : True,
    "show_ui_builder":True,
    "usermenu_links": [
        {"name": "Profile", "url": "/admin/customer-profile", "new_window": True},
    ],

}


ui_tweaks_setting = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "solar",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

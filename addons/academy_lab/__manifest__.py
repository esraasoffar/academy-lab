{
    "name": "Academy Lab",
    "version": "18.0.1.0.0",
    "summary": "Training Academy Management System",
    "author": "Esraa",
    "category": "Education",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'security/academy_record_rules.xml',

        'views/academy_course_views.xml',
        'views/academy_enrollment_views.xml',
        'views/academy_category_views.xml',
        'views/academy_menu.xml',
    ],
    "installable": True,
    "application": True,
}
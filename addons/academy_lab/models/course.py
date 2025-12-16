from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcademyCourse(models.Model):
    _name = 'academy.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Training Course'

    # Fields
    name = fields.Char(
        string="Course Name",
        required=True,
        tracking=True
    )

    code = fields.Char(
        string="Course Code",
        required=True,
        index=True
    )

    description = fields.Text(string="Course Description")
    duration_hours = fields.Float(string="Number of Hours")
    price = fields.Float(string="Price")

    max_students = fields.Integer(default=20)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        tracking=True
    )

    start_date = fields.Date(tracking=True)
    end_date = fields.Date(tracking=True)

    category_id = fields.Many2one('academy.course.category', string='Category')
    instructor_id = fields.Many2one('res.partner', string='Instructor')
    enrollment_ids = fields.One2many(
        'academy.enrollment',
        'course_id',
        string='Enrollments'
    )

    enrolled_count = fields.Integer(
        compute='_compute_enrolled_count',
        store=True
    )

    available_seats = fields.Integer(
        compute='_compute_available_seats',
        store=True
    )

    is_full = fields.Boolean(
        compute='_compute_is_full',
        store=True
    )

    instructor_name = fields.Char(
        related='instructor_id.name',
        store=True
    )

    # =====================
    # Compute
    # =====================
    @api.depends('enrollment_ids.state')
    def _compute_enrolled_count(self):
        for course in self:
            course.enrolled_count = len(
                course.enrollment_ids.filtered(
                    lambda e: e.state == 'confirmed'
                )
            )

    @api.depends('max_students', 'enrolled_count')
    def _compute_available_seats(self):
        for course in self:
            course.available_seats = (
                course.max_students - course.enrolled_count
            )

    @api.depends('available_seats')
    def _compute_is_full(self):
        for course in self:
            course.is_full = course.available_seats <= 0

    # =====================
    # Constraints
    # =====================
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError(
                        "End date must be after start date."
                    )

    @api.constrains('max_students')
    def _check_max_students(self):
        for record in self:
            if record.max_students <= 0:
                raise ValidationError(
                    "Max students must be greater than zero."
                )

    _sql_constraints = [
        (
            'unique_course_code',
            'unique(code)',
            'Course code must be unique.'
        )
    ]

    # =====================
    # Overrides
    # =====================
    @api.model
    def create(self, vals):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super().create(vals)

    def write(self, vals):
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super().write(vals)

    # =====================
    # Actions (Workflow)
    # =====================
    def action_publish(self):
        for record in self:
            if not record.instructor_id:
                raise ValidationError(
                    "Instructor is required before publishing."
                )
            record.state = 'published'

    def action_start(self):
        for record in self:
            record.state = 'in_progress'

    def action_complete(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

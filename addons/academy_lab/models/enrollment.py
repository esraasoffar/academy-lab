from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcademyEnrollment(models.Model):
    _name = 'academy.enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Academy Enrollment'

    # Fields
    student_id = fields.Many2one('res.partner', string='Student', required=True)
    course_id = fields.Many2one('academy.course', string='Course', required=True)

    enrollment_date = fields.Date(
        string='Enrollment Date',
        default=fields.Date.today
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed'),
        ],
        default='draft'
    )

    grade = fields.Float(string='Grade')
    attendance_percentage = fields.Float(string='Attendance Percentage', tracking=True)
    notes = fields.Text(string='Notes')

    # Computed / Related Fields
    student_name = fields.Char(
        related='student_id.name',
        store=True
    )

    course_name = fields.Char(
        related='course_id.name',
        store=True
    )

    passed = fields.Boolean(
        string='Passed',
        compute='_compute_passed',
        store=True
    )

    @api.depends('grade', 'attendance_percentage')
    def _compute_passed(self):
        for record in self:
            record.passed = (
                record.grade >= 60 and
                record.attendance_percentage >= 75
            )


    # Constraints
    _sql_constraints = [
        (
            'unique_student_course',
            'unique(student_id, course_id)',
            'Student already enrolled in this course'
        )
    ]

    # Methods to change state
    def action_confirm(self):
        for record in self:
            if record.course_id.is_full:
                raise ValidationError(
                    "This course is already full."
                )
            record.state = 'confirmed'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_complete(self):
        for record in self:
            record.state = 'completed'
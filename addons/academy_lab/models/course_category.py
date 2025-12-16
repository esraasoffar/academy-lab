from odoo import models, fields, api


class AcademyCourseCategory(models.Model):
    _name = 'academy.course.category'
    _description = 'Course Category'

    name = fields.Char(
        string='Category Name',
        required=True
    )

    description = fields.Text(string='Description')

    course_ids = fields.One2many(
        'academy.course',
        'category_id',
        string='Courses'
    )

    course_count = fields.Integer(
        string='Courses Count',
        compute='_compute_course_count',
        store=True
    )

    @api.depends('course_ids')
    def _compute_course_count(self):
        for record in self:
            record.course_count = len(record.course_ids)

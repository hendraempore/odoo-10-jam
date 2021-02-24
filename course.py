from odoo import api, fields, models

class Course(models.Model):
	_name = "academic.course"

	name = fields.Char(
		"Name",
		required=True,
	)

	description = fields.Text("Description")

	responsible_id = fields.Many2one(
		comodel_name="res.users",
		string="Responsible",
		required=True,
	)

	session_ids = fields.One2many(
		comodel_name="academic.session",
		string="Sessions",
		inverse_name="course_id",
	)

	_sql_constraints = [
		('sql_cek_name','UNIQUE(name)','Nama tidak boleh sama!'),
		('sql_cek_desc','CHECK(name <> description)','Name dan Description tidak boleh sama!')
	]
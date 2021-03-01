from odoo import api, fields, models
from openerp.exceptions import ValidationError
import time, logging

_logger = logging.getLogger(__name__)

STATES = [
	('draft','Draft'),
	('confirm','Confirm'),
	('done','Done'),
]

class Session(models.Model):
	_name = "academic.session"

	# def cari_tanggal(self):
	# 	return time.strftime("%Y-%m-%d")

	name = fields.Char(
		"Name",
		required=True,
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	course_id = fields.Many2one(
		comodel_name="academic.course",
		string="Course",
		required=True,
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	instructor_id = fields.Many2one(
		comodel_name="res.partner",
		string="Instructor",
		required=True,
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	start_date = fields.Date(
		string="Start Date",
		required=False,
		# default=cari_tanggal,
		default=lambda self: time.strftime("%Y-%m-%d"),
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	duration = fields.Integer(
		string="Duration",
		required=False,
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	seats = fields.Integer(
		string="Seats",
		required=False,
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	active = fields.Boolean(
		string="Active",
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	attendee_ids = fields.One2many(
		comodel_name="academic.attendee",
		string="Attendees",
		inverse_name="session_id",
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	taken_seats = fields.Float(
		string="Taken Seats",
		compute="_compute_taken_seats",
		readonly=True
	)

	image_small = fields.Binary(
		string="Image",
		readonly=True,
		states={'draft' : [('readonly',False)]},
	)

	state = fields.Selection(
		string="State",
		selection=STATES,
		readonly=True,
		required=True,
		default=STATES[0][0],
	)

	def _compute_taken_seats(self):
		for x in self:
			x.hitung()

	@api.onchange('seats')
	def onchange_seats(self):
		self.hitung()

	def hitung(self):
		if self.seats > 0:
			self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats
		else:
			self.taken_seats = 0.0

	# # @api.multi
	# def cek_instruktur(self):
	# 	for session in self:
	# 		# x = []
	# 		# for attendee in session.attendee_ids:
	# 		# 	x.append(attendee.partner_id.id)
	# 		x = [att.partner_id.id for att in session.attendee_ids]
	# 		if session.instructor_id.id in x:
	# 			return False
	# 	return True

	# _constraints = [(cek_instruktur, 'Instruktur tidak boleh merangkap sebagai attendee', ['instructor_id','attendee_ids'])]

	@api.constrains('instructor_id','attendee_ids')
	def _cek_instruktur(self):
		for session in self:
			x = [att.partner_id.id for att in session.attendee_ids]
			if session.instructor_id.id in x:
				raise ValidationError('Instruktur tidak boleh merangkap sebagai attendee')

	# @api.multi
	def copy(self, default=None):
		default = dict(default or {}, name=self.name + " (copy)")
		# print "*********************************************"
		# print default
		# print "*********************************************"
		_logger.info(default)
		return super(Session, self).copy(default=default)

	# @api.multi
	def action_confirm(self):
		self.state = STATES[1][0]

	# @api.multi
	def action_done(self):
		self.state = STATES[2][0]

	# @api.multi
	def action_draft(self):
		self.state = STATES[0][0]
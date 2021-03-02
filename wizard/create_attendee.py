from odoo import api, fields, models

class AttendeeWizard(models.TransientModel):
	_name = "academic.attendee.wizard"

	def _get_default_session(self):
		context = self.env.context
		if context.get('active_model') == 'academic.session':
			return context.get('active_ids', False)
		return False

	# session_id = fields.Many2one(
	# 	comodel_name="academic.session",
	# 	string="Session",
	# 	default=_get_default_session
	# )

	session_ids = fields.Many2many(
		comodel_name="academic.session",
		string="Sessions",
		default=_get_default_session
	)

	attendee_ids = fields.One2many(
		comodel_name="academic.attendee.wizard.partner",
		inverse_name="wizard_id",
		string="Partners to Add",
	)

	def action_add_attendee(self):

		# import pdb; pdb.set_trace()

		self.ensure_one()
		session_ids = self.session_ids

		for session_id in session_ids:
			session_id.attendee_ids = [
				(0,0,{'name':'001', 'partner_id':x.partner_id.id}) for x in self.attendee_ids
			]

		return {'type': 'ir.actions.act_window_close'}

class AttendeePartner(models.TransientModel):
	_name = 'academic.attendee.wizard.partner'

	wizard_id = fields.Many2one(
		comodel_name = "academic.attendee.wizard",
		string="Wizard",
	)

	partner_id = fields.Many2one(
		comodel_name="res.partner",
		string="Partner to add",
	)
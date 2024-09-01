import frappe
from frappe.utils import nowdate

def update_user_status():
    expired_fees_collections = get_expired_fees_collections
    for fee in expired_fees_collections:
        gym_member = frappe.get_doc('Gym Member', fee.member_id)
        user = gym_member.user_id

        if user:
            user_doc = frappe.get_doc('User', user)
            if user_doc.enabled != 0:
                user_doc.enabled = 0
                user_doc.save()
                frappe.db.commit()

        frappe.db.set_value('Fees Collection', fee.name, 'status', 'Inactive')

def get_expired_fees_collections():
    today = nowdate()
    expired_fees_collections = frappe.get_all('Fees Collection', filters={
        'to_date': ['=', today],
        'status': 'Active'
    }, fields=['name', 'member_id'])

    return expired_fees_collections

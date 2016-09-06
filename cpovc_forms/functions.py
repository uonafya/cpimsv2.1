from cpovc_registry.functions import get_client_ip, get_meta_data
from cpovc_forms.models import (FormsAuditTrail)

def save_audit_trail(request, params, audit_type):
    """Method to save audit trail depending on transaction."""
    try:
        user_id = request.user.id
        ip_address = get_client_ip(request)
        form_id = params['form_id']
        form_type_id = audit_type
        transaction_type_id = params['transaction_type_id']
        interface_id = params['interface_id']
        meta_data = get_meta_data(request)

        print 'Audit Trail', params

        FormsAuditTrail(
                transaction_type_id=transaction_type_id,
                interface_id=interface_id,
                # timestamp_modified=None,
                form_id=form_id,
                form_type_id=form_type_id,
                ip_address=ip_address,
                meta_data=meta_data,
                app_user_id=user_id).save()

    except Exception, e:
        print 'Error saving audit - %s' % (str(e))
        pass
    else:
        pass
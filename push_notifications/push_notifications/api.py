import frappe
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request


@frappe.whitelist(allow_guest=False, methods=['GET', 'POST'])
def send_push_notification(user=None, subject=None, body=None, doctype=None, docname=None):
    """
    Send push notification to user's mobile device
    Accepts data from both URL parameters and POST body
    
    Args:
        user: ERPNext username to send notification to
        subject: Notification title
        body: Notification message
        doctype: Optional - source doctype
        docname: Optional - source document name
    """
    
    # Get from URL params or POST data (frappe.form_dict handles both)
    user = user or frappe.form_dict.get('user')
    subject = subject or frappe.form_dict.get('subject')
    body = body or frappe.form_dict.get('body')
    doctype = doctype or frappe.form_dict.get('doctype')
    docname = docname or frappe.form_dict.get('docname')
    
    # Validate required parameters
    if not user:
        return {"success": False, "message": "User parameter required"}
    
    try:
        # Get Firebase config
        firebase_config = frappe.get_single("Firebase Config")
        
        if not firebase_config.enabled:
            return {"success": False, "message": "Firebase disabled"}
        
        # Get user's FCM token from Mobile Device
        devices = frappe.get_all(
            "Mobile Device",
            filters={"user": user},
            fields=["fcm_token"],
            limit=1
        )
        
        if not devices or not devices[0].get("fcm_token"):
            return {"success": False, "message": "No FCM token found for user"}
        
        fcm_token = devices[0]["fcm_token"]
        
        # Parse service account JSON
        service_account_info = json.loads(firebase_config.service_account_json)
        project_id = firebase_config.project_id
        
        # Get OAuth access token
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/firebase.messaging']
        )
        credentials.refresh(Request())
        access_token = credentials.token
        
        # Prepare Firebase payload
        firebase_url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
        
        payload = {
            "message": {
                "token": fcm_token,
                "notification": {
                    "title": subject[:100] if subject else "ERPNext Notification",
                    "body": body[:100] if body else "New notification"
                },
                "data": {
                    "doctype": doctype or "",
                    "docname": docname or "",
                },
                "android": {
                    "priority": "high",
                    "notification": {
                        "channel_id": "high_importance_channel",
                        "sound": "default"
                    }
                }
            }
        }
        
        # Send to Firebase
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            firebase_url,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            frappe.logger().info(f"✅ Push notification sent to {user}")
            return {"success": True, "message": "Notification sent"}
        else:
            error_msg = f"Firebase error: {response.status_code} - {response.text}"
            frappe.log_error(error_msg, "Push Notification Error")
            return {"success": False, "message": error_msg}
            
    except Exception as e:
        error_msg = f"Error sending push notification: {str(e)}"
        frappe.log_error(error_msg, "Push Notification Error")
        return {"success": False, "message": error_msg}

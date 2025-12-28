# Push Notifications

Firebase Cloud Messaging push notifications for ERPNext custom mobile apps.

## Installation

1. Add this app to your Frappe Cloud site
2. Install the app from App Installer
3. Configure Firebase Config doctype with your Firebase credentials
4. Create Server Script to call the API when notifications are created

## Usage

### From Server Script

```python
def execute(doc, method):
    send_push = frappe.get_attr("push_notifications.push_notifications.api.send_push_notification")
    
    send_push(
        user=doc.for_user,
        subject=doc.subject,
        body=doc.message or doc.subject
    )
```

### Server Script Setup

1. Go to Server Script List
2. Create new Server Script:
   - Script Type: DocType Event
   - DocType: Notification Log
   - Event: After Insert
3. Add the code above
4. Save and enable

## Requirements

- Firebase project with Cloud Messaging enabled
- Firebase Config doctype configured in ERPNext
- Mobile Device doctype with user FCM tokens

## License

MIT

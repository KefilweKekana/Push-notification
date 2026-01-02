from . import __version__ as app_version

app_name = "push_notifications"
app_title = "Push Notifications"
app_publisher = "OctaNode"
app_description = "Firebase Push Notifications for ERPNext"
app_email = "kefilwe@octanode.co.za"
app_license = "MIT"

# Document Events - automatically send push notifications
doc_events = {
    "Notification Log": {
        "after_insert": "push_notifications.push_notifications.api.send_notification_on_insert"
    }
}

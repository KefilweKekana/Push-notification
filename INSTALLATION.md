# Installation Instructions for Push Notifications App

## Folder Structure

The correct structure is:
```
push_notifications/                  (root folder)
├── setup.py
├── requirements.txt
├── MANIFEST.in
├── README.md
├── .gitignore
└── push_notifications/              (inner folder - the Python package)
    ├── __init__.py
    ├── hooks.py                     ← MUST BE HERE
    ├── patches.txt                  ← MUST BE HERE
    ├── modules.txt
    └── push_notifications/          (sub-module for code)
        ├── __init__.py
        └── api.py
```

## Step 1: Upload to GitHub

1. **Create a new GitHub repository**
   - Go to https://github.com/new
   - Repository name: `push_notifications`
   - Description: `Firebase Push Notifications for ERPNext`
   - Public or Private: Your choice
   - Click "Create repository"

2. **Upload files to GitHub**
   - Extract the `push_notifications` folder
   - Open terminal/command prompt
   - Navigate to the folder:
     ```bash
     cd path/to/push_notifications
     ```
   - Initialize git and push:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/push_notifications.git
     git push -u origin main
     ```

   **OR use GitHub Desktop (easier):**
   - Extract the folder
   - Open GitHub Desktop
   - File → Add Local Repository
   - Select the `push_notifications` folder
   - Publish repository

## Step 2: Install on Frappe Cloud

1. **Login to Frappe Cloud**
   - Go to https://frappecloud.com/
   - Login to your account

2. **Go to your site**
   - Click on your site (e.g., octatest.jh.frappe.cloud)

3. **Add the app**
   - Click "Apps" in the left sidebar
   - Click "Add App" button
   - Enter GitHub repository URL:
     ```
     https://github.com/YOUR_USERNAME/push_notifications
     ```
   - Click "Add App"
   - Wait for app to be added (takes 1-2 minutes)

4. **Install the app**
   - Once app is added, click "Install" button next to it
   - Confirm installation
   - Wait for installation to complete (takes 2-3 minutes)

## Step 3: Create Server Script

1. **In ERPNext**, search: `Server Script`

2. **Click "New"**

3. **Fill in:**
   - Script Name: `Send Push Notification`
   - Script Type: `DocType Event`
   - DocType: `Notification Log`
   - Event: `After Insert`
   - Disabled: ☐ (UNCHECKED)

4. **Script:**
   ```python
   def execute(doc, method):
       # Only send if notification is for a user
       if not doc.for_user:
           return
       
       # Call the custom app method
       send_push = frappe.get_attr("push_notifications.push_notifications.api.send_push_notification")
       
       send_push(
           user=doc.for_user,
           subject=doc.subject,
           body=doc.message or doc.subject or "New notification"
       )
   ```

5. **Click "Save"**

## Step 4: Test

1. **Make sure:**
   - Firebase Config is configured with your credentials
   - Mobile Device has FCM token for your user
   - ERPFlow app is installed on phone and logged in

2. **Create a test notification:**
   - Create a ToDo and assign to yourself
   - OR mention yourself in a comment

3. **Check your phone** - notification should appear! 🔔

## Troubleshooting

**App installation fails:**
- Check GitHub repository is public or Frappe Cloud has access
- Verify hooks.py exists in `push_notifications/push_notifications/hooks.py`
- Verify patches.txt exists in `push_notifications/push_notifications/patches.txt`

**Notifications not sending:**
- Check Error Log in ERPNext for errors
- Verify Firebase Config is enabled
- Verify Mobile Device has FCM token
- Check Server Script is enabled (Disabled checkbox is UNCHECKED)
- Look for errors with title "Push Notification Error"

**Need help?**
- Check Error Log in ERPNext
- The custom app logs errors with title "Push Notification Error"

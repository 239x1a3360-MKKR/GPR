# Admin Panel: Delete User Guide

## Overview

The admin panel now includes delete functionality for users with safety checks and warnings to prevent accidental deletions.

## How to Delete Users

### Single User Deletion

1. **Navigate to Users**: Go to Admin Panel → Users
2. **Select User**: Click on the username you want to delete
3. **Delete**: Scroll to the bottom and click the red "Delete" button
4. **Confirm**: Confirm the deletion on the confirmation page

### Bulk User Deletion

1. **Navigate to Users**: Go to Admin Panel → Users
2. **Select Users**: Check the boxes next to the users you want to delete
3. **Choose Action**: Select "Delete selected users" from the "Action" dropdown
4. **Execute**: Click "Go" button
5. **Confirm**: Confirm the deletion

## Safety Features

### Protection Against Accidental Deletion

The system includes several safety checks:

1. **Self-Deletion Prevention**: 
   - You cannot delete your own account
   - Error message: "You cannot delete your own account."

2. **Superuser Protection**:
   - Only superusers can delete other superusers
   - Regular admins cannot delete superuser accounts
   - Error message: "You cannot delete superuser accounts."

3. **Admin Profile Protection**:
   - Only superusers can delete admin profiles
   - Regular admins cannot delete admin profiles
   - Error message: "You cannot delete admin profiles."

4. **Data Warning**:
   - System warns about related data (submissions) that will be deleted
   - Warning: "Deleting user 'username' will also delete X submission(s)."

## What Gets Deleted

When you delete a user:

- ✅ User account is deleted
- ✅ UserProfile is deleted (cascade)
- ✅ All submissions by that user are deleted (cascade)
- ✅ All related data is removed

## Delete UserProfile

You can also delete user profiles separately:

1. **Navigate to User Profiles**: Go to Admin Panel → User profiles
2. **Select Profile**: Click on the profile or select multiple
3. **Delete**: Use the delete button or bulk delete action

**Note**: Deleting a UserProfile will also delete the associated User account due to CASCADE relationship.

## Best Practices

1. **Review Before Deleting**: Check user's submission count before deletion
2. **Backup Important Data**: If needed, export user data before deletion
3. **Use Bulk Delete Carefully**: Double-check selected users before confirming
4. **Verify Permissions**: Ensure you have proper permissions before attempting deletion

## Error Messages

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| "You cannot delete your own account." | Trying to delete yourself | Select a different user |
| "You cannot delete superuser accounts." | Trying to delete superuser as non-superuser | Only superusers can delete superusers |
| "You cannot delete admin profiles." | Trying to delete admin profile as non-superuser | Only superusers can delete admin profiles |

## Troubleshooting

### Delete Button Not Showing

- Check that you have proper admin permissions
- Ensure you're logged in as admin or superuser
- Refresh the page

### Cannot Delete User

- Check if you're trying to delete yourself
- Verify user is not a superuser (if you're not superuser)
- Check for any error messages displayed

### Related Data Concerns

- Submissions are automatically deleted when user is deleted (CASCADE)
- This is by design to maintain data integrity
- Consider exporting data before deletion if needed

## Security Notes

- Deletion is permanent and cannot be undone
- Always verify the user before deletion
- Use bulk delete with caution
- Keep backups of important data


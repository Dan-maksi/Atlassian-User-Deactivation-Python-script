# Atlassian_User_Automation
An Atlassian automation app, which runs in a gitlabs pipeline which deactivates inactive users after a set amount of days and post a notification into a given slack channel, with the deleted users, last active date, email and pipeline id.

These are enviorment variablies assigned in the git pipeline which are needed for the app to run:

days_threshold: is the number of days that a given user is allowed to be inactive

dry_run: Dry_run allows you to run the app without deactivating an users, but it still outputs what users would have been deleted. (Good for testing)

token: Is the Orginization Admin API token needed to make apis calls. (https://support.atlassian.com/organization-administration/docs/manage-an-organization-with-the-admin-apis/)

orgId: Is your orginization id (https://confluence.atlassian.com/jirakb/what-it-is-the-organization-id-and-where-to-find-it-1207189876.html)

organization: is the name of the orginization, example: https://example-org.atlassian.net/

email: Admins email which will be used to make API calls (this app uses 2 versions of API calls and both need diffrent authentication methods one email and assosiated token, one Admin API key)

basicauth = Key assosiated with email (https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)

gitlab_pipeline_url = URL of pipeline used to run script

slack_channel = Stack channel where you want notification posted

slack_token = Asosiated Stack API key

exceptions: is list of Emails that you would like the script to ignore

NOTE: The script cannot deactivate users from a diffrent orginization that you may have invited to yours. Because the deactivate API call only requires Admin token and user id,
it cannot tell if you are trying to remove them from yours or from the origin one, since the account id is the same across orginizations.


# Atlassian User Automation

Atlassian User Automation is an automation app for Atlassian that runs in a GitLab pipeline. The app deactivates inactive users after a set amount of days and posts a notification with the deleted users, their last active date, email, and pipeline ID to a specified Slack channel.

## Environment Variables

The following environment variables must be assigned in the Git pipeline for the app to run:

- `days_threshold`: the number of days a user is allowed to be inactive before being deactivated.
- `dry_run`: allows running the app without deactivating users, but still outputs what users would have been deleted, good for testing.
- `token`: the organization admin API token required for making API calls. [Learn more about admin APIs](https://support.atlassian.com/organization-administration/docs/manage-an-organization-with-the-admin-apis/).
- `orgId`: the organization ID. [Learn where to find it](https://confluence.atlassian.com/jirakb/what-it-is-the-organization-id-and-where-to-find-it-1207189876.html).
- `organization`: the name of the organization (e.g. https://example-org.atlassian.net/).
- `email`: the admin's email used to make API calls. The app uses two versions of API calls, each with different authentication methods: one email and associated token, and one admin API key.
- `basicauth`: the key associated with the email. [Learn how to manage API tokens](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).
- `gitlab_pipeline_url`: the URL of the pipeline used to run the script (used in Slack notifications).
- `slack_channel`: the Slack channel where the notification should be posted.
- `slack_token`: the associated Slack API key.
- `exceptions`: a list of emails that the script should ignore.

Note that the script cannot deactivate users from a different organization that you may have invited to yours. This is because the deactivate API call only requires the admin token and user ID, which cannot tell if you are trying to remove them from your organization or from the original one, as the account ID is the same across organizations.

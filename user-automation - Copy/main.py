import os, requests, json
from requests.auth import HTTPBasicAuth
from datetime import datetime, date
from slack_sdk import WebClient

today = datetime.today()
deactivated_user = []
days_threshold = int(os.environ.get('DAYS_THRESHOLD'))
dry_run = os.environ.get('DRY_RUN', 'True').lower() == 'true'
token = os.environ.get('TOKEN')
orgId = os.environ.get('ORGANIZATION_ID')
organization = "wcloud"
email = os.environ.get("EMAIL")
basicauth = os.environ.get("EMAIL_TOKEN")
gitlab_pipeline_url = os.environ.get('CI_PIPELINE_URL')
slack_channel = str(os.environ.get('SLACK_CHANNEL'))
slack_token = os.environ.get('SLACK_TOKEN')
authentication = HTTPBasicAuth(email, basicauth)
exceptions = []
base_url = "https://api.atlassian.com/"
base_admin_url = base_url + "admin/v1/orgs/"
base_users_url = base_url + "users/"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": token
}


def get_user():
    url = f"https://{organization}.atlassian.net/rest/api/3/users"

    auth = authentication

    headers = {
        "Accept": "application/json"
    }

    query = {
        'maxResults': '1000',
        'startAt': "0"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    return json.loads(response.text)


def make_checks(accounts):
    act_users = 0
    for user in accounts:
        if user["active"] is True and user["accountType"] == "atlassian" and user.get('emailAddress') not in exceptions and user['displayName'] not in exceptions:
            act_users = act_users + 1
            last_active = get_last_active(user["accountId"])
            if last_active == "Never Accessed":
                pass
            elif is_older_than_30_days(last_active) is True:
                deactivate(user, last_active)
                pass
    print(act_users)


def get_last_active(accountid):
    datestocomp = []
    url = f"https://api.atlassian.com/admin/v1/orgs/{orgId}/directory/users/{accountid}/last-active-dates"
    headers = {
        "Accept": "application/json",
        "Authorization": token
    }

    response = requests.request(
        "GET",
        url,
        headers=headers
    )

    for user in json.loads(response.text)["data"]["product_access"]:
        try:
            datestocomp.append(user["last_active"])
        except:
            pass
    if len(datestocomp) == 1:
        return datestocomp[0]
    elif len(datestocomp) == 2:
        return get_newest_date(datestocomp)
    else:
        return "Never Accessed"


def get_newest_date(dates):
    date1 = datetime.strptime(dates[0], '%Y-%m-%d')
    date2 = datetime.strptime(dates[1], '%Y-%m-%d')

    if date1 > date2:
        return dates[0]
    else:
        return dates[1]


def is_older_than_30_days(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    delta = today - date_obj
    if delta.days > days_threshold:
        return True
    else:
        return False


def deactivate(user, lastactive):
    url = base_users_url + user["accountId"] + "/manage/lifecycle/disable"
    payload = json.dumps({
        "message": "Deactivated inactive user"
    })

    if dry_run:
        deactivated_user.append(f"({user['displayName']}, {user.get('emailAddress')}, {lastactive})")

    else:
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers
        )
        deactivated_user.append(f"({user['displayName']}, {user.get('emailAddress')}, {lastactive})")
        print(response.text)


def results():
    list = "\n".join(deactivated_user)
    default = "No inactive users found."
    message = ""
    if len(list) == 0:
        message = default
    else:
        message = list

    slack_client = WebClient(token=slack_token)
    slack_message = f'Atlassian deactivate users <{gitlab_pipeline_url}|pipeline> result:'"\n" + message

    slack_client.chat_postMessage(text=slack_message, channel=slack_channel)



make_checks(get_user())
results()





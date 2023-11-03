from thotnr_ml_client import MLModel
import requests


def test():
    url = 'https://zs-ae-dev.icops.dev.zsservices.com/datatypes/zpsa_265_1024_2179/app-api/graphql?dagContextId=8285&versionTagId=10990'

    headers = {
        'authority': 'zs-ae-dev.icops.dev.zsservices.com',
        'accept': 'application/json',
        'accept-language': 'en,ar;q=0.9',
        'authorization': 'Bearer eyJraWQiOiJ0RlZ4UndEU0R4WXZaeFUxNlV4WFwvZEE4QWhlbXM5aFdEdnBobUVPeWdwQT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3YjFhMjUyZC1jNDlhLTQzNzItYTk0Ny1lYzY3NTkzZTk3ZWYiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9DWEJMRTBxVlYiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiIyM2JhOXI2NDJxc2kwM2RocjMzZm5uNG9mMSIsIm9yaWdpbl9qdGkiOiI5OGFkMjYzOS1lOGIyLTQxNDctYmFhYi0yMTJkMmZkNzcyNDgiLCJldmVudF9pZCI6IjE5YTVhNDdiLTZkOWItNGNiYi04NjQyLWU2MjEyNzUwZTMzOSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNjk4ODk4MzAxLCJleHAiOjE2OTg5MDU1MjYsImlhdCI6MTY5ODkwMTkyNiwianRpIjoiYWRiZjM5NDctMzQzNC00MzBjLWIyY2MtNWU2ZjQ0Y2Q2NmFmIiwidXNlcm5hbWUiOiJTYW5rZXQifQ.D-m7mstT4U2eWHSFgYvcJNBHhOScj8dHRbis6d3YiWJwbWOkIX1aLQ1GWhZ6RfM2GRwyioSRRIVVgu26h50dSS-ujarfty5lOD-UxaCcB7PnXAJVq3ebMt0eoOreRcCjIWndLAp6nCu3GLrUnQ_Fs7IZlpactIGm1ledpc7Bsn8OVIam4EwOe0m8bAt4QMA0FP8eSNDOHGf_Slo8X-Z682DgdiryRvpW5aLfLnhctRg8fkn5RdbhYNpfcdLdL7-7bQsZwZupH8e1ay-kSKLK7TAbW8gu_EKrCokd4WEYJ-zO0u2a8HtGvsj0IjXYcIaMWxElqYT5MK7IUBbL_a_9_g',
        'bitemporalprops': '{"default":{"as_of_ts":"now","valid_ts":"now"}}',
        'content-type': 'application/json; charset=utf-8',
        'cookie': 'auth="Bearer eyJraWQiOiJ0RlZ4UndEU0R4WXZaeFUxNlV4WFwvZEE4QWhlbXM5aFdEdnBobUVPeWdwQT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI3YjFhMjU2ZC1jNDlhLTQzNzItYTk0Ny1e',
        'graphqloptype': 'query',
        'origin': 'https://zs-ae-dev.icops.dev.zsservices.com',
        'referer': 'https://zs-ae-dev.icops.dev.zsservices.com/apps/zpsa_265_1024_2179/instance/object/8487',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'uacacheid': '41809',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'userid': '2674'
    }

    data = {
        "query": 'query MyQuery {\n  MlModel1486_api(condition: null,\n  first: 11,\n  offset: 0,\n  orderBy: modified_on_desc,\n  ) {\n    edges {\n      node {\n        MlModel1486_id,is_deleted,created_by,modified_by,created_on,modified_on,mlCode,s3Path,isActive,groupId,modelMetadata\n      }\n      cursor\n    }\n  }\n}    \n'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")



if __name__ == '__main__':
    ml_model = MLModel()
    print(ml_model.get_current_active_model())
    # test()



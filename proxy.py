from mitmproxy import http
import json

def request(flow):
    if "content-type" not in flow.request.headers:
        return
    if "application/json" in flow.request.headers["content-type"] or "text/plain" in flow.request.headers["content-type"]:
        slack_json = json.loads(flow.request.text, strict=False)
        if "blocks" in slack_json:
            slack_text = ""
            if len(slack_json['blocks']) > 1:
                for block in slack_json['blocks']:
                    if "text" in block:
                        slack_text += block['text']['text']
                    elif "fields" in block:
                        for field in block['fields']:
                            slack_text += "\n" + field['text']
            mattermost_json = '{"text": "' + slack_text + '"}'
        else:
            mattermost_json = slack_json

        flow.request.text = mattermost_json

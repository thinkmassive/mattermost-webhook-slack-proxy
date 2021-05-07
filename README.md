A simple Docker image that uses [mitmproxy](https://mitmproxy.org/) to convert Slack "blocks" webhook payloads to the legacy format. This is useful for sending [webhooks to Mattermost](https://docs.mattermost.com/developer/webhooks-incoming.html), which [doesn't yet support the new format](https://mattermost.atlassian.net/browse/MM-26729).

Messages are still susceptible to the limitations described in the Mattermost docs about [Slack Compatibility](https://docs.mattermost.com/developer/webhooks-incoming.html#slack-compatibility).

# Quickstart

Point the webhook source to the proxy port (18080 in this example) and set `proxy_dest` to the Mattermost host (including protocol & port).

```bash
docker run \
    -p 18080:8080 \
    -e proxy_dest=http://mattermost:8065/
    thinkmassive/mattermost-webhook-slack-proxy
```

Test the connection using `curl`:

```bash
MM_HOST=http://localhost:18080
MM_SECRET=REPLACE_WITH_YOUR_WEBHOOK_SECRET

curl -i -X POST -H 'Content-Type: application/json' \
  -d '{"blocks": [{"text": {"text": "Hello :tada:"}}]}' \
  $MM_HOST/hooks/$MM_SECRET
```

If you run the proxy in an ad-hoc container, you may want to attach it to an existing docker-compose network with the `--network` parameter. Then your other compose hosts can refer to it by its alias, which can be found using `docker inspect` on the ad-hoc container.

# Docker Compose

```bash
  mattermost:
    image: mattermost/mattermost-preview:latest
    ports:
      - 8065:8065

  mattermost-proxy:
    image: thinkmassive/mattermost-webhook-slack-proxy:latest
    environment:
      - listen_port=8080
      - proxy_dest=http://mattermost:8065
    ports:
      - 8080:8080
```

# Kubernetes

I will add a kubernetes manifest soon.

---

# Development Notes

This initial implementation is extremely simple. It rewrites the payload as a single `text` field with the contents of `blocks[0][text][text]`.

The Slack "blocks" message looks like this:
```json
{"blocks": [{
  "text": {
    "text": "This is where your chat message goes"
  }
}]}
```

The legacy message looks like this:
```json
{"text": "This is where your chat message goes"}
```  

# Interactive Use

You can change the entrypoint to experiment with `mitmproxy` and run it in interactive mode.

```bash
docker run -it --entrypoint /bin/sh \
    -p 18080:8080 \
    thinkmassive/mattermost-webhook-slack-proxy
```

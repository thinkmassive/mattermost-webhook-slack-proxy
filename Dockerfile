FROM mitmproxy/mitmproxy

ENV listen_port=8080
ENV proxy_dest=http://mattermost:8065/

COPY proxy.py /

CMD ["/bin/sh", "-c", "mitmdump -p ${listen_port} -m reverse:${proxy_dest} -s /proxy.py"]

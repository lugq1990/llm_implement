## Log monitor and log discovery

This is based on `ES` and `Kibana` to implement log monitor and data discovery.


### elasticsearch

```shell
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.8.1
docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.8.1
```

#### information:
- password: `Benk38BLTx8XjuySmdJ_`
- kibana enrollment token:  `eyJ2ZXIiOiI4LjguMSIsImFkciI6WyIxNzIuMjAuMC4yOjkyMDAiXSwiZmdyIjoiNGE3NTg2YmM3MjRkMDM5ODU2ZTAwODE5MGJjMGU3NGViNTYyMmFiZDk2NDRjM2NmMTVlYjVkMmZmY2M4MzZjMCIsImtleSI6IlZvR0szSWdCaV9kM05pN1kwQXRQOlBDLURjMGhKUlpTazljSWNQXzhKR0EifQ==`


### Kibana

```shell
docker pull docker.elastic.co/kibana/kibana:8.8.1
docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.8.1
```

Start kibana: 
1. login `http://0.0.0.0:5601/?code=001702`
2. fillin enrollment token
3. username: `elastic`, password: `zTXhS6p+Xo*fXs63s+YH`


### elastic agent
- [how to create elastic agent](https://www.elastic.co/guide/en/fleet/current/elastic-agent-container.html)
```shell
docker pull docker.elastic.co/beats/elastic-agent:8.8.1
docker run --env FLEET_SERVER_ENABLE=true --env FLEET_SERVER_ELASTICSEARCH_HOST=localhost:9200 --env FLEET_SERVER_SERVICE_TOKEN=dWxSODNJZ0JVZTdZU21zVXloVHo6QTd3RGtWODlRTWVQV2ZraDhZd3FPUQ== --env FLEET_SERVER_POLICY_ID=policy1 -p 8220:8220 --rm docker.elastic.co/beats/elastic-agent:8.8.1 


### local server

- setup privacy for kibana
```shell
    xpack.security.enabled: true
    xpack.security.authc.api_key.enabled: true
```
- reset password for es: `./bin/elasticsearch-setup-passwords interactive`

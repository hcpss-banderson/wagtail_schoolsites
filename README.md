# wagtail.hcpss.org

A Wagtail version of the HCPSS school websites.

## Getting Started

### Launch Containers

```shell
docker-compose up -d
```

### Get Content Exports

Next we need specially formatted content exported from school site(s):

```shell
./fetch-exports.sh aes
```

You can fetch the exports of multiple schools:

```shell
./fetch-exports.sh aes mwms omhs
```

This will put the exported data in the /content folder

### Load the Exported Data into Wagtail

```shell
./import.sh aes mwms omhs
```

### Log In

Go to ```http://localhost:8000/admin```

### 

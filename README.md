# obd-feeder

This is an OBD feeder for [kuksa.val](https://github.com/eclipse/kuksa.val)


## Using docker
To build:
```
docker build -t obd_feeder .
```

To run:
```
docker run -it -v $PWD/config:/config obd_feeder
```

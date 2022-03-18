#If pydio installed - here is a startup script
docker run -d -e CELLS_EXTERNAL=<External address and port> -e CELLS_BIND=0.0.0.0:8883 -p 8883:8883 -v /var/cells/:/var/cells/ --network=host pydio/cells

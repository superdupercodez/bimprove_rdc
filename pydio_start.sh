#docker run -d -e CELLS_EXTERNAL=193.166.161.173:1883 -e CELLS_BIND=193.166.161.173:1883 -p 1883:1883 -v /var/cells/ --network=host pydio/cells
#docker run -d -e CELLS_EXTERNAL=193.166.161.173:8883 -e CELLS_BIND=193.166.161.173:8883 -p 8883:8883 -v /var/cells/ --network=host pydio/cellsll
#docker run -d -e CELLS_NO_TLS=0 -e CELLS_EXTERNAL=fasolt4.willab.fi:8883 -e CELLS_BIND=fasolt4.willab.fi:8883 -p 8883:8883 -v /var/cells --network=host
#docker run -d -e CELLS_NO_TLS=0 -e CELLS_EXTERNAL=fasolt4.willab.fi:8883 -e CELLS_BIND=0.0.0.0:8883 -p 8883:8883 -v /var/cells --network=host pydio/cells
#docker run -d -e CELLS_EXTERNAL=fasolt4.willab.fi:8883 -e CELLS_BIND=0.0.0.0:8883 -p 8883:8883 -v /var/cells:/var/cells/data --network=host pydio/cells
docker run -d -e CELLS_EXTERNAL=fasolt4.willab.fi:8883 -e CELLS_BIND=0.0.0.0:8883 -p 8883:8883 -v /var/cells/:/var/cells/ --network=host pydio/cells

## Repo structure

The project directory is mainly structured in this way:

    ZooTube
        ├── src
            ├── util
                ├── config.json
                ├── connect_util.py
                └── web_template.py
            ├── zootube_app.py  # Web application
            ├── publisher.py    # Publish frames from video to queue
            └── consumer.py     # Read frames from queue and process using YOLO
        ├── k8scluster        # Deploy docker to k8s cluster
            ├── deployment.yml
            └── service.yml
	    ├── dockerimage       # Build docker image as consumer
            └── Dockerfile
	    └── test   # test space for development
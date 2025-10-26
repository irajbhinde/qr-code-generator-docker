IMAGE=qr-code-generator-app
CONTAINER=qr-generator
DH_USER?=your-dockerhub-username

.PHONY: build run logs stop push clean

build:
\tdocker build -t $(IMAGE) .

run:
\tdocker run -d --name $(CONTAINER) $(IMAGE)

logs:
\tdocker logs $(CONTAINER)

stop:
\tdocker stop $(CONTAINER) || true
\tdocker rm $(CONTAINER) || true

push:
\tdocker tag $(IMAGE) $(DH_USER)/$(IMAGE):latest
\tdocker push $(DH_USER)/$(IMAGE):latest

clean:
\trm -rf qr_codes logs || true

PYTHON ?= python3
REQS = tools/requirements.txt

.PHONY: install sprite photo index validate

install:
	$(PYTHON) -m pip install -r $(REQS)

sprite:
	$(PYTHON) tools/render_sprite.py recipes/$(ID) --preview

photo:
	$(PYTHON) tools/resize_photo.py $(IN) recipes/$(ID)

index:
	$(PYTHON) tools/build_index.py

validate:
	$(PYTHON) tools/validate.py

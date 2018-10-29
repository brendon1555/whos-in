.PHONY: serve drop-db deps compile assets


PROJ_NAME=whosin

ANOMALY_DIR=$(HOME)/anomaly

# Closure Library and Compiler
CLOSURE_LIBRARY_RELEASE = 20180910
CLOSURE_LIBRARY = $(ANOMALY_DIR)/lib/closure-library-$(CLOSURE_LIBRARY_RELEASE)

# Closure Compiler
CLOSURE_COMPILER_RELEASE = 20181008
CLOSURE_COMPILER = $(ANOMALY_DIR)/bin/closure-compiler-v$(CLOSURE_COMPILER_RELEASE).jar
CLOSURE_DEPSWRITER=$(CLOSURE_LIBRARY)/closure/bin/build/depswriter.py
COMPILE_FULL=false

# Java
JAVA_VERSION=java-11-openjdk-amd64
JAVA=/usr/lib/jvm/$(JAVA_VERSION)/bin/java
JAVA_HEAP_SIZE = 2g

serve:
	cd whos_in; python server.py

drop-db:
	rm whos_in/whos_in.db

deps:
	[ -e client/closure-library ] || ln -s $(CLOSURE_LIBRARY) client/closure-Library

	@echo "Generating Closure dependencies using depswriter..."
	cd client/; python $(CLOSURE_DEPSWRITER) \
	--root_with_prefix="$(PROJ_NAME) ../../../$(PROJ_NAME)" > $(PROJ_NAME)-deps.js

define compile_js_app
	cd client; $(JAVA) -client -Xmx$(JAVA_HEAP_SIZE) -jar $(CLOSURE_COMPILER) \
	--compilation_level=$(2) \
	--warning_level=VERBOSE \
	--manage_closure_dependencies \
	--output_manifest=closure-compiler.MF \
	--jscomp_error=useOfGoogBase \
	--js=$(CLOSURE_LIBRARY)/closure/goog/**.js \
	--hide_warnings_for=$(CLOSURE_LIBRARY) \
	--js=!$(CLOSURE_LIBRARY)/**_test.js \
	--js=renaming-maps/$(3).js \
	--hide_warnings_for=renaming-maps/$(3).js \
	--js=$(PROJ_NAME)/**.js \
	--rename_variable_prefix wi_ \
	--closure_entry_point=$(1) \
	--js_output_file=../whos-in/static/js/$(PROJ_NAME)-$(4).js
endef

compile:
	ifeq ($(COMPILE_FULL), true)
		$(call compile_js_app,$(PROJ_NAME).ui.Renderer,SIMPLE,uncompiled,lsimple)
		$(call compile_js_app,$(PROJ_NAME).ui.Renderer,SIMPLE,compiled,simple-minified)
		$(call compile_js_app,$(PROJ_NAME).ui.Renderer,ADVANCED,uncompiled,advanced)
	endif
		$(call compile_js_app,$(PROJ_NAME).ui.Renderer,ADVANCED,compiled,advanced-minified)

assets:
	[ -d client/renaming-maps ] || mkdir client/renaming-maps
	[ -d whos-in/static/images ] || mkdir whos-in/static/images
	[ -d whos-in/static/styles ] || mkdir whos-in/static/styles

	cd whos-in/static/styles; $(JAVA) -jar $(CLOSURE_GSS_COMPILER) \
	--output-renaming-map-format CLOSURE_COMPILED \
	--rename NONE \
	--output-renaming-map ../../../client/renaming-maps/uncompiled.js \
	--output-file $(PROJ_NAME).css ../../../assets/styles/style.css

	cd whos-in/static/styles; $(JAVA) -jar $(CLOSURE_GSS_COMPILER) \
	--output-renaming-map-format CLOSURE_COMPILED \
	--rename CLOSURE \
	--output-renaming-map ../../../client/renaming-maps/compiled.js \
	--output-file $(PROJ_NAME)-minified.css ../../../assets/styles/style.css
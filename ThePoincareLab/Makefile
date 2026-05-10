SHELL := /bin/bash

PROJECT ?= the-poincare-lab

.PHONY: help install dev build preview deploy

## help: Show this help message
help:
	@echo "Available targets:" && echo
	@awk ' \
		/^## / {desc = substr($$0, 4); next} \
		/^[a-zA-Z0-9_.-]+:([^=]|$$)/ { \
			name = $$1; sub(/:.*/, "", name); \
			if (desc) { printf "\t- %-18s %s\n", name, desc; desc = "" } \
		} \
	' $(MAKEFILE_LIST)

## install: Install npm dependencies
install:
	npm install

## dev: Start Vite dev server with hot-reload (http://localhost:5173)
dev:
	npm run dev

## build: Build production bundle into dist/
build:
	npm run build

## preview: Build and serve production bundle locally (http://localhost:4173)
preview: build
	npm run preview

## deploy: Build and deploy to Cloudflare Pages (set PROJECT= to override project name)
deploy: build
	npx wrangler pages deploy dist --project-name $(PROJECT)

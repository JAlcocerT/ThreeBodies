# Simple Makefile for ThreeBodies
# Use `make help` to see available targets

SHELL := /bin/bash
COMPOSE ?= docker compose

# Paths
TRAEFIK_COMPOSE := Z_DeployMe/docker-compose.yml
TINYAUTH_COMPOSE := Z_DeployMe/TinyAuth_docker-compose.yml
POINCARE_DIR := ThePoincareLab

.PHONY: help run docker docker-up docker-down docker-logs traefik traefik-down traefik-logs tiny tiny-down tiny-logs \
        poincare-install poincare-dev poincare-build poincare-preview

## help: Show this help message
help:
	@echo "Available targets:" && echo
	@awk ' \
		/^## / {desc = substr($$0, 4); next} \
		/^[a-zA-Z0-9_.-]+:([^=]|$$)/ { \
			name = $$1; sub(/:.*/, "", name); \
			if (desc) { printf "\t- %s: %s\n", name, desc; desc = "" } \
		} \
	' $(MAKEFILE_LIST)

## run: Run the app directly (bare metal) with Hypercorn on 0.0.0.0:5050
run:
	hypercorn app-v2:app --bind 0.0.0.0:5050

## docker: Build and start using the default docker-compose.yml at the repo root (foreground)
docker: docker-up

## docker-up: Build and start containers (default compose)
docker-up:
	$(COMPOSE) build && $(COMPOSE) up

## docker-down: Stop and remove containers (default compose)
docker-down:
	$(COMPOSE) down

## docker-logs: Tail logs from default compose (Ctrl+C to stop)
docker-logs:
	$(COMPOSE) logs -f

## traefik: Start stack using Traefik compose at Z_DeployMe/docker-compose.yml (foreground)
traefik:
	$(COMPOSE) -f $(TRAEFIK_COMPOSE) up --build

## traefik-down: Stop Traefik stack
traefik-down:
	$(COMPOSE) -f $(TRAEFIK_COMPOSE) down

## traefik-logs: Tail logs for Traefik stack
traefik-logs:
	$(COMPOSE) -f $(TRAEFIK_COMPOSE) logs -f

## tiny: Start stack using TinyAuth+Traefik compose at Z_DeployMe/TinyAuth_docker-compose.yml (foreground)
tiny:
	$(COMPOSE) -f $(TINYAUTH_COMPOSE) up --build

## tiny-down: Stop TinyAuth+Traefik stack
tiny-down:
	$(COMPOSE) -f $(TINYAUTH_COMPOSE) down

## tiny-logs: Tail logs for TinyAuth+Traefik stack
tiny-logs:
	$(COMPOSE) -f $(TINYAUTH_COMPOSE) logs -f

# ── ThePoincareLab (React + Vite) ────────────────────────────────────────────

## poincare-install: Install npm dependencies for ThePoincareLab
poincare-install:
	cd $(POINCARE_DIR) && npm install

## poincare-dev: Start Vite dev server (hot-reload, http://localhost:5173)
poincare-dev:
	cd $(POINCARE_DIR) && npm run dev

## poincare-build: Build production bundle into ThePoincareLab/dist/
poincare-build:
	cd $(POINCARE_DIR) && npm run build

## poincare-preview: Serve the production build locally (http://localhost:4173) — mirrors CF Pages
poincare-preview: poincare-build
	cd $(POINCARE_DIR) && npm run preview

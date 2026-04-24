# Part D - Reflection and Architecture Documentation

## 64. Git Workflow Analysis
A branching strategy matters in teams because it creates predictable integration points, reduces accidental breakage on the main line, and makes review ownership clear. In this assignment, `develop` acts as the integration branch while feature branches isolate work and make pull requests reviewable. `git merge` preserves branch topology and is useful when you want traceable integration commits (for example conflict-resolution context). `git rebase` rewrites local history to apply commits on top of an updated base and produces a cleaner linear timeline before sharing. I use merge for collaborative branch integration and rebase for updating local branches before opening a PR.

## 65. Docker Optimization Justification
The original Docker approach had weak layering, no runtime hardening, and leaked sensitive defaults. The optimized image uses `python:3.9-slim`, installs dependencies through `requirements.txt` in an early cache-friendly layer, and copies app code later to avoid reinstalling dependencies on every source change. This significantly improves rebuild performance and lowers image size compared with a full `python:3.9` base and multiple `pip install` layers.

Security and runtime posture are improved by removing hardcoded DB secrets from the Dockerfile, running as a non-root user (`appuser`), exposing only application port `5000`, and defining a container `HEALTHCHECK`. Dockerfile secrets are risky because they become part of build history and image metadata, making accidental disclosure likely if images are shared or pushed.

## 66. Networking Analysis
Docker's default bridge network does not provide automatic DNS name resolution between arbitrary containers unless specific legacy links are used, so direct service-name communication is unreliable there. A user-defined bridge network includes embedded DNS and allows containers to resolve each other by service/container name (for example app connecting to host `db` in Compose). This is why the assignment stack uses a custom network (`sakila-network`) for stable service discovery and cleaner inter-container communication.

## 67. Docker Compose vs Manual Commands
Docker Compose solves orchestration concerns that manual `docker run` commands do not handle elegantly: dependency ordering, shared network/volume definitions, repeatable environment injection, and profile-based one-time services like `test-runner`. With Compose, the whole stack is declared once and started consistently with `docker compose up -d`.

`docker compose down` removes containers and networks but keeps named volumes. `docker compose down -v` additionally removes named volumes, which destroys persisted MySQL data. In this assignment, that difference is critical because the persistence task depends on keeping the `sakila-db-data` volume across container recreation.

## 68. CI/CD Pipeline Design Decisions
The pipeline is intentionally ordered as `lint -> test -> build -> security-scan` to fail fast and conserve runner resources. Linting is cheapest and catches style/static quality issues before spending time on service-container startup or image builds. Unit/integration tests then validate behavior prior to packaging. Build and smoke test validate deployability only after correctness checks pass.

The security scan is configured as non-blocking (`exit-code: 0`) because vulnerability reports are essential visibility, but blocking every finding can halt delivery on inherited base-image CVEs that are not immediately remediable. This balances risk awareness with operational flow. Concurrency cancellation prevents obsolete runs from consuming runners when newer commits supersede older ones on the same branch.

## 69. Production Readiness Assessment
For production, I would add centralized secrets management (for example cloud secret manager + short-lived credentials), full observability (structured logs, metrics, traces, SLO-based alerting), and infrastructure as code (Terraform/CloudFormation) to make environments reproducible and auditable. I would also add container orchestration (Kubernetes with readiness/liveness probes and rolling deployments), backup/restore testing for the database volume, and disaster recovery controls (multi-zone deployment, recovery playbooks, and periodic failover drills). These practices reduce operational risk beyond the current coursework-level deployment model.

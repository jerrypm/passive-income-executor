## Software Development & Engineering

### 1. Greenfield System Architecture
**Prompt**: Act as a principal software architect with 15 years designing distributed systems at Stripe and Shopify. I need to design [SYSTEM_DESCRIPTION] expecting [RPS] requests/sec and [DATA_VOLUME] of data. Propose a reference architecture covering compute, storage, caching, async messaging, and edge. Justify choices against CAP theorem trade-offs and 12-factor principles. Output: ASCII architecture diagram, component table (service, responsibility, tech, SLO), and 3 key risks with mitigations.

### 2. Monolith To Microservices Migration
**Prompt**: Act as a staff engineer who led 4 monolith decompositions at FAANG scale. My codebase is [CODEBASE_DESCRIPTION] with [LOC] lines in [LANGUAGE]. Propose a strangler-fig migration plan using DDD bounded contexts. Identify seams, shared kernels, and anti-corruption layers. Output: migration roadmap (6 phases), bounded-context map in ASCII, service extraction order ranked by risk/value, and rollback strategy per phase.

### 3. Event Driven Architecture Design
**Prompt**: Act as a principal engineer specializing in event-driven systems with Kafka and Kinesis. Design an event-driven architecture for [DOMAIN] with [EVENT_TYPES]. Apply event sourcing + CQRS where appropriate. Cover schema evolution, idempotency, exactly-once semantics, and dead-letter handling. Output: event catalog table (name, producer, consumers, schema version), sequence diagram in ASCII for the happy path, and a checklist of 10 production-readiness gates.

### 4. Multi Region Active Active
**Prompt**: Act as a distinguished engineer who shipped multi-region active-active platforms at AWS. Design a multi-region active-active deployment for [SERVICE] targeting [RTO] RTO and [RPO] RPO. Address conflict resolution (CRDT vs LWW), traffic steering, split-brain, and data residency ([REGIONS]). Output: topology diagram in ASCII, failure-mode table (scenario, detection, automatic response, human runbook), and load-test plan.

### 5. Capacity Planning Model
**Prompt**: Act as a performance engineer with deep queuing theory expertise. Build a capacity model for [SERVICE] given baseline [RPS], p99 latency budget [MS], growth rate [X]%/month, and instance profile [CPU/MEM]. Use Little's Law and USE method. Output: spreadsheet-style table (month, RPS, instances, $cost, headroom %), bottleneck analysis per tier, and 3 scale-out triggers with alert thresholds.

### 6. Service Mesh Decision
**Prompt**: Act as a platform architect who evaluated Istio, Linkerd, and Consul Connect in production. Given [CLUSTER_SIZE], [LANGUAGE_MIX], and [SECURITY_REQS], recommend a service mesh or explain why none. Compare mTLS, traffic splitting, observability, and operational cost. Output: decision matrix (criteria x mesh), ADR in MADR format, and a 30-day adoption plan with exit criteria.

### 7. Hexagonal Architecture Refactor
**Prompt**: Act as a clean-architecture expert following Alistair Cockburn's hexagonal pattern. Refactor [MODULE] written in [LANGUAGE] to hexagonal architecture. Identify ports, adapters, and the domain core. Preserve behavior; eliminate framework coupling. Output: before/after package layout tree, interface definitions for ports with docstrings, and a unit test example that runs the domain without any adapters.

### 8. Domain Driven Design Modeling
**Prompt**: Act as a DDD practitioner trained by Eric Evans and Vaughn Vernon. Model the [BUSINESS_DOMAIN] using strategic DDD. Identify bounded contexts, aggregates, entities, value objects, domain events, and context relationships (shared kernel, ACL, conformist). Output: context map in ASCII, aggregate table (name, root, invariants, events), and a ubiquitous-language glossary of 15+ terms.

### 9. CQRS Read Model Design
**Prompt**: Act as a principal engineer who built CQRS systems handling 1B events/day. For [USE_CASE], design the read-side: projection store, materialized views, rebuild strategy, and eventual-consistency UX. Cover catch-up subscriptions, poison messages, and zero-downtime schema migrations. Output: projection spec table, SQL DDL for read models, and a rebuild runbook with step-by-step commands.

### 10. Technical Design Document
**Prompt**: Act as a tech lead writing a TDD for a senior review committee. The feature is [FEATURE_DESCRIPTION]. Produce a production-grade technical design document covering goals, non-goals, API contract, data model, failure modes, rollout plan, metrics, and alternatives considered. Output: full TDD in Markdown sections (Context, Proposal, Alternatives, Risks, Rollout, Observability, Open Questions) with at least one ASCII diagram.

### 11. Principled Code Review
**Prompt**: Act as a staff engineer reviewing a PR from a mid-level dev. Review the following [LANGUAGE] code: [CODE_BLOCK]. Apply SOLID, DRY, YAGNI, and Clean Code principles. Flag naming, cohesion, coupling, error handling, testability, and performance. Output: line-numbered comments table (line, severity P0/P1/P2, issue, suggested fix, principle violated) and a 3-sentence overall verdict.

### 12. SOLID Refactor Exercise
**Prompt**: Act as Robert C. Martin teaching SOLID. Take this class [CODE_BLOCK] in [LANGUAGE] and refactor it to honor all five SOLID principles. Explain each violation found before fixing. Output: original violations list, refactored code with inline comments showing which principle each change satisfies, and a UML-style ASCII class diagram of the new design.

### 13. Design Pattern Application
**Prompt**: Act as a GoF design-patterns expert. For this scenario: [PROBLEM_DESCRIPTION], recommend the most appropriate pattern (Strategy, Factory, Observer, Decorator, Adapter, Command, etc.) with justification. Explain why other candidates are worse. Output: pattern name, intent quote from GoF, [LANGUAGE] implementation with tests, class diagram in ASCII, and 2 anti-pattern traps to avoid.

### 14. Legacy Code Rescue
**Prompt**: Act as Michael Feathers applying "Working Effectively with Legacy Code". I have untested legacy [LANGUAGE] code: [CODE_BLOCK]. Apply the "sprout method", "seam", and "characterization test" techniques to make it testable without changing behavior. Output: identified seams table, characterization tests in the project's test framework, refactored code, and the order of safe steps followed.

### 15. Cyclomatic Complexity Reduction
**Prompt**: Act as a code-quality engineer obsessed with McCabe complexity. This function [CODE_BLOCK] has high cyclomatic complexity. Reduce it below 10 using guard clauses, polymorphism, table-driven methods, and early returns. Preserve behavior. Output: original complexity score, refactored code, new complexity score, and a table mapping each original branch to the new structure.

### 16. Dead Code Elimination
**Prompt**: Act as a code archaeologist specializing in large monorepos. Given [CODEBASE_DESCRIPTION], propose a safe strategy to detect and remove dead code: unreferenced functions, unreachable branches, feature-flag orphans, and zombie tests. Cover static analysis tools per [LANGUAGE]. Output: tool list with commands, a 5-phase removal plan, rollback strategy, and risk ranking per category.

### 17. API Consistency Audit
**Prompt**: Act as an API governance lead at a platform company. Audit the following API surface [API_SPEC] for consistency: naming (camelCase vs snake_case), pluralization, error envelopes, pagination style, timestamp formats, and HTTP status usage. Output: inconsistency table (endpoint, issue, fix, breaking? y/n), proposed style guide in bullets, and a migration plan using deprecation headers.

### 18. Function Naming Refactor
**Prompt**: Act as a clean-code reviewer who believes names are the hardest problem in CS. Rename the functions and variables in [CODE_BLOCK] written in [LANGUAGE]. Apply the rules: intention-revealing, pronounceable, searchable, no encodings, verbs for functions, nouns for variables. Output: before/after rename table with rationale, refactored code, and 3 rules of thumb the dev should internalize.

### 19. Code Smell Catalog
**Prompt**: Act as a Fowler-trained refactoring expert. Scan this code [CODE_BLOCK] in [LANGUAGE] for smells from "Refactoring" (long method, large class, feature envy, data clumps, primitive obsession, shotgun surgery, etc.). Output: smell table (smell name, location, evidence, recommended refactoring technique), priority-ordered refactor list, and a refactored version of the top 3 issues.

### 20. Pull Request Template
**Prompt**: Act as an engineering-excellence lead defining PR hygiene for a 200-dev org. Design a PR template and review checklist that enforces small diffs, test coverage, observability hooks, security review, and rollback notes. Tailor to [LANGUAGE/STACK]. Output: Markdown PR template ready to commit to .github/, reviewer checklist table, and 5 metrics to track (cycle time, review latency, etc.).

### 21. Stack Trace Triage
**Prompt**: Act as an SRE on the pager for 10 years. Analyze this stack trace: [ERROR_TRACE] from a [LANGUAGE]/[FRAMEWORK] service. Perform root-cause analysis using the "5 Whys" technique. Distinguish symptom from cause. Output: ordered hypothesis list with disproof steps, most-likely root cause with evidence, immediate mitigation, permanent fix, and 2 detection gaps that let this escape.

### 22. Heisenbug Investigation
**Prompt**: Act as a debugging expert who specializes in intermittent failures. The bug is: [BUG_DESCRIPTION], reproducing ~[FREQUENCY]. Suspect categories: race conditions, GC pauses, DNS, clock skew, network partitions, or memory pressure. Propose an investigation plan using eBPF, flight recorder, or equivalent. Output: hypothesis tree, instrumentation commands to capture evidence, and a decision table mapping observed signal to verdict.

### 23. Memory Leak Hunt
**Prompt**: Act as a JVM/Node/Go/Swift performance engineer (pick by [LANGUAGE]). RSS grows [X]MB/hour in [SERVICE]. Walk through a leak-hunting playbook using heap dumps, allocation profilers, and retained-size analysis. Output: step-by-step commands for the target runtime, common leak patterns to check (listener leaks, cache without eviction, closures), and a root-cause report template.

### 24. Latency Spike Diagnosis
**Prompt**: Act as a performance engineer at a trading firm. p99 latency for [ENDPOINT] jumped from [BASELINE] to [CURRENT]. Use the USE method (Utilization, Saturation, Errors) and RED method to partition the search space. Output: diagnostic decision tree, dashboard query list (Prometheus/Datadog), top 10 suspects ranked by prior probability, and bisection plan using canary traffic.

### 25. Flaky Test Root Cause
**Prompt**: Act as a test-infrastructure lead who eliminated flakes in a 50k-test suite. Test [TEST_NAME] fails [X]% of runs with [ERROR]. Classify the flake: timing, order dependency, shared state, network, random seed, or resource leak. Output: classification with evidence, minimal reproducer strategy, fix options ranked by permanence, and a quarantine policy template.

### 26. Production Incident Postmortem
**Prompt**: Act as an SRE writing a blameless postmortem per Google SRE Book. Incident: [INCIDENT_DESCRIPTION], duration [X] min, impact [Y]. Produce a postmortem covering timeline, detection, response, root cause (using causal chain, not a single cause), contributing factors, and action items. Output: full postmortem in Google's format with timestamps table, "what went well / what went wrong", and 5+ action items with owners.

### 27. Distributed Tracing Analysis
**Prompt**: Act as an observability engineer fluent in OpenTelemetry. Given a trace [TRACE_JSON] from a [N]-service request, identify the critical path, hotspots, and missing spans. Compute self-time vs wall-time per service. Output: annotated trace summary, service contribution table (service, self-time, wait-time, % of critical path), and 3 optimization levers ranked by impact.

### 28. Git Bisect Strategy
**Prompt**: Act as a senior engineer who has debugged regressions via bisect hundreds of times. A regression was introduced between [GOOD_SHA] and [BAD_SHA] in [REPO]. Design a bisect strategy including a reliable reproducer script, skip rules for broken commits, and automated `git bisect run`. Output: reproducer script in bash, full bisect command sequence, and a template for the fix commit message.

### 29. Concurrency Bug Analysis
**Prompt**: Act as a concurrency expert with deep knowledge of memory models in [LANGUAGE]. Given this code [CODE_BLOCK], find data races, deadlocks, livelocks, or missed wake-ups. Reason about happens-before ordering. Output: bug list with line numbers, a minimal reproducer, the correct fix using appropriate primitive (mutex, channel, atomic, actor), and a verification approach (race detector, TLA+, or stress test).

### 30. Perf Regression Bisection
**Prompt**: Act as a performance engineer maintaining a benchmark suite. Benchmark [BENCH_NAME] regressed [X]% between releases [A] and [B]. Design a bisection using microbenchmarks + profiler (perf/pprof/Instruments). Output: bisection plan, profiler commands, flamegraph reading guide, and a report template with before/after numbers, root cause, and fix verification.

### 31. TDD Kata Walkthrough
**Prompt**: Act as Kent Beck teaching TDD. Walk me through implementing [FEATURE] in [LANGUAGE] using strict red-green-refactor. Show at least 6 micro-cycles. For each cycle: failing test, minimal production code, refactor. Output: numbered cycles with test code, production code, and a one-line rationale per step, ending with a summary of emergent design decisions.

### 32. Test Pyramid Strategy
**Prompt**: Act as a QA architect defining a test strategy for [PROJECT_DESCRIPTION] in [STACK]. Apply Mike Cohn's test pyramid plus the "testing trophy" for frontend. Balance unit, integration, contract, E2E, and exploratory. Output: pyramid ratio table (level, % of suite, tools, avg runtime budget), what to test at each level, and 5 anti-patterns to avoid (ice-cream cone, etc.).

### 33. Property Based Test Design
**Prompt**: Act as a property-based testing expert using Hypothesis/QuickCheck/fast-check. For [FUNCTION_SIGNATURE], design properties beyond the obvious: invariants, roundtrips, oracle comparisons, metamorphic relations, model-based tests. Output: property list with rationale, [LANGUAGE]/[FRAMEWORK] implementation, shrinking strategy, and 3 bugs this would catch that example-based tests would miss.

### 34. Contract Test Setup
**Prompt**: Act as a microservices testing lead using Pact. My consumer [SERVICE_A] calls provider [SERVICE_B] via [PROTOCOL]. Set up consumer-driven contract tests with Pact broker, versioning, and CI gates. Output: consumer-side test code in [LANGUAGE], provider verification setup, broker URL strategy, CI pipeline YAML snippet, and a rollout checklist.

### 35. Mutation Testing Adoption
**Prompt**: Act as a test-quality engineer introducing mutation testing. For [LANGUAGE] project with [X]% line coverage, explain what mutation score reveals that coverage hides. Recommend a tool (Stryker, PIT, mutmut, mull). Output: setup commands, baseline mutation run plan, incremental adoption strategy (per-package thresholds), and interpretation of common surviving mutants.

### 36. E2E Test Stability
**Prompt**: Act as a test-infra lead who made Playwright/Cypress suites stable at scale. Current E2E suite has [X]% flake rate and [Y] min runtime. Diagnose and fix: wait strategy, test data, parallelization, retries, and selectors. Output: root-cause table (symptom, cause, fix), best-practice checklist, sample stable test in [FRAMEWORK], and a flake budget policy.

### 37. BDD Scenario Authoring
**Prompt**: Act as a BDD coach trained by Dan North. For [USER_STORY], write Gherkin scenarios following "Given-When-Then" with declarative (not imperative) style. Cover happy path, edge cases, and error cases. Avoid UI coupling. Output: feature file in Gherkin, step definition signatures in [LANGUAGE], and 3 smells to avoid (scenario soup, UI leakage, data tables as DSL).

### 38. Test Doubles Strategy
**Prompt**: Act as a testing expert who internalized Gerard Meszaros's xUnit Patterns. For [UNIT_UNDER_TEST], decide when to use dummies, stubs, fakes, spies, or mocks. Avoid over-mocking. Output: dependency table (collaborator, double type, rationale), example test in [LANGUAGE]/[FRAMEWORK], and a rule-of-thumb cheatsheet for picking the right double.

### 39. Load Test Plan
**Prompt**: Act as a performance QA engineer using k6/Locust/Gatling. Design a load test for [API_ENDPOINT] targeting [RPS] with [LATENCY_SLO]. Include warm-up, ramp, steady-state, stress, and soak phases. Cover think time, realistic distributions, and data seeding. Output: test script in [TOOL], scenario table, pass/fail criteria, and a results interpretation guide.

### 40. Snapshot Testing Ethics
**Prompt**: Act as a senior frontend engineer who has seen snapshot tests become technical debt. For [COMPONENT] in [FRAMEWORK], decide when snapshot tests help vs harm. Propose guidelines: what to snapshot, size limits, review discipline, and when to prefer visual regression or assertion-based tests. Output: policy document (do/don't/when), example correct test, and example anti-pattern.

### 41. REST API Design
**Prompt**: Act as an API designer who contributed to the JSON:API spec. Design a REST API for [RESOURCE_DESCRIPTION]. Apply Richardson Maturity Model level 3 (HATEOAS optional), proper HTTP verbs, status codes, idempotency, pagination (cursor), filtering, sorting, and error envelopes per RFC 7807. Output: endpoint table, request/response examples, OpenAPI 3.1 skeleton, and versioning strategy.

### 42. GraphQL Schema Design
**Prompt**: Act as a GraphQL architect who designed schemas at GitHub/Shopify scale. Model [DOMAIN] as a GraphQL schema. Use Relay-style connections, global IDs, union/interface types, and proper nullability. Address N+1 via DataLoader, persisted queries, and depth limits. Output: SDL schema, resolver responsibilities table, security considerations, and a 10-item schema review checklist.

### 43. gRPC Service Definition
**Prompt**: Act as a backend engineer who migrated REST services to gRPC at scale. Define a gRPC service for [USE_CASE] using protobuf 3. Include unary, server-streaming, client-streaming, and bidi where justified. Cover deadlines, retries, backoff, auth interceptors, and error model (google.rpc.Status). Output: .proto file, service behavior table, and a client/server skeleton in [LANGUAGE].

### 44. API Versioning Strategy
**Prompt**: Act as a platform API lead who has deprecated endpoints at scale. For [API] with [N] consumers, compare versioning strategies: URI path, header, media type, query param, and evolution. Recommend one with justification, including deprecation policy, sunset headers, and client migration kit. Output: decision matrix, chosen strategy ADR, deprecation timeline template, and client notification plan.

### 45. Webhook Delivery System
**Prompt**: Act as a principal engineer who built Stripe-style webhooks. Design a reliable webhook delivery system with exponential backoff, idempotency keys, HMAC signatures (replay protection), dead-letter queue, and consumer dashboard. Output: architecture diagram in ASCII, delivery state machine, retry schedule table, HMAC signing code sample in [LANGUAGE], and a consumer integration guide.

### 46. Rate Limiting Algorithm Choice
**Prompt**: Act as an infra engineer who implemented rate limiters at edge. Compare fixed window, sliding window, token bucket, and leaky bucket for [USE_CASE] with [RPS] and [BURST]. Address distributed state (Redis vs local). Output: comparison table, recommendation with rationale, pseudocode for chosen algorithm, Redis Lua script if distributed, and headers to return (X-RateLimit-*, Retry-After).

### 47. API Pagination Patterns
**Prompt**: Act as a backend lead who redesigned pagination for a 10B-row API. Compare offset/limit, keyset (cursor), seek, and time-based pagination for [RESOURCE]. Address stability, consistency under mutation, deep-paging cost, and total counts. Output: decision tree, chosen approach with SQL examples, API contract (cursor opaque format), and 3 pitfalls to avoid.

### 48. Idempotency Key Design
**Prompt**: Act as a payments engineer who built idempotency at Stripe. Design idempotency for [MUTATING_ENDPOINT]. Cover key generation by client, server storage TTL, request fingerprinting, concurrent-request handling, and response replay. Output: sequence diagram in ASCII, storage schema, pseudocode for the middleware, failure cases (key reuse with different body), and 5-item test plan.

### 49. OpenAPI Documentation
**Prompt**: Act as an API DX lead. Given this endpoint [ENDPOINT_DESCRIPTION], write a complete OpenAPI 3.1 spec including schemas, examples (request + response), error responses, security schemes, server variables, and x-codeSamples for [LANGUAGES]. Output: full YAML spec, Spectral lint rules to enforce quality, and a doc-site generation command.

### 50. Error Response Standard
**Prompt**: Act as an API governance lead defining error contracts. Specify an error response standard based on RFC 7807 (Problem Details) for [API]. Cover type URIs, machine-readable codes, trace IDs, retryable flag, and i18n. Output: JSON schema for the error envelope, example responses for validation/auth/server errors, status-code mapping table, and client handling pseudocode.

### 51. Schema Design Normalization
**Prompt**: Act as a database architect with expertise in relational modeling. Design a normalized schema (3NF) for [DOMAIN]. Identify entities, relationships, keys (natural vs surrogate), and constraints. Then selectively denormalize for [READ_PATTERN]. Output: ER diagram in ASCII, DDL for [POSTGRES/MYSQL], index plan, and a denormalization table (what, why, staleness tolerance).

### 52. Index Optimization Plan
**Prompt**: Act as a Postgres performance expert. Given these slow queries [QUERY_LIST] and table stats [TABLE_INFO], design an index strategy. Consider btree, hash, GIN, GiST, BRIN, and partial/covering/expression indexes. Output: recommended indexes with CREATE statements, expected effect per query (EXPLAIN reasoning), write-amplification cost, and an index-maintenance plan.

### 53. SQL Query Refactor
**Prompt**: Act as a SQL tuning expert. Rewrite this query [SQL_QUERY] for performance while preserving results. Consider CTE vs subquery, window functions, lateral joins, avoiding SELECT *, predicate pushdown, and index usage. Output: rewritten SQL, EXPLAIN ANALYZE interpretation, expected plan change, and 3 common pitfalls you avoided.

### 54. NoSQL Data Modeling
**Prompt**: Act as a DynamoDB/MongoDB expert who internalized Rick Houlihan's single-table design. Model [DOMAIN] for [ACCESS_PATTERNS] in DynamoDB. Design PK/SK, GSIs, and item collection layout. Avoid hot partitions. Output: access-pattern table (name, PK, SK, index), entity-attribute-value matrix, 3 sample items, and cost estimate (RCU/WCU).

### 55. Database Migration Zero Downtime
**Prompt**: Act as a DBA who has run online migrations on 10TB tables. For [MIGRATION_DESCRIPTION] on [ENGINE], design a zero-downtime migration using expand-contract, shadow reads/writes, or pt-online-schema-change/gh-ost. Output: step-by-step runbook, backfill script skeleton, rollback plan, monitoring metrics, and expected duration formula.

### 56. Sharding Strategy
**Prompt**: Act as a principal engineer who sharded a Postgres cluster at scale. For [TABLE] growing [X]GB/month, recommend a sharding strategy: range, hash, directory, geo, or Citus/Vitess. Address rebalancing, cross-shard joins, and distributed transactions. Output: strategy choice with ADR, shard key rationale, topology diagram, and 5 operations that become harder.

### 57. Read Replica Architecture
**Prompt**: Act as a database reliability engineer. Design a read-replica topology for [PRIMARY_DB] with [READ_RPS]. Cover replication lag budget, routing (app-level vs proxy), failover, split-brain prevention, and stale-read handling (read-your-writes). Output: topology diagram, lag monitoring queries, routing logic pseudocode, and a failover runbook.

### 58. Cache Invalidation Strategy
**Prompt**: Act as a caching expert who has burned on Phil Karlton's second hardest problem. For [READ_HEAVY_WORKLOAD] with [CONSISTENCY_REQS], choose between cache-aside, read-through, write-through, write-behind, and refresh-ahead. Handle stampede (singleflight), TTL jitter, and negative caching. Output: strategy with justification, pseudocode, failure modes table, and observability metrics to track hit ratio and staleness.

### 59. Transaction Isolation Choice
**Prompt**: Act as a database expert fluent in ANSI isolation levels and MVCC. For [WORKFLOW] in [ENGINE], choose between Read Committed, Repeatable Read, Snapshot, and Serializable. Explain phenomena allowed (dirty read, non-repeatable read, phantom, write skew). Output: chosen level with rationale, SQL example showing the race prevented, and 3 application-level alternatives (SELECT FOR UPDATE, optimistic locking).

### 60. Data Warehouse Modeling
**Prompt**: Act as an analytics engineer trained by Kimball. Model [BUSINESS_PROCESS] as a star schema. Identify fact table grain, dimensions (SCD type 1/2/3), conformed dims, and aggregates. Output: bus matrix table, fact and dim DDL, grain declaration, and dbt model skeleton with ref() and tests (unique, not_null, relationships).

### 61. Dockerfile Hardening
**Prompt**: Act as a container security engineer. Review/write a production-grade Dockerfile for [LANGUAGE] app. Apply multi-stage builds, distroless/alpine base, non-root user, minimal capabilities, readonly filesystem, explicit USER/WORKDIR, .dockerignore, and vuln scanning. Output: the Dockerfile, .dockerignore, and a table of hardening steps with CIS benchmark references.

### 62. Kubernetes Deployment Manifest
**Prompt**: Act as a Kubernetes SRE. Write production-grade manifests for [SERVICE]: Deployment, Service, HPA, PDB, NetworkPolicy, and ConfigMap/Secret. Set resource requests/limits, liveness/readiness/startup probes, securityContext (runAsNonRoot, readOnlyRootFilesystem), topology spread, and rolling update strategy. Output: YAML manifests, kubectl validate command, and a 15-item production checklist.

### 63. CI Pipeline Design
**Prompt**: Act as a DevEx lead building pipelines for a 500-dev org. Design a CI pipeline for [REPO_LAYOUT] in [CI_TOOL] (GitHub Actions/GitLab/Buildkite). Cover build, unit, lint, type-check, security scan, container build, artifact signing (Cosign/SLSA), and cache strategy. Output: YAML pipeline, stage table with runtime budgets, cache keys, and parallelization plan.

### 64. CD Deployment Strategy
**Prompt**: Act as a release engineer who shipped via blue/green, canary, and progressive delivery. For [SERVICE] with [TRAFFIC], recommend a deployment strategy using Argo Rollouts/Flagger or equivalent. Cover metrics-based auto-rollback, feature flags, and DB coupling. Output: strategy with rationale, rollout spec YAML, analysis template metrics, and rollback triggers.

### 65. Terraform Module Design
**Prompt**: Act as an IaC architect who maintains a Terraform module registry. Design a reusable Terraform module for [RESOURCE] following the standard structure (main.tf, variables.tf, outputs.tf, versions.tf, examples/). Apply least privilege, tagging, and lifecycle. Output: module files, README with inputs/outputs table, tflint/checkov rules, and a semver release plan.

### 66. Helm Chart Authoring
**Prompt**: Act as a platform engineer authoring Helm charts used by 50 teams. Write a Helm chart for [APP] with values.yaml, templates, NOTES.txt, and helpers. Support overrides for resources, image, env, ingress, and HPA. Include values schema (values.schema.json) for validation. Output: chart files, a default values.yaml with comments, and a `helm template` test example.

### 67. Observability Stack Setup
**Prompt**: Act as an observability lead who deployed Prometheus + Grafana + Loki + Tempo at scale. For [ENVIRONMENT], design the full stack: metrics, logs, traces, and correlation. Cover cardinality control, retention, and sampling. Output: architecture diagram in ASCII, retention/cost table, 5 golden-signal dashboards outline, and alert policy starter pack.

### 68. SLO SLI Definition
**Prompt**: Act as an SRE applying Google's SRE book. For [SERVICE], define SLIs (availability, latency, correctness, freshness), SLOs (target %), SLAs, and error budget policy. Pick the right measurement window. Output: SLI specification table (name, formula, query), SLO targets with rationale, error budget math, and burn-rate alert thresholds (fast + slow).

### 69. Infrastructure Cost Optimization
**Prompt**: Act as a FinOps engineer who reduced AWS bills by 40%. Given [INFRA_DESCRIPTION] and [MONTHLY_COST], produce an optimization plan covering right-sizing, Savings Plans, Spot, storage tiers, egress, idle resources, and architectural changes. Output: savings table (lever, est. $/month, risk, effort), quick-wins list, and a 90-day execution plan.

### 70. Chaos Engineering Plan
**Prompt**: Act as a chaos engineer at Netflix-scale. Design a chaos experiment plan for [SYSTEM] starting at GameDay level and progressing to production. Use Principles of Chaos (hypothesis, blast radius, abort). Output: experiment catalog table (name, hypothesis, blast radius, abort conditions), tool recommendation (Gremlin/Litmus/ChaosMesh), and a maturity roadmap.

### 71. Threat Model Workshop
**Prompt**: Act as a security architect running STRIDE-based threat modeling. For [SYSTEM_DESCRIPTION], produce a threat model: data flow diagram, trust boundaries, threats per STRIDE category, and mitigations. Output: ASCII DFD with trust zones, threat table (threat, STRIDE, likelihood, impact, mitigation, owner), and 5 highest-priority action items.

### 72. OWASP Top 10 Audit
**Prompt**: Act as an application security engineer. Audit [APP_DESCRIPTION] in [LANGUAGE]/[FRAMEWORK] against OWASP Top 10 (2021). For each category (A01 Broken Access Control through A10 SSRF), assess exposure and recommend controls. Output: audit table (category, status, evidence, remediation, priority), top 3 critical findings with code fixes, and a remediation sprint plan.

### 73. Auth Architecture Design
**Prompt**: Act as an IAM architect who designed OAuth2/OIDC at scale. For [APP] with [USER_TYPES], design the auth architecture: identity provider, flows (auth code + PKCE, device, client credentials), token format (JWT vs opaque), session management, and refresh rotation. Output: architecture diagram, flow sequence for each use case, token claims schema, and 10-item security checklist.

### 74. Secrets Management Plan
**Prompt**: Act as a platform security engineer. Design secrets management for [ENVIRONMENT] using Vault/AWS Secrets Manager/SOPS. Cover rotation, dynamic credentials, least privilege, audit logging, and developer ergonomics. Address bootstrapping the "secret zero". Output: architecture, rotation policy per secret type, rollout plan from current state, and 5 common mistakes to avoid.

### 75. CSRF XSS Prevention
**Prompt**: Act as a web security engineer. For [WEB_APP] in [FRAMEWORK], design defenses against XSS (stored, reflected, DOM) and CSRF. Cover CSP (strict-dynamic + nonces), SameSite cookies, synchronizer tokens, output encoding, and Trusted Types. Output: control table (threat, defense, implementation), sample CSP header, code snippets for each defense, and a test plan.

### 76. SQL Injection Defense
**Prompt**: Act as an AppSec engineer. Given this [LANGUAGE] code [CODE_BLOCK] that builds SQL, identify injection risks and refactor using parameterized queries, prepared statements, or ORMs. Cover dynamic identifiers (table/column names), IN clauses, and LIKE patterns. Output: vulnerable-vs-fixed code, test payloads, and a library-level lint rule to prevent regression.

### 77. Dependency Supply Chain
**Prompt**: Act as a supply-chain security engineer who implemented SLSA level 3. For [REPO] in [LANGUAGE], design defenses: lockfile integrity, Dependabot/Renovate, SBOM generation (Syft), vuln scanning (Grype/Trivy), signed commits, signed artifacts (Cosign), and provenance attestation. Output: control table, CI workflow snippets, and an incident playbook for a compromised dependency.

### 78. JWT Best Practices
**Prompt**: Act as an identity engineer who has seen every JWT footgun. Review/design JWT usage for [APP]: algorithm choice (EdDSA vs RS256; never none), kid rotation, aud/iss/exp validation, token scope minimization, storage (httpOnly cookie vs memory), and revocation. Output: do/don't table, token claim schema, sample signing and verification code in [LANGUAGE], and 5 common exploits.

### 79. Zero Trust Network Design
**Prompt**: Act as a zero-trust architect. For [INTERNAL_ENVIRONMENT], design zero-trust access: identity-aware proxy, device posture, mTLS everywhere, workload identity (SPIFFE/SPIRE), policy engine (OPA), and continuous verification. Output: architecture in ASCII, policy examples in Rego, migration plan from perimeter model, and measurable outcomes.

### 80. Security Incident Response
**Prompt**: Act as a security IR lead. An alert fires: [ALERT_DESCRIPTION]. Walk through the IR playbook per NIST SP 800-61: detection, triage, containment (short + long term), eradication, recovery, and post-incident. Output: minute-by-minute action list, communication template for stakeholders, evidence-preservation commands, and a post-incident report outline.

### 81. SwiftUI Architecture MVVM
**Prompt**: Act as a principal iOS engineer who shipped SwiftUI apps at scale. For [APP_DESCRIPTION], design an MVVM architecture using Swift Concurrency, @Observable (or ObservableObject), and dependency injection via environment. Cover navigation with NavigationStack, state restoration, and previewability. Output: module diagram, ViewModel protocol, a sample feature with View + ViewModel + Repo, and testing strategy.

### 82. UIKit To SwiftUI Migration
**Prompt**: Act as an iOS tech lead migrating a UIKit codebase to SwiftUI incrementally. Given [APP_DESCRIPTION] with [LOC] UIKit code, propose a strangler-fig plan using UIHostingController, UIViewRepresentable, and coordinator bridges. Output: migration phases, compatibility bridge patterns (code snippets), risks table, and a rollback plan per screen.

### 83. Swift Concurrency Refactor
**Prompt**: Act as a Swift concurrency expert who read Doug Gregor's evolution proposals. Refactor this callback-based code [CODE_BLOCK] to async/await with proper actor isolation, structured concurrency (TaskGroup), cancellation, and Sendable conformance. Output: refactored code, isolation domain diagram, a table of each original callback mapped to async, and 3 data-race pitfalls avoided.

### 84. Core Data SwiftData Modeling
**Prompt**: Act as an iOS data architect. Model [DOMAIN] in Core Data or SwiftData (pick based on [MIN_IOS]). Cover entities, relationships, validation, migration (lightweight vs manual), background contexts, and conflict resolution. Output: entity diagram, sample .xcdatamodeld spec in table form, migration plan between versions, and a thread-safety checklist.

### 85. iOS Performance Optimization
**Prompt**: Act as an iOS performance engineer fluent in Instruments. For [APP_SYMPTOM] (e.g., slow launch, scroll jank, battery drain), design an investigation using Time Profiler, Allocations, Core Animation, and os_signpost. Output: Instruments template per symptom, common causes table, code-level checklist (main thread, image decoding, cell reuse), and acceptance criteria.

### 86. iOS Accessibility Audit
**Prompt**: Act as an iOS accessibility lead certified in WCAG 2.2. Audit [SCREEN_DESCRIPTION] for VoiceOver, Dynamic Type, Smart Invert, Reduce Motion, Switch Control, and color contrast. Output: finding table (issue, WCAG criterion, fix), SwiftUI code samples for accessibilityLabel/Value/Hint/Traits, a11y test plan using XCUITest, and a sign-off checklist.

### 87. App Store Release Checklist
**Prompt**: Act as an iOS release manager who has shipped 200+ App Store releases. For [APP] release [VERSION], produce a release checklist: version bumping, changelog, screenshots, privacy nutrition labels, ATT, App Review guidelines compliance, phased rollout, and rollback plan. Output: checklist in Markdown, common rejection reasons to pre-check, and a post-release monitoring plan.

### 88. iOS Push Notification Design
**Prompt**: Act as an iOS backend + client engineer who built APNs at scale. Design push notifications for [USE_CASE]: APNs tokens, token refresh, silent pushes, NotificationServiceExtension for mutable content, critical alerts, and server-side provider API. Cover delivery metrics and opt-in funnel. Output: architecture, iOS code snippets, server payload examples, and analytics events to track.

### 89. Swift Package Modularization
**Prompt**: Act as an iOS build engineer. Given [APP_DESCRIPTION] with [LOC], propose a SwiftPM-based modularization: feature modules, core modules, interface vs implementation split, and binary targets for heavy deps. Address build times, test speed, and preview reliability. Output: package graph diagram, Package.swift skeletons, module boundary rules, and a migration path from monolith.

### 90. iOS Secure Storage
**Prompt**: Act as an iOS security engineer. For [SENSITIVE_DATA] (tokens, PII, keys), design secure storage using Keychain (kSecAttrAccessible options), Secure Enclave for keys, CryptoKit, and biometrics gating via LocalAuthentication. Cover jailbreak-resistant strategies and backup/restore semantics. Output: decision table per data type, Swift code sample, and 5 pitfalls (iCloud Keychain, sim vs device).

### 91. React Component Architecture
**Prompt**: Act as a principal frontend engineer who led design systems at Vercel/Shopify. For [FEATURE] in React 19, design the component tree using composition over props, container/presentational split, and server vs client components. Apply accessibility primitives (Radix/ARIA). Output: component tree diagram, props table for each component, sample TSX with Suspense boundaries, and a testing plan.

### 92. Next.js App Router Design
**Prompt**: Act as a Next.js expert who shipped App Router apps in production. Design the routing, data fetching, and caching strategy for [APP]. Cover Server Components, Server Actions, streaming, parallel/intercepted routes, `revalidatePath/Tag`, and edge vs node runtime. Output: route tree, data-fetch table per route, cache keys, and 5 common footguns to avoid.

### 93. Frontend State Management
**Prompt**: Act as a frontend architect who has used Redux, Zustand, Jotai, Recoil, and TanStack Query. For [APP_DESCRIPTION], choose a state strategy separating server state, URL state, form state, and UI state. Output: decision matrix, chosen tools with rationale, sample store/query code in TypeScript, and an anti-pattern list (global state creep, prop drilling, over-fetching).

### 94. Web Performance Budget
**Prompt**: Act as a web perf engineer fluent in Core Web Vitals (LCP, INP, CLS). For [SITE_TYPE], set perf budgets and design a monitoring plan using Lighthouse CI, WebPageTest, and RUM (CrUX/SpeedCurve). Output: budget table (metric, budget, critical path), optimization levers ranked by impact (image, JS, CSS, fonts, TTFB), and a CI gate configuration.

### 95. React Hook Refactor
**Prompt**: Act as a React expert fluent in the rules of hooks and React 19 features. Refactor this component [CODE_BLOCK] using custom hooks, `useMemo`/`useCallback` only where justified, `useEffect` cleanup, and `use` hook for promises. Remove derived-state bugs. Output: refactored component, extracted hooks, a before/after behavior table, and 3 common hook mistakes avoided.

### 96. CSS Architecture Scalable
**Prompt**: Act as a CSS architect who has owned design tokens at scale. For [DESIGN_SYSTEM], compare CSS Modules, Tailwind, CSS-in-JS (Vanilla Extract, Panda), and Open Props. Cover tokens, theming (light/dark), spacing scale, and build output size. Output: decision matrix, chosen approach with ADR, token schema in JSON, and a migration plan from current CSS.

### 97. Web Accessibility Audit
**Prompt**: Act as a certified accessibility engineer (IAAP CPACC). Audit [PAGE] against WCAG 2.2 AA: keyboard, focus management, ARIA roles/states, contrast, semantic landmarks, form labels, and live regions. Output: finding table (criterion, severity, evidence, fix), code patches in HTML/JSX, axe-core test config, and manual test script (keyboard-only walkthrough).

### 98. Frontend Build Optimization
**Prompt**: Act as a build engineer fluent in Vite, Turbopack, esbuild, and webpack. For [PROJECT] with [BUILD_TIME] and [BUNDLE_SIZE], optimize: code splitting, tree shaking, dynamic imports, module federation, and dep pre-bundling. Output: current vs target metrics, config snippets for the bundler, lever table ranked by impact/effort, and a regression-prevention plan (size-limit).

### 99. SSR Hydration Strategy
**Prompt**: Act as a rendering expert who has debugged hydration mismatches in the wild. For [APP] in [FRAMEWORK], decide between CSR, SSR, SSG, ISR, and RSC. Cover hydration cost, TTI vs TTFB trade-offs, island architecture (Astro/Qwik), and streaming. Output: decision tree, chosen strategy with rationale, route-level rendering table, and a debugging guide for hydration errors.

### 100. Frontend Testing Strategy
**Prompt**: Act as a frontend testing lead following Kent C. Dodds's testing trophy. For [APP] in [FRAMEWORK], design a test strategy: static (TS, ESLint), unit (Vitest), component (Testing Library), integration, E2E (Playwright), visual regression (Chromatic), and a11y (axe). Output: trophy ratio table, tooling choices with rationale, sample tests per level, and 5 anti-patterns to avoid (testing implementation details, etc.).

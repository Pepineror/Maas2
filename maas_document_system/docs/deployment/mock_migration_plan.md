# Mock to Real Migration Plan (Section F5)

This document outlines the steps to replace development mocks with production implementations.

## 1. Redmine Client
- **Current**: `RedmineExtractor` uses `RedmineClient` which connects to real API but might rely on mocks in tests.
- **Action**: Ensure `RedmineClient` handles Network Errors, Rate Limiting, and huge pagination in production.
- **Verification**: Run `tests/integration/test_redmine_real.py` (to be created) against a Staging Redmine instance.

## 2. API Authentication
- **Current**: `middleware/auth.py` with static secret check.
- **Action**: Integrate with an Identity Provider (Keycloak/Auth0) if single sign-on is required.
- **Verification**: Pen-test the JWT validation logic.

## 3. Workflow Execution
- **Current**: synchronous `workflow.run()` in background thread.
- **Action**: Move to a durable task queue (Celery or Agno's native async runner with storage).
- **Migration**:
  1. Setup Redis/Postgres for state.
  2. Update `api_openwebui.py` to push task to queue.
  3. Create Worker process consuming queue.

## 4. LLM Provider
- **Current**: Likely using `MockLLM` or direct API in dev.
- **Action**: Configure `LiteLLM` or Agno's Model router to use Production Keys and Tiered routing (Flash vs Pro).

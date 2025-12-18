# MAAS Production Manifest

## F1. Credentials & Secrets
Identify all confidential keys required for production.

| Variable Name | Description | Security Requirement |
|---|---|---|
| `MAAS_API_KEY_SECRET` | Master key for internal API access | Store in Secret Manager |
| `JWT_SECRET` | Signing key for JWT Tokens | Rotated quarterly, Secret Manager |
| `REDMINE_API_KEY` | Access key for Redmine API | Read-only permissions preferred |
| `LLM_API_KEY` | Key for Model Provider (OpenAI/Anthropic/Google) | Usage limits configured |
| `DB_PASSWORD` | Database user password | Only accessible by backend |
| `REDIS_PASSWORD` | Redis access password | Only accessible by backend |

## F2. External Services
Dependencies external to the cluster.

- **Redmine Instance**: `http://cidiia.uce.edu.do` (REST API)
- **OpenWebUI**: `http://openwebui-service:3000` (Callbacks)
- **Model Provider**: `https://api.openai.com` or similar.

## F3. Model Configuration (Production)
Defines the AI models for different tiers.

### Tier 1: Fast/Reasoning (Planner)
- **Model**: `gemini-1.5-flash` or `gpt-4o-mini`
- **Context Window**: 128k+
- **Usage**: Initial planning, quick checks.

### Tier 2: High Quality (Author/Reviewer)
- **Model**: `gemini-1.5-pro` or `claude-3-5-sonnet`
- **Context Window**: 200k+
- **Usage**: Drafting content, final review.

## F4. Infrastructure Requirements
Recommended resources for `maas-backend` and `maas-ui`.

| component | CPU | RAM | Storage |
|---|---|---|---|
| Backend | 2 vCPU | 4 GB | 20 GB (Logs/Temp) |
| UI | 1 vCPU | 1 GB | N/A |
| Redis | 1 vCPU | 2 GB | Persistence Enabled |
| VectorDB | 4 vCPU | 16 GB | High IOPS SSD |


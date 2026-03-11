# Contribution Requests

Structured requests for changes to Synthesis-Owned shared artifacts.

**Template:** `docs/templates/CONTRIBUTION_REQUEST_TEMPLATE.yaml`
**Schema:** `docs/schemas/contribution_request.schema.json`
**Validator:** `python scripts/validate_contribution_requests.py docs/contribution_requests`

## Rules
- One file per invention: `<INVENTION_ID>.yaml`
- `invention_id` in the file must match the filename
- Request IDs must be unique across all files
- Only the Synthesis Engineer applies these to shared artifacts

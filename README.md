# BCN ⇄ Fez fare tracker

Static GitHub Pages dashboard plus a scheduled GitHub Actions job that queries Ignav and commits fare history to `data/fares.json`.

## Setup
1. In **Settings → Secrets and variables → Actions → New repository secret**, add `IGNAV_API_KEY` with your Ignav API key. Never place the key in `index.html`, public files, or chat.
2. Open **Actions → Monitor BCN-Fez fares → Run workflow** once to test. The job also runs daily at 07:17 UTC.
3. Enable Pages under **Settings → Pages**, deploy from the `main` branch / root.
4. Inspect the first run's logs and `data/fares.json`. Adjust response mapping if Ignav's API schema differs.
5. Set a price threshold in the dashboard. The current threshold is browser-local and does not send email yet.

## Security
- Ignav key is only read from GitHub Actions secret `IGNAV_API_KEY`.
- The API request is server-side in Actions, with `X-Api-Key`.
- Only fare history and UI code are committed; never commit credentials.

## Current scope
- Daily cheapest-date search for BCN → FEZ, one adult, economy, 7-day stay, next 365 days.
- Fare history and CSV export.
- Round-trip itinerary details, alert delivery, and editable date/party settings remain follow-up work.

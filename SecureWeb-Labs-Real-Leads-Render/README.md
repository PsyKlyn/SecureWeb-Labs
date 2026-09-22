# SecureWeb Labs — Render + Discord Leads

This version makes the assessment form real. Form submissions are sent server-side
to a Discord channel through a Discord webhook.

## Deploy on Render

1. Push this folder to a private GitHub repository.
2. Create a Render Web Service from the repository.
3. Build command:
   `pip install -r requirements.txt`
4. Start command:
   `gunicorn app:app`
5. In Render → Environment, create:
   `DISCORD_WEBHOOK_URL`
6. Put your Discord webhook URL in that environment variable.
7. Deploy and test the form.

## Create the Discord webhook

In the Discord server/channel where you want leads:
Channel Settings → Integrations → Webhooks → New Webhook → Copy Webhook URL.

IMPORTANT:
- Never put the webhook URL in `index.html` or JavaScript.
- Never commit the webhook URL to GitHub.
- Keep it only in Render's environment variables.
- If the URL is ever exposed, regenerate/delete the webhook.

## Google Ads

After the form works:
- Add the Google Ads conversion tag.
- Fire the conversion event only after `/api/assessment` returns success.
- If you want a dedicated thank-you URL for conversion tracking, add one later.

## Lead flow

Google Ad → Landing page → Form → Flask backend → Discord webhook → Lead notification

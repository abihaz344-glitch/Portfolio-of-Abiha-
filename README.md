# Abiha Fatima — Portfolio (deploy-ready)

This is a lightweight, responsive, and animated portfolio for **Abiha Fatima**.
Features:
- Dark theme with colorful animated gradient + subtle wave.
- Overlay rain effect (CSS).
- Glassmorphism cards and tabs.
- Sections: Home, Skills, Projects, Education, Contact.
- Contact form wired for EmailJS (placeholders included).
- GitHub Actions workflow to deploy to Vercel (see below).

## Quick start (local)
1. Open `index.html` in your browser.
2. Edit `script.js` to set your EmailJS `serviceID`, `templateID`, and `publicKey` for the contact form.

## Deploy to Vercel (GitHub integration)
This repo includes an example GitHub Actions workflow at `.github/workflows/deploy.yml` that uses the Vercel CLI to trigger a deployment on push to `main`.

### Required repository secrets
- `VERCEL_TOKEN` — your Vercel token.
- `VERCEL_ORG_ID` — found in Vercel project settings.
- `VERCEL_PROJECT_ID` — found in Vercel project settings.

After adding secrets, push to `main` and the workflow will deploy.

## Notes
- Update the placeholder project links and GitHub URLs inside `index.html`.
- Replace EmailJS placeholders in `script.js` with your actual IDs.
- This is intentionally minimal (no frameworks) for fast loading and easy customization.

Enjoy — customize fonts, colors, and animations as you like!

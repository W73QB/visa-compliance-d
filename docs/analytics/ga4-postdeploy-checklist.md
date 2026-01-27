# GA4/GTM Post-Deploy Checklist

## GTM container
- GTM ID: GTM-N4JLPLC2
- Verify gtm.js loads on:
  - https://visafact.org/
  - https://visafact.org/ui/

## GA4 (Realtime)
- Measurement ID: G-6BLK7YFGMS
- Expected events:
  - page_view (home + /ui/)
  - run_check (after user clicks "Check Compliance")
  - select_visa / select_product (when dropdowns change)

## Manual steps
1. Open Chrome Incognito.
2. Disable ad blockers.
3. DevTools → Network → filter `gtm.js`.
4. Confirm request to `https://www.googletagmanager.com/gtm.js?id=GTM-N4JLPLC2`.
5. Tag Assistant Preview should detect container.
6. GA4 Realtime should show page_view within 1–2 minutes.

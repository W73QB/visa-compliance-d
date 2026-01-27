# Production Verification (2026-01-27)

## Header Check
```
permissions-policy: geolocation=(), microphone=(), camera=()
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
x-content-type-options: nosniff
report-to: {"group":"csp-endpoint","max_age":10886400,"endpoints":[{"url":"https://visafact.org/__cspreport"}]}
content-security-policy-report-only: default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data: https://www.google-analytics.com; connect-src 'self' https://www.google-analytics.com https://region1.google-analytics.com https://analytics.google.com https://www.googletagmanager.com; base-uri 'self'; frame-ancestors 'none'; object-src 'none'; report-to csp-endpoint
```

## GTM Marker Check

### Homepage (/)
```
<script>(function(){var e="GTM-N4JLPLC2";window.GTM_ID=e,window.dataLayer=window.dataLayer||[],window.trackEvent=function(e,t){if(!window.GTM_ID)return;window.dataLayer.push(Object.assign({event:e},t||{}))},function(e,t,n,s,o){e[s]=e[s]||[],e[s].push({"gtm.start":(new Date).getTime(),event:"gtm.js"});var a=t.getElementsByTagName(n)[0],i=t.createElement(n),r=s!="dataLayer"?"&l="+s:"";i.async=!0,i.src="https://www.googletagmanager.com/gtm.js?id="+o+r,a.parentNode.insertBefore(i,a)}(window,document,"script","dataLayer",e)})()</script>
```

### UI (/ui/)
```
<meta name="gtm-id" content="GTM-N4JLPLC2">
// Lightweight GTM bootstrap with opt-in ID (set via window.GTM_ID or <meta name="gtm-id">).
const meta = document.querySelector('meta[name="gtm-id"]');
w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
```

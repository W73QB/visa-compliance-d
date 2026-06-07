/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./ui/**/*.{html,js}",
        "./layouts/**/*.html",
        "./content/**/*.md"
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                // Token-matched hex values (mirror --vf-color-* in visafact.css).
                // Opacity modifiers (bg-accent/10 etc.) require raw hex, not CSS vars.
                "primary":          "#19335a",   // --vf-color-primary
                "primary-hover":    "#122645",   // --vf-color-primary-hover
                "accent":           "#d4a51e",   // --vf-color-accent
                "accent-hover":     "#b89118",   // --vf-color-accent-hover
                "background-light": "#faf8f5",   // --vf-color-paper
                "background-dark":  "#0f1419",
                "surface-light":    "#ffffff",   // --vf-color-surface
                "surface-dark":     "#1a232e",
                "border-soft":      "#e8e4df",   // --vf-color-line
                "border-dark":      "#2d3748",
                "success-green":    "#059669",   // --vf-color-success
                "warning-yellow":   "#d97706",   // --vf-color-warning
                "error-red":        "#dc2626",   // --vf-color-danger
                "unknown-gray":     "#6b7280",   // --vf-color-unknown
                "info-blue":        "#0369a1",   // --vf-color-info
                "text-primary":     "#151515",   // --vf-color-ink
                "text-secondary":   "#525252",   // --vf-color-text-secondary
            },
            fontFamily: {
                "display": ["'DM Serif Display'", "Georgia", "serif"],
                "body":    ["'Plus Jakarta Sans'", "system-ui", "sans-serif"]
            },
            borderRadius: {
                "DEFAULT": "0.5rem",
                "lg":  "var(--vf-radius-lg, 12px)",
                "xl":  "var(--vf-radius-xl, 16px)",
                "2xl": "20px",
            },
            boxShadow: {
                "sm":  "var(--vf-shadow-1, 0 1px 3px rgba(0,0,0,0.08))",
                "DEFAULT": "var(--vf-shadow-1, 0 1px 3px rgba(0,0,0,0.08))",
                "md":  "var(--vf-shadow-2, 0 4px 12px rgba(0,0,0,0.08))",
                "lg":  "var(--vf-shadow-2, 0 4px 12px rgba(0,0,0,0.08))",
                "xl":  "var(--vf-shadow-3, 0 8px 24px rgba(0,0,0,0.10))",
                "2xl": "var(--vf-shadow-3, 0 8px 24px rgba(0,0,0,0.10))",
                "none": "none",
            },
            transitionDuration: {
                "fast": "120ms",
                "base": "200ms",
                "slow": "350ms",
            },
            transitionTimingFunction: {
                "standard":   "cubic-bezier(0.2, 0.0, 0, 1)",
                "emphasized": "cubic-bezier(0.3, 0.0, 0, 1)",
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/container-queries'),
    ],
}

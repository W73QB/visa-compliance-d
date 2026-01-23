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
                "primary": "#1e3a5f",
                "primary-hover": "#152a45",
                "accent": "#c9a227",
                "accent-hover": "#b8921f",
                "background-light": "#faf8f5",
                "background-dark": "#0f1419",
                "surface-light": "#ffffff",
                "surface-dark": "#1a232e",
                "border-soft": "#e8e4df",
                "border-dark": "#2d3748",
                "success-green": "#059669",
                "warning-yellow": "#d97706",
                "error-red": "#dc2626",
                "unknown-gray": "#6b7280",
                "info-blue": "#0369a1",
                "text-primary": "#1a1a1a",
                "text-secondary": "#525252"
            },
            fontFamily: {
                "display": ["'DM Serif Display'", "Georgia", "serif"],
                "body": ["'Plus Jakarta Sans'", "system-ui", "sans-serif"]
            },
            borderRadius: {
                "DEFAULT": "0.5rem",
                "lg": "1rem",
                "xl": "1.5rem",
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/container-queries'),
    ],
}

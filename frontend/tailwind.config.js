 /** @type {import('tailwindcss').Config} */
 export default {
   content: [
     "./index.html",
     "./src/**/*.{js,ts,jsx,tsx}",
   ],
   theme: {
     extend: {
       colors: {
         // Base colors from design.md
         'bg-base': '#0d0d0d',
         'bg-elevated': '#141414',
         'bg-hover': '#1a1a1a',
         'fg-primary': '#e8e8e8',
         'fg-secondary': '#a0a0a0',
         'fg-muted': '#6a6a6a',
         'separator': '#2a2a2a',
         'border': '#2a2a2a',
         // Severity colors
         'sev-critical': '#dc2626',
         'sev-high': '#ea580c',
         'sev-medium': '#ca8a04',
         'sev-low': '#16a34a',
         'sev-info': '#3b82f6',
         // Status colors
         'status-success': '#16a34a',
         'status-warning': '#ca8a04',
         'status-error': '#dc2626',
         'status-info': '#3b82f6',
       },
       fontFamily: {
         'ui': ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
         'mono': ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
       },
       fontSize: {
         'xs': ['0.75rem', { lineHeight: '1.5' }],
         'sm': ['0.875rem', { lineHeight: '1.5' }],
         'base': ['1rem', { lineHeight: '1.6' }],
         'lg': ['1.125rem', { lineHeight: '1.6' }],
         'xl': ['1.25rem', { lineHeight: '1.5' }],
         '2xl': ['1.5rem', { lineHeight: '1.4' }],
         '3xl': ['1.875rem', { lineHeight: '1.3' }],
         '4xl': ['2.25rem', { lineHeight: '1.2' }],
       },
       spacing: {
         '0': '0',
         '1': '4px',
         '2': '8px',
         '3': '12px',
         '4': '16px',
         '5': '20px',
         '6': '24px',
         '8': '32px',
         '10': '40px',
         '12': '48px',
         '16': '64px',
       },
       borderRadius: {
         'none': '0',
         'sm': '4px',
         'md': '6px',
         'lg': '8px',
         'full': '9999px',
       },
       boxShadow: {
         // No shadows per design restrictions
         'none': 'none',
       },
       animation: {
         // Disabled animations per design restrictions
         'none': 'none',
       },
       transitionDuration: {
         '0': '0ms',
       },
     },
   },
   corePlugins: {
     // Disable animations that violate design restrictions
     animation: false,
     transitionProperty: false,
     transitionDuration: false,
     transitionTimingFunction: false,
     transitionDelay: false,
   },
   plugins: [],
 }

// Tailwind (Play CDN) configuration shared by all kiosk pages.
// Must be loaded immediately AFTER the cdn.tailwindcss.com script tag.
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "tertiary-fixed-dim": "#c8c6c6",
        "on-tertiary-container": "#656464",
        "primary-fixed-dim": "#c6c6c7",
        "secondary-fixed": "#e5e2e1",
        "on-tertiary": "#303030",
        "on-secondary-container": "#b7b5b4",
        "on-background": "#e2e2e2",
        "primary-fixed": "#e2e2e2",
        "on-secondary-fixed-variant": "#474746",
        "on-secondary": "#313030",
        "tertiary": "#ffffff",
        "on-secondary-fixed": "#1c1b1b",
        "on-surface": "#e2e2e2",
        "on-tertiary-fixed": "#1b1c1c",
        "surface-container": "#1f1f1f",
        "inverse-on-surface": "#303030",
        "surface-tint": "#c6c6c7",
        "tertiary-fixed": "#e4e2e1",
        "primary-container": "#e2e2e2",
        "surface-bright": "#393939",
        "primary": "#ffffff",
        "on-error": "#690005",
        "secondary-container": "#474746",
        "surface-container-high": "#2a2a2a",
        "on-surface-variant": "#c4c7c8",
        "surface-variant": "#353535",
        "outline-variant": "#444748",
        "background": "#131313",
        "on-primary-container": "#636565",
        "error-container": "#93000a",
        "surface-container-low": "#1b1b1b",
        "on-primary-fixed": "#1a1c1c",
        "surface": "#131313",
        "on-tertiary-fixed-variant": "#474747",
        "outline": "#8e9192",
        "surface-container-highest": "#353535",
        "tertiary-container": "#e4e2e1",
        "error": "#ffb4ab",
        "inverse-primary": "#5d5f5f",
        "surface-container-lowest": "#0e0e0e",
        "on-primary-fixed-variant": "#454747",
        "on-primary": "#2f3131",
        "secondary": "#c8c6c5",
        "surface-dim": "#131313",
        "inverse-surface": "#e2e2e2",
        "on-error-container": "#ffdad6",
        "secondary-fixed-dim": "#c8c6c5"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "md": "16px",
        "gutter": "24px",
        "xs": "4px",
        "xl": "40px",
        "margin-mobile": "20px",
        "xxl": "64px",
        "margin-desktop": "48px",
        "unit": "4px",
        "lg": "24px",
        "sm": "8px"
      },
      fontFamily: {
        "label-md": ["Source Serif 4"],
        "label-sm": ["Source Serif 4"],
        "body-lg": ["Source Serif 4"],
        "display-lg-mobile": ["EB Garamond"],
        "body-md": ["Source Serif 4"],
        "headline-md": ["EB Garamond"],
        "headline-sm": ["EB Garamond"],
        "display-lg": ["EB Garamond"]
      },
      fontSize: {
        "label-md": ["14px", { "lineHeight": "1.4", "letterSpacing": "0.05em", "fontWeight": "600" }],
        "label-sm": ["12px", { "lineHeight": "1.4", "letterSpacing": "0.03em", "fontWeight": "400" }],
        "body-lg": ["18px", { "lineHeight": "1.6", "fontWeight": "400" }],
        "display-lg-mobile": ["32px", { "lineHeight": "1.2", "letterSpacing": "-0.01em", "fontWeight": "500" }],
        "body-md": ["16px", { "lineHeight": "1.6", "fontWeight": "400" }],
        "headline-md": ["32px", { "lineHeight": "1.2", "fontWeight": "400" }],
        "headline-sm": ["24px", { "lineHeight": "1.3", "fontWeight": "400" }],
        "display-lg": ["48px", { "lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "500" }]
      }
    }
  }
};

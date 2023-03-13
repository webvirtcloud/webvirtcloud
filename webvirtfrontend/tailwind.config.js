// eslint-disable-next-line @typescript-eslint/no-var-requires
const colors = require('tailwindcss/colors');

module.exports = {
  content: ['./*.html', './src/**/*.css', './src/**/*.{ts,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        cyan: colors.cyan,
      },
      textColor: {
        body: 'var(--color-text-body)',
        alt: 'var(--color-text-alt)',
        alt2: 'var(--color-text-alt2)',
        'button-default': 'var(--color-text-button-default)',
        'button-disabled': 'var(--color-text-button-disabled)',
        'button-danger': 'var(--color-text-button-danger)',
      },
      backgroundColor: {
        body: 'var(--color-bg-body)',
        base: 'var(--color-bg-base)',
        alt: 'var(--color-bg-alt)',
        alt2: 'var(--color-bg-alt2)',

        'input-default': 'var(--color-bg-input-default)',
        'input-disabled': 'var(--color-bg-input-disabled)',

        'button-disabled': 'var(--color-bg-button-disabled)',

        'button-default': 'var(--color-bg-button-default)',
        'button-default-hover': 'var(--color-bg-button-default-hover)',
        'button-default-active': 'var(--color-bg-button-default-active)',

        'button-secondary': 'var(--color-bg-button-secondary)',
        'button-secondary-hover': 'var(--color-bg-button-secondary-hover)',

        'button-danger': 'var(--color-bg-button-danger)',
        'button-danger-hover': 'var(--color-bg-button-danger-hover)',

        'interactive-hover': 'var(--color-bg-interactive-hover)',

        'control-default': 'var(--color-bg-control-default)',
      },
      borderColor: {
        DEFAULT: 'var(--color-bg-alt2)',
        'input-default': 'var(--color-border-input-default)',
        'button-secondary': 'var(--color-border-button-secondary)',
        'button-secondary-active': 'var(--color-border-button-secondary-active)',
        'button-danger': 'var(--color-border-button-danger)',
        'button-danger-active': 'var(--color-border-button-danger-active)',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};

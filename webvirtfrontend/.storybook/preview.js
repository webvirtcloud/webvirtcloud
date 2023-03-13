import '../src/assets/css/tailwind.css';
import { themes } from '@storybook/theming';

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  darkMode: {
    classTarget: 'html',
    stylePreview: true,
    // Override the default dark theme
    dark: { ...themes.dark  },
    // Override the default light theme
    light: { ...themes.normal },
  },
}
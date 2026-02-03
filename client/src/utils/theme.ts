/**
 * Theme Utility Functions
 *
 * This file contains utilities for managing theme state and persistence
 */

export type Theme = 'light' | 'dark';

export const THEMES = {
  LIGHT: 'light' as Theme,
  DARK: 'dark' as Theme,
};

export const THEME_STORAGE_KEY = 'cvision-theme';

/**
 * Get the initial theme from localStorage or system preference
 */
export const getInitialTheme = (): Theme => {
  // Check localStorage first
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY) as Theme | null;
  if (storedTheme && (storedTheme === 'light' || storedTheme === 'dark')) {
    return storedTheme;
  }

  // Check system preference
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return THEMES.DARK;
  }

  return THEMES.LIGHT;
};

/**
 * Apply theme to document
 * Sets the theme-dark class on the body element
 */
export const applyTheme = (theme: Theme): void => {
  if (theme === THEMES.DARK) {
    document.body.classList.add('theme-dark');
  } else {
    document.body.classList.remove('theme-dark');
  }
  localStorage.setItem(THEME_STORAGE_KEY, theme);
};

/**
 * Toggle between light and dark theme
 */
export const toggleTheme = (currentTheme: Theme): Theme => {
  return currentTheme === THEMES.LIGHT ? THEMES.DARK : THEMES.LIGHT;
};


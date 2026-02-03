import { createContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import type { Theme } from '../utils/theme';
import { getInitialTheme, applyTheme, toggleTheme as toggleThemeUtil } from '../utils/theme';

export interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

// eslint-disable-next-line react-refresh/only-export-components
export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

/**
 * Theme Provider Component
 * Wrap your app with this provider to enable theme management
 */
export const ThemeProvider = ({ children }: ThemeProviderProps) => {
  const [theme, setTheme] = useState<Theme>(() => getInitialTheme());
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    // Apply theme on mount
    applyTheme(theme);

    // Remove preload class to enable transitions
    setTimeout(() => {
      document.body.classList.remove('preload');
      setIsInitialized(true);
    }, 100);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Only run on mount

  useEffect(() => {
    if (isInitialized) {
      applyTheme(theme);
    }
  }, [theme, isInitialized]);

  const toggleTheme = () => {
    setTheme((currentTheme) => toggleThemeUtil(currentTheme));
  };

  const value: ThemeContextType = {
    theme,
    setTheme,
    toggleTheme,
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

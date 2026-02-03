import { useContext } from 'react';
import { ThemeContext, type ThemeContextType } from '../contexts/ThemeContext';

/**
 * Hook to use theme context
 * Must be used within ThemeProvider
 */
export const useTheme = (): ThemeContextType => {
    const context = useContext(ThemeContext);
    if (context === undefined) {
        throw new Error('useTheme must be used within a ThemeProvider');
    }
    return context;
};


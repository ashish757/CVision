import { useTheme } from '../hooks/useTheme';
import { Moon, Sun} from 'lucide-react';

const ThemeToggle = ({icon = true}) => {
  const { theme, toggleTheme } = useTheme();

  if (icon)  return (
    <button
      onClick={toggleTheme}
      className={`flex items-center justify-center w-10 h-10 bg-primary/30 text-muted border border-border rounded-lg hover:bg-primary/10 hover:text-primary hover:border-primary transition-all hover:scale-105 active:scale-95`}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {theme === 'light' ? (
        <Moon className="w-5 h-5" />
      ) : (
        <Sun className="w-5 h-5" />
      )}
    </button>
  );

  return (
      <button
          onClick={toggleTheme}
          className={`w-full flex items-center space-x-3 px-4 py-3 text-muted hover:bg-primary/10 hover:text-primary rounded-lg transition-colors`}
          aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      >
        {theme === 'light' ? (
        <Moon className="w-5 h-5" />
        ) : (
        <Sun className="w-5 h-5" />
        )}

        <span>{theme  === 'light' ? "Dark Mode" : "Light Mode"}</span>
      </button>
  );




};

export default ThemeToggle;

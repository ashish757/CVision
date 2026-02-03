import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { ThemeProvider } from './contexts/ThemeContext'
import { store } from './redux/store'
import './index.css'
import App from './App.tsx'

// Add preload class to prevent transition flash on page load
document.body.classList.add('preload');

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider store={store}>
      <ThemeProvider>
        <App />
      </ThemeProvider>
    </Provider>
  </StrictMode>,
)

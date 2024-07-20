import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from '@/pages/App';
import { QueryClientProvider } from '@tanstack/react-query';
import queryClient from './services/queryClient';
import { ThemeProvider } from './services/ThemeProvider';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </ThemeProvider>
  </StrictMode>,
);

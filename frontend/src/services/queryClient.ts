import { QueryClient } from '@tanstack/react-query';
import axios from 'axios';

const getBaseUrl = () => {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5173';
  } else {
    return 'https://real-estate-map.eivindnesje.no';
  }
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: async ({ queryKey }) => {
        const [url] = queryKey;
        const baseUrl = getBaseUrl(); // Get base URL based on environment
        const { data } = await axios.get(`${baseUrl}/data/${url as string}`);
        return data;
      },
    },
  },
});

export default queryClient;

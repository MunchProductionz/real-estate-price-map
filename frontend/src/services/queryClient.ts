import { QueryClient } from '@tanstack/react-query';
import axios from 'axios';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: async ({ queryKey }) => {
        const [url] = queryKey;
        const { data } = await axios.get(
          `http://localhost:5173/data/${url as string}`,
        );
        return data;
      },
    },
  },
});

export default queryClient;

import { useState, useEffect } from 'react';

type Size = 'sm' | 'md' | 'lg' | 'xl' | '2xl';

const sizes: Record<Size, string> = {
  sm: '(min-width: 640px)',
  md: '(min-width: 768px)',
  lg: '(min-width: 1024px)',
  xl: '(min-width: 1280px)',
  '2xl': '(min-width: 1536px)',
};
const getMediaQuery = (size: Size): string => sizes[size];

const useMediaQuery = (size: Size) => {
  const query = getMediaQuery(size);
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }
    const listener = () => setMatches(media.matches);
    window.addEventListener('resize', listener);
    return () => window.removeEventListener('resize', listener);
  }, [matches, query]);

  return matches;
};

export default useMediaQuery;

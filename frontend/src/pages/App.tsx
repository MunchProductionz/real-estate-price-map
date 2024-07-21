import ModeToggle from '@/components/ModeToggle';
import { useQuery } from '@tanstack/react-query';
import { useEffect } from 'react';
import Map from '@/components/Map';

export default function App() {
  // const { data } = useQuery({
  //   queryKey: ['dummy_data.json'],
  // });

  // useEffect(() => {
  //   console.log(data);
  // }, [data]);

  return (
    <div className='m-8'>
      <ModeToggle />
      <Map />
    </div>
  );
}

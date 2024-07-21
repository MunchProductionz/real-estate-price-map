import Filters from '@/components/Filters';
import Map from '@/components/Map';
import { MapProvider } from '@/services/MapContext';

export default function App() {
  return (
    <MapProvider>
      <Filters />
      <Map />
    </MapProvider>
  );
}

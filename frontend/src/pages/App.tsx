import Filters from '@/components/Filters';
import Map from '@/components/Map';
import Sidebar from '@/components/Sidebar';
import { MapProvider } from '@/services/MapContext';

export default function App() {
  return (
    <MapProvider>
      <Sidebar>
        <Map />
      </Sidebar>
    </MapProvider>
  );
}

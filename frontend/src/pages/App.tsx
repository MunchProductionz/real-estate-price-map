import Map from '@/components/Map';
import { MapProvider } from '@/services/MapContext';
import Layout from './Layout';

export default function App() {
  return (
    <MapProvider>
      <Layout>
        <Map />
      </Layout>
    </MapProvider>
  );
}

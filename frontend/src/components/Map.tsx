import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { useQuery } from '@tanstack/react-query';
import { useEffect, useRef, useState } from 'react';

const containerStyle = {
  width: '100%',
  height: '100vh',
};

const center = {
  lat: 59.9,
  lng: 10.7,
};

const mapId = '42cab03dda42e877';

const ZOOM_THRESHOLD = 13; // Minimum zoom level to show labels

export default function MapComponent() {
  const mapRef = useRef<google.maps.Map | null>(null);
  const [markers, setMarkers] = useState<google.maps.Marker[]>([]);

  const { data: geoJsonData } = useQuery<any>({
    queryKey: ['postcodes.geojson'],
  });

  useEffect(() => {
    if (mapRef.current && geoJsonData) {
      try {
        mapRef.current!.data.addGeoJson(geoJsonData);
        mapRef.current!.data.setStyle({
          fillColor: 'black',
          fillOpacity: 0.05,
          strokeColor: 'black',
          strokeWeight: 0.5,
        });

        // Create markers for labels
        const newMarkers: google.maps.Marker[] = [];
        mapRef.current!.data.forEach((feature) => {
          const bounds = new google.maps.LatLngBounds();
          feature.getGeometry()?.forEachLatLng((latLng: google.maps.LatLng) => {
            bounds.extend(latLng);
          });
          const center = bounds.getCenter();
          const postnummer = feature.getProperty('postnummer') as string;

          const marker = new google.maps.Marker({
            position: center,
            map: mapRef.current,
            label: {
              text: postnummer,
              color: 'black',
              fontSize: '14px',
              fontWeight: 'bold',
            },
            icon: 'http://maps.google.com/mapfiles/ms/micons/blank.png', // Blank icon to avoid default markers
            visible: false, // Initially set markers to not visible
          });

          newMarkers.push(marker);
        });

        setMarkers(newMarkers);
      } catch (error) {
        console.error('Error adding GeoJSON to map:', error);
      }
    }
  }, [geoJsonData]);

  useEffect(() => {
    const map = mapRef.current;
    if (map) {
      const handleZoomChange = () => {
        const zoom = map.getZoom();
        if (!zoom) return;
        markers.forEach((marker) => {
          marker.setMap(zoom >= ZOOM_THRESHOLD ? map : null);
        });
      };

      const updateMarkersVisibility = () => {
        if (!map) return;
        const bounds = map.getBounds();
        if (!bounds) return;

        markers.forEach((marker) => {
          const position = marker.getPosition();
          const zoom = map.getZoom();
          if (!zoom) return;
          if (position) {
            marker.setVisible(bounds.contains(position) && zoom >= ZOOM_THRESHOLD);
          }
        });
      };

      // Add zoom change listener
      const zoomListener = google.maps.event.addListener(map, 'zoom_changed', () => {
        handleZoomChange();
        updateMarkersVisibility();
      });

      // Add bounds change listener to update marker visibility based on viewport
      const boundsListener = google.maps.event.addListener(map, 'bounds_changed', updateMarkersVisibility);

      // Initial call to set visibility based on the current zoom level and viewport
      handleZoomChange();
      updateMarkersVisibility();

      return () => {
        // Clean up listeners on component unmount
        google.maps.event.removeListener(zoomListener);
        google.maps.event.removeListener(boundsListener);
      };
    }
  }, [markers]);

  return (
    <LoadScript googleMapsApiKey='AIzaSyBTtRSxC4endO-vpel6LKkHzDAGt4F1oN8'>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={11}
        options={{ mapId }}
        onLoad={(map) => {
          mapRef.current = map;
          console.log('Map loaded');
        }}
      >
        {/* Child components, such as markers, info windows, etc. */}
      </GoogleMap>
    </LoadScript>
  );
}

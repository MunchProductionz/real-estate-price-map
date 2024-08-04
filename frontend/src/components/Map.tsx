import { useMap } from '@/services/MapContext';
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { useQuery } from '@tanstack/react-query';
import { useEffect, useRef, useState } from 'react';

const ZOOM_THRESHOLD = 15; // Minimum zoom level to show labels

export default function MapComponent() {
  const mapRef = useRef<google.maps.Map | null>(null);
  const [markers, setMarkers] = useState<google.maps.Marker[]>([]);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const { maxPrice, squareMeters } = useMap();

  const { data: geoJsonData } = useQuery<any>({
    queryKey: ['postcodes.json'],
  });

  useEffect(() => {
    if (mapRef.current && geoJsonData && isMapLoaded) {
      try {
        setTimeout(() => {
          const map = mapRef.current!;

          // Clear existing data to avoid stacking styles
          map.data.forEach((feature) => {
            map.data.remove(feature);
          });

          map.data.addGeoJson(geoJsonData);
          map.data.setStyle((feature) => {
            const averagePrice = feature.getProperty(
              'averagePrice' + squareMeters + 'm2',
            ) as number;
            if (maxPrice > averagePrice) {
              // Affordability check
              if (maxPrice > averagePrice * 1.2) {
                // 20% buffer for high affordability (potential bidding war)
                return {
                  fillColor: 'RoyalBlue', // #4169E1
                  fillOpacity: 0.3,
                  strokeColor: 'MidnightBlue', // #191970
                  strokeWeight: 0.1,
                };
              } else {
                return {
                  fillColor: 'Salmon', // #FA8072
                  fillOpacity: 0.3,
                  strokeColor: 'Maroon', // #800000
                  strokeWeight: 0.1,
                };
              }
            } else {
              return {
                fillColor: 'black', // #000000
                fillOpacity: 0.5,
                strokeColor: 'black', // #000000
                strokeWeight: 0.1,
              };
            }
          });

          // Create markers for labels
          const newMarkers: google.maps.Marker[] = [];
          map.data.forEach((feature) => {
            const bounds = new google.maps.LatLngBounds();
            feature
              .getGeometry()
              ?.forEachLatLng((latLng: google.maps.LatLng) => {
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
        }, 500); // Adjust the delay time as needed
      } catch (error) {
        console.error('Error adding GeoJSON to map:', error);
      }
    }
  }, [geoJsonData, isMapLoaded, maxPrice, squareMeters]);

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
            marker.setVisible(
              bounds.contains(position) && zoom >= ZOOM_THRESHOLD,
            );
          }
        });
      };

      // Add zoom change listener
      const zoomListener = google.maps.event.addListener(
        map,
        'zoom_changed',
        () => {
          handleZoomChange();
          updateMarkersVisibility();
        },
      );

      // Add bounds change listener to update marker visibility based on viewport
      const boundsListener = google.maps.event.addListener(
        map,
        'bounds_changed',
        updateMarkersVisibility,
      );

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
    <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        mapContainerStyle={{
          width: '100%',
          height: '100%',
        }}
        center={{
          lat: 59.93,
          lng: 10.75,
        }}
        zoom={11}
        options={{ mapId: import.meta.env.VITE_GOOGLE_MAP_ID }}
        onLoad={(map) => {
          mapRef.current = map;
          setIsMapLoaded(true);
        }}
      >
        {/* Child components, such as markers, info windows, etc. */}
      </GoogleMap>
    </LoadScript>
  );
}

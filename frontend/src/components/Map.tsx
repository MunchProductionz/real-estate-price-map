import { LocationDirectory, NearestLocation } from '@/lib/types/distanceData';
import { useMap } from '@/services/MapContext';
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { useQuery } from '@tanstack/react-query';
import { useEffect, useRef, useState } from 'react';

export default function MapComponent() {
  const ZOOM_THRESHOLD = 15; // Minimum zoom level to show labels
  const mapCenterRef = useRef<{ lat: number; lng: number }>({
    lat: 59.93,
    lng: 10.75,
  });
  const mapRef = useRef<google.maps.Map | null>(null);
  const [markers, setMarkers] = useState<google.maps.Marker[]>([]);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const {
    maxPrice,
    squareMeters,
    filters,
    selectedPostcode,
    selectedPostcodeRef,
    setSelectedPostcode,
  } = useMap();

  const { data: geoJsonData } = useQuery<any>({
    queryKey: ['postcodes.json'],
  });

  const { data: distanceData } = useQuery<LocationDirectory>({
    queryKey: ['distance_data.json'],
  });

  function setColor({ feature }: { feature: google.maps.Data.Feature }) {
    const averagePrice = feature.getProperty(
      'averagePrice' + squareMeters + 'm2',
    ) as number;

    const nearestLocation =
      distanceData?.[feature.getProperty('postnummer') as string]
        .nearest_location;
    let filtered = false;

    if (nearestLocation) {
      // Define specific keys using keyof
      const locationKeys: Array<keyof NearestLocation> = [
        'vinmonopolet',
        'shopping_mall',
      ];

      // Iterate over location keys
      for (const location of locationKeys) {
        const travelData = nearestLocation[location].travel_data;

        let maxDistance = Infinity;
        let maxTime = Infinity;
        let travelMethod = 'driving';
        if (filters[location]?.active) {
          maxDistance = filters[location]?.maxDistance ?? Infinity;
          maxTime = filters[location]?.maxTime ?? Infinity;
          travelMethod = filters[location]?.mode ?? 'driving';
        }

        const distance =
          (travelData[travelMethod as 'walking' | 'driving']?.distance
            .kilometers ?? 0) < maxDistance;
        const time =
          (travelData[travelMethod as 'walking' | 'driving']?.duration
            .minutes ?? 0) < maxTime;

        if (!distance || !time) filtered = true;
      }
    }

    if (maxPrice > averagePrice && !filtered) {
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
  }

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
            return setColor({ feature });
          });
          map.data.addListener(
            'click',
            (event: google.maps.Data.MouseEvent) => {
              const postcode = event.feature.getProperty(
                'postnummer',
              ) as string;
              if (postcode === selectedPostcodeRef.current) {
                setSelectedPostcode(null);
                map.data.revertStyle();
                return;
              }
              setSelectedPostcode(postcode);
              map.data.revertStyle();
              map.data.overrideStyle(event.feature, {
                fillColor: 'DarkGray', // #A9A9A9
                fillOpacity: 0.3,
                zIndex: 2,
              });
            },
          );

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
  }, [geoJsonData, isMapLoaded, maxPrice, squareMeters, filters]);

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

  useEffect(() => {
    const map = mapRef.current;
    if (map) {
      // Update mapCenterRef when the map is moved
      const centerChangeListener = google.maps.event.addListener(
        map,
        'center_changed',
        () => {
          const center = map.getCenter();
          if (center) {
            mapCenterRef.current = { lat: center.lat(), lng: center.lng() };
          }
        },
      );

      return () => {
        // Clean up the center change listener on unmount
        google.maps.event.removeListener(centerChangeListener);
      };
    }
  }, []);

  return (
    <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        mapContainerStyle={{
          width: '100%',
          height: 'calc(100vh - 56px)',
        }}
        center={mapCenterRef.current}
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

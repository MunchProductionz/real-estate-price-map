import { NearestLocation } from '@/lib/types/distanceData';
import { useMap } from '@/services/MapContext';
import { GoogleMap, LoadScript } from '@react-google-maps/api';
import { useEffect, useRef, useState } from 'react';

export default function MapComponent() {
  const {
    maxPrice,
    squareMeters,
    filters,
    selectedPostcodeRef,
    geoJsonData,
    distanceData,
    city,
    cityCenters,
    setSelectedPostcode,
    setFilterView,
  } = useMap();
  const mapCenterRef = useRef<{ lat: number; lng: number }>({
    lat: 59.93,
    lng: 10.75,
  });
  const mapRef = useRef<google.maps.Map | null>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const geoJsonAdded = useRef(false); // Flag to track if GeoJSON is already added

  function setColor({ feature }: { feature: google.maps.Data.Feature }) {
    const map = mapRef.current!;
    map.data.revertStyle(feature);

    const averagePrice = feature.getProperty(
      'averagePrice' + squareMeters + 'm2',
    ) as number;

    let nearestLocation = null;
    let filtered = false;
    if (city === 'oslo') {
      nearestLocation =
        distanceData?.[feature.getProperty('postnummer') as string]
          ?.nearest_location;
    }

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

          if (!geoJsonAdded.current) {
            map.data.addGeoJson(geoJsonData);

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
                setFilterView(false);
                map.data.revertStyle();
                map.data.overrideStyle(event.feature, {
                  fillColor: 'DarkGray', // #A9A9A9
                  fillOpacity: 0.3,
                  zIndex: 2,
                });
              },
            );
            geoJsonAdded.current = true;
          }

          map.data.setStyle((feature) => {
            return setColor({ feature });
          });
        }, 500); // Adjust the delay time as needed
      } catch (error) {
        console.error('Error adding GeoJSON to map:', error);
      }
    }
  }, [geoJsonData, isMapLoaded, maxPrice, squareMeters, filters, city]);

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

  useEffect(() => {
    const map = mapRef.current;
    if (map && cityCenters) {
      map.setCenter({
        lat: cityCenters[city].lat,
        lng: cityCenters[city].lng,
      });
    }
  }, [cityCenters, city]);

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
      ></GoogleMap>
    </LoadScript>
  );
}

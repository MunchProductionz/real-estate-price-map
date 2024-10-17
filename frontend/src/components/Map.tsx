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

  function setColor({ feature }: { feature: google.maps.Data.Feature }) {
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
      const locationKeys: Array<keyof NearestLocation> = [
        'vinmonopolet',
        'shopping_mall',
      ];

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
      if (maxPrice > averagePrice * 1.2) {
        return {
          fillColor: 'RoyalBlue',
          fillOpacity: 0.3,
          strokeColor: 'MidnightBlue',
          strokeWeight: 0.1,
        };
      } else {
        return {
          fillColor: 'Salmon',
          fillOpacity: 0.3,
          strokeColor: 'Maroon',
          strokeWeight: 0.1,
        };
      }
    } else {
      return {
        fillColor: 'black',
        fillOpacity: 0.5,
        strokeColor: 'black',
        strokeWeight: 0.1,
      };
    }
  }

  useEffect(() => {
    console.log(geoJsonData);
    console.log(mapRef.current);
    console.log(isMapLoaded);
    if (mapRef.current && geoJsonData && isMapLoaded) {
      try {
        const map = mapRef.current!;
        map.data.forEach((feature) => {
          map.data.remove(feature);
        });
        map.data.addGeoJson(geoJsonData);

        google.maps.event.clearListeners(map.data, 'click');
        map.data.addListener('click', (event: google.maps.Data.MouseEvent) => {
          const postcode = event.feature.getProperty('postnummer') as string;
          map.data.revertStyle();
          if (postcode === selectedPostcodeRef.current) {
            setSelectedPostcode(null);
          } else {
            setSelectedPostcode(postcode);
            setFilterView(false);
            map.data.overrideStyle(event.feature, {
              fillColor: 'DarkGray',
              fillOpacity: 0.3,
              zIndex: 2,
            });
          }
        });
      } catch (error) {
        console.error('Error adding GeoJSON to map:', error);
      }
    }
  }, [geoJsonData, isMapLoaded]);

  useEffect(() => {
    if (mapRef.current && isMapLoaded) {
      const map = mapRef.current!;
      map.data.setStyle((feature) => setColor({ feature }));
    }
  }, [maxPrice, squareMeters, filters, city, distanceData]);

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
      >
        {/* Child components, such as markers, info windows, etc. */}
      </GoogleMap>
    </LoadScript>
  );
}

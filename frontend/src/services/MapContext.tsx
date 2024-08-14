import { Feature, GeoJsonData } from '@/lib/types/GeoJsonData';
import { CityCentrums } from '@/lib/types/cityCentrums';
import { LocationDirectory, PostalCodeEntry } from '@/lib/types/distanceData';
import { useQuery } from '@tanstack/react-query';
import {
  Context,
  Dispatch,
  MutableRefObject,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react';

interface DistanceFilter {
  mode: 'driving | walking';
  maxDistance: number;
  maxTime: number;
  active: boolean;
}

interface Filters {
  vinmonopolet?: DistanceFilter;
  shopping_mall?: DistanceFilter;
}

type City =
  | 'bergen'
  | 'bodo'
  | 'drammen'
  | 'kristiansand'
  | 'oslo'
  | 'stavanger'
  | 'tromso'
  | 'trondheim';

export type MapContextType = {
  equity: number;
  debt: number;
  income: number;
  extraLoan: number;
  squareMeters: number;
  maxPrice: number;
  filters: Filters;
  selectedPostcode: string | null;
  selectedPostcodeRef: MutableRefObject<string | null>;
  geoJsonData: any;
  distanceData: LocationDirectory | undefined;
  selectedFeature: Feature | undefined;
  selectedDistance: PostalCodeEntry | undefined;
  city: City;
  cityCentrums?: CityCentrums;
  setEquity: Dispatch<SetStateAction<number>>;
  setDebt: Dispatch<SetStateAction<number>>;
  setIncome: Dispatch<SetStateAction<number>>;
  setExtraLoan: Dispatch<SetStateAction<number>>;
  setSquareMeters: Dispatch<SetStateAction<number>>;
  setFilters: Dispatch<SetStateAction<Filters>>;
  setCity: Dispatch<SetStateAction<City>>;
  setSelectedPostcode: (data: string | null) => void;
};

const MapContext: Context<MapContextType> = createContext({} as MapContextType);

export function MapProvider({ children }: { children: React.ReactNode }) {
  const [equity, setEquity] = useState(0);
  const [income, setIncome] = useState(400000);
  const [debt, setDebt] = useState(0);
  const [extraLoan, setExtraLoan] = useState(0);
  const [squareMeters, setSquareMeters] = useState(60);
  const [maxPrice, setMaxPrice] = useState(0);
  const [filters, setFilters] = useState<Filters>({});
  const [selectedPostcode, _setSelectedPostcode] = useState<string | null>(
    null,
  );
  const [selectedFeature, setSelectedFeature] = useState<Feature | undefined>();
  const [selectedDistance, setSelectedDistance] = useState<
    PostalCodeEntry | undefined
  >();
  const [city, setCity] = useState<City>('oslo');

  const { data: geoJsonData } = useQuery<GeoJsonData>({
    queryKey: [`postcodes_finalized/postcodes_${city}.json`],
  });

  const { data: distanceData } = useQuery<LocationDirectory>({
    queryKey: ['distance_data.json'],
  });

  const { data: cityCentrums } = useQuery<CityCentrums>({
    queryKey: ['city_centrums.json'],
  });

  const selectedPostcodeRef = useRef(selectedPostcode);
  const setSelectedPostcode = (data: string | null) => {
    selectedPostcodeRef.current = data;
    _setSelectedPostcode(data);
    const feature = geoJsonData?.features.find(
      (feature) => feature.properties.postnummer === data,
    );
    setSelectedFeature(feature);
    const selectedDistance = data ? distanceData?.[data] : undefined;
    setSelectedDistance(selectedDistance);
  };

  useEffect(() => {
    setMaxPrice(equity + income * 5 - debt + extraLoan);
  }, [equity, income, debt, extraLoan]);

  return (
    <MapContext.Provider
      value={{
        equity,
        debt,
        income,
        extraLoan,
        squareMeters,
        maxPrice,
        filters,
        selectedPostcode,
        selectedPostcodeRef,
        geoJsonData,
        distanceData,
        selectedFeature,
        selectedDistance,
        city,
        cityCentrums,
        setEquity,
        setDebt,
        setIncome,
        setExtraLoan,
        setSquareMeters,
        setFilters,
        setSelectedPostcode,
        setCity,
      }}
    >
      {children}
    </MapContext.Provider>
  );
}

export const useMap = () => useContext<MapContextType>(MapContext);

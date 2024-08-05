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
  setEquity: Dispatch<SetStateAction<number>>;
  setDebt: Dispatch<SetStateAction<number>>;
  setIncome: Dispatch<SetStateAction<number>>;
  setExtraLoan: Dispatch<SetStateAction<number>>;
  setSquareMeters: Dispatch<SetStateAction<number>>;
  setFilters: Dispatch<SetStateAction<Filters>>;
  // _setSelectedPostcode: Dispatch<SetStateAction<string | null>>;
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

  const selectedPostcodeRef = useRef(selectedPostcode);
  const setSelectedPostcode = (data: string | null) => {
    selectedPostcodeRef.current = data;
    _setSelectedPostcode(data);
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
        setEquity,
        setDebt,
        setIncome,
        setExtraLoan,
        setSquareMeters,
        setFilters,
        setSelectedPostcode,
      }}
    >
      {children}
    </MapContext.Provider>
  );
}

export const useMap = () => useContext<MapContextType>(MapContext);

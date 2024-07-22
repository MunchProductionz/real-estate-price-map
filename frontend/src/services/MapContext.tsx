import { Context, Dispatch, SetStateAction, createContext, useContext, useEffect, useState } from 'react';

export type MapContextType = {
  equity: number;
  debt: number;
  income: number;
  extraLoan: number;
  squareMeters: number;
  maxPrice: number;
  setEquity: Dispatch<SetStateAction<number>>;
  setDebt: Dispatch<SetStateAction<number>>;
  setIncome: Dispatch<SetStateAction<number>>;
  setExtraLoan: Dispatch<SetStateAction<number>>;
  setSquareMeters: Dispatch<SetStateAction<number>>;
};

const MapContext: Context<MapContextType> = createContext({} as MapContextType);

export function MapProvider({ children }: { children: React.ReactNode }) {
  const [equity, setEquity] = useState(0);
  const [income, setIncome] = useState(400000);
  const [debt, setDebt] = useState(0);
  const [extraLoan, setExtraLoan] = useState(0);
  const [squareMeters, setSquareMeters] = useState(60);
  const [maxPrice, setMaxPrice] = useState(0);

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
        setEquity,
        setDebt,
        setIncome,
        setExtraLoan,
        setSquareMeters,
      }}
    >
      {children}
    </MapContext.Provider>
  );
}

export const useMap = () => useContext<MapContextType>(MapContext);

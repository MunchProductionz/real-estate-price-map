import { useMap } from '@/services/MapContext';
import { Input } from './shadcn/ui/input';
import { Label } from './shadcn/ui/label';
import { Slider } from './shadcn/ui/slider';

export default function Inputs() {
  const {
    equity,
    debt,
    income,
    extraLoan,
    squareMeters,
    setEquity,
    setDebt,
    setIncome,
    setExtraLoan,
    setSquareMeters,
  } = useMap();
  const maxPrice = equity + 5 * income - debt + extraLoan;

  // Function to format numbers with spaces
  const formatNumberWithSpaces = (num: number): string => {
    if (num === 0) return '';
    return num.toLocaleString('nb-NO');
  };

  // Function to remove spaces and parse number
  const parseNumber = (value: string): number => {
    const cleaned = value.replace(/\s/g, '');
    // Parse as an integer, fallback to 0 if NaN
    return parseInt(cleaned, 10) || 0;
  };

  // Handler to prevent input that leads to NaN
  const handleInputChange =
    (setter: React.Dispatch<React.SetStateAction<number>>) =>
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const input = e.target.value;
      setter(parseNumber(input));
    };
  return (
    <div className='flex w-full flex-col items-center gap-4 p-4'>
      <div className='w-full space-y-1'>
        <Label>Egenkapital</Label>
        <Input
          type='text'
          placeholder='Egenkapital'
          value={formatNumberWithSpaces(equity)}
          onChange={handleInputChange(setEquity)}
        />
      </div>
      <div className='w-full'>
        <Label>Ekstra lån gjennom familie</Label>
        <Input
          type='text'
          placeholder='Ekstra lån'
          value={formatNumberWithSpaces(extraLoan)}
          onChange={handleInputChange(setExtraLoan)}
        />
      </div>
      <div className='w-full space-x-1 space-y-3'>
        <Label>Lønn</Label>
        <Label>{formatNumberWithSpaces(income)}</Label>
        <Slider
          defaultValue={[400000]}
          max={2000000}
          step={50000}
          onValueChange={(e: number[]) => setIncome(e[0])}
        />
      </div>
      <div className='w-full'>
        <Label>Eksisterende gjeld</Label>
        <Input
          type='text'
          placeholder='Eksisterende gjeld'
          value={formatNumberWithSpaces(debt)}
          onChange={handleInputChange(setDebt)}
        />
      </div>
      <div className='w-full space-x-1 space-y-3'>
        <Label>Kvadratmeter </Label>
        <Label>{formatNumberWithSpaces(squareMeters)}</Label>
        <Slider
          defaultValue={[60]}
          max={200}
          min={20}
          step={10}
          onValueChange={(e: number[]) => setSquareMeters(e[0])}
        />
      </div>
      <div className='w-full space-x-1'>
        <Label>Maksimal Kjøpssum</Label>
        <Label>{formatNumberWithSpaces(maxPrice)}</Label>
      </div>
    </div>
  );
}

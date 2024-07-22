import { useMap } from '@/services/MapContext';
import ModeToggle from './ModeToggle';
import { Input } from './shadcn/ui/input';
import { Label } from './shadcn/ui/label';
import { Slider } from './shadcn/ui/slider';

export default function Filters() {
  const { equity, debt, income, extraLoan, squareMeters, setEquity, setDebt, setIncome, setExtraLoan, setSquareMeters } = useMap();
  const maxPrice = equity + 5 * income - debt + extraLoan
  return (
    <div className='m-4 flex justify-between'>
      <div className='flex flex-col gap-2'>
        <Label className='ml-2'>Eiendeler</Label>
        <Input
          type='number'
          placeholder='Eiendeler'
          value={equity}
          onChange={(e) => setEquity(parseInt(e.target.value))}
        />
      </div>
      <div className='flex w-2/6 flex-col gap-2'>
        <div>
          <Label className='ml-2'>Lønn</Label>
          <Label className='ml-2'>{income.toLocaleString()}</Label>
        </div>
        <Slider defaultValue={[400000]} max={2000000} step={50000} onValueChange={(e) => setIncome(e[0])} />
        <div>
          <Label className='ml-2'>Ekstra lån</Label>
          <Input type='number' placeholder='Ekstra lån' value={extraLoan} onChange={(e) => setExtraLoan(parseInt(e.target.value))} />
        </div>
      </div>
      <div className='flex flex-col gap-2'>
        <div>
          <Label className='ml-2'>Gjeld</Label>
          <Input type='number' placeholder='Gjeld' value={debt} onChange={(e) => setDebt(parseInt(e.target.value))} />
        </div>
        <div>
          <Label className='ml-2'>Maksimal Kjøpssum</Label>
          <Label className='ml-2'>{maxPrice.toLocaleString()}</Label> 
        </div>
      </div>
      <div className='flex flex-col gap-2'>
        <div>
          <Label className='ml-2'>Kvadratmeter</Label>
          <Label className='ml-2'>{squareMeters.toLocaleString()}</Label>
        </div>
        <Slider defaultValue={[60]} max={200} min={20} step={10} onValueChange={(e) => setSquareMeters(e[0])} />
      </div>
      <ModeToggle />
    </div>
  );
}

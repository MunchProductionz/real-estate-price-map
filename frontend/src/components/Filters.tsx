import { cn } from '@/lib/utils';
import { Car, LucideIcon, ShoppingCart, Wine, X } from 'lucide-react';
import { Dispatch, SetStateAction, useEffect, useState } from 'react';
import { Button } from './shadcn/ui/button';
import { Checkbox } from './shadcn/ui/checkbox';
import { Switch } from './shadcn/ui/switch';
import { FaPersonWalking } from 'react-icons/fa6';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from './shadcn/ui/select';
import { Input } from './shadcn/ui/input';
import useMediaQuery from '@/lib/hooks/useMediaQueries';
import { useMap } from '@/services/MapContext';

function Filter({
  Icon,
  name,
  displayName,
}: {
  Icon: LucideIcon;
  name: string;
  displayName: string;
}) {
  const [checked, setChecked] = useState(false);
  const [selectedValue, setSelectedValue] = useState('walking');
  const [maxDistance, setMaxDistance] = useState(Infinity);
  const [maxTime, setMaxTime] = useState(Infinity);
  const { setFilters } = useMap();

  useEffect(() => {
    setFilters((prev) => ({
      ...prev,
      [name]: {
        type: selectedValue,
        maxDistance: maxDistance,
        maxTime: maxTime,
        active: checked,
      },
    }));
  }, [checked, selectedValue, maxDistance, maxTime]);
  const formatNumber = (num: number): string => {
    if (num === 0 || num === Infinity) return '';
    return num.toString();
  };
  return (
    <div className='flex items-end gap-2 p-2'>
      <div className='m-2 flex w-36 items-center gap-1 text-lg'>
        <Icon />
        {displayName}
      </div>
      <Switch
        className='m-2'
        checked={checked}
        onCheckedChange={() => setChecked((prev) => !prev)}
      />
      <Select value={selectedValue} onValueChange={setSelectedValue}>
        <SelectTrigger className='w-32'>
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel>Fremkostmidler</SelectLabel>
            <SelectItem value='driving'>
              <div className='flex gap-2 text-base'>
                <Car />
                Bil
              </div>
            </SelectItem>
            <SelectItem value='walking'>
              <div className='flex gap-2 text-base'>
                <FaPersonWalking />
                Gå
              </div>
            </SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
      <div>
        Max km:
        <Input
          type='text'
          placeholder='Distanse'
          className='w-32 text-lg'
          value={formatNumber(maxDistance)}
          onChange={(e) => setMaxDistance(parseInt(e.target.value) || Infinity)}
        />
      </div>
      <div>
        Max minutter:
        <Input
          type='text'
          placeholder='Tid'
          className='w-32 text-lg'
          value={formatNumber(maxTime)}
          onChange={(e) => setMaxTime(parseInt(e.target.value) || Infinity)}
        />
      </div>
    </div>
  );
}

export default function Filters({
  filterView,
  expanded,
  setFilterView,
}: {
  filterView: boolean;
  expanded: boolean;
  setFilterView: Dispatch<SetStateAction<boolean>>;
}) {
  return (
    <div
      className={cn(
        'fixed bottom-0 m-2 overflow-hidden bg-background transition-all duration-300',
        filterView
          ? // ? expanded
            //   ? 'ml-2 w-[calc(100vw-272px)] md:w-[60vw]'
            //   : 'ml-2 w-[calc(100vw-16px)] md:w-[690px]'
            'ml-2 w-[700px]'
          : 'ml-0 w-0',
      )}
    >
      <div
        // className={cn(

        //   'p-2 md:w-[680px]',
        //   expanded ? 'w-[calc(100vw-272px)]' : 'w-[calc(100vw-16px)]',
        // )}
        className='w-[700px] p-2'
      >
        <div className='flex justify-between'>
          <div className='text-xl font-semibold'>Filter</div>
          <Button
            size='icon'
            variant='ghost'
            onClick={() => setFilterView((prev) => !prev)}
          >
            <X strokeWidth='3px' />
          </Button>
        </div>
        <div className=''>
          <Filter Icon={Wine} name='vinmonopolet' displayName='Vinmonopolet' />
          <Filter
            Icon={ShoppingCart}
            name='shopping_mall'
            displayName='Kjøpesenter'
          />
        </div>
      </div>
    </div>
  );
}

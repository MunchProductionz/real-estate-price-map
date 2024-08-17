import { cn } from '@/lib/utils';
import { useMap } from '@/services/MapContext';
import { Menu } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';
import ModeToggle from './ModeToggle';
import { Button } from './shadcn/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from './shadcn/ui/dropdown-menu';
import { City } from '@/lib/types/cityCenters';

export default function Navbar({
  setExpanded,
}: {
  expanded: boolean;
  setExpanded: Dispatch<SetStateAction<boolean>>;
}) {
  const { city, cityCenters, setCity } = useMap();
  return (
    <div className='sticky bottom-1 top-0 z-40 flex h-14 items-center justify-between border bg-background p-2 shadow'>
      <Button
        size='icon'
        variant='ghost'
        // className={cn('fixed top-2 transition-all duration-300')}
        onClick={() => setExpanded((prev) => !prev)}
      >
        <Menu strokeWidth={'3px'} />
      </Button>
      <DropdownMenu>
        <DropdownMenuTrigger asChild className={cn('')}>
          <Button variant='outline'>
            <span className='capitalize'>{city}</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          {Object.entries(cityCenters ?? {}).map(([cityName]) => (
            <DropdownMenuItem
              key={cityName}
              onClick={() => setCity(cityName as City)}
              className='capitalize'
            >
              {cityName}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
      <ModeToggle />
    </div>
  );
}

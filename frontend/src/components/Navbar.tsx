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
import { cn } from '@/lib/utils';
import { useMap } from '@/services/MapContext';

export default function Navbar({
  setExpanded,
}: {
  expanded: boolean;
  setExpanded: Dispatch<SetStateAction<boolean>>;
}) {
  const { setCity } = useMap();
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
          <Button variant='outline' size='icon'>
            <Sun className='h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0' />
            <Moon className='absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100' />
            <span className='sr-only'>Toggle theme</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align='end'>
          <DropdownMenuItem onClick={() => setCity('trondheim')}>
            Trondheim
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => setCity('oslo')}>
            Oslo
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => setCity('bergen')}>
            Bergen
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <ModeToggle />
    </div>
  );
}

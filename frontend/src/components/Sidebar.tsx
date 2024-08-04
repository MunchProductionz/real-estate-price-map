import { ReactNode, useState } from 'react';
import { Button } from './shadcn/ui/button';
import { cn } from '@/lib/utils';
import { Menu, X } from 'lucide-react';
import Filters from './Filters';
import ModeToggle from './ModeToggle';

export default function Sidebar({ children }: { children: ReactNode }) {
  const [expanded, setExpanded] = useState(true);
  return (
    <div className='flex min-h-screen bg-background'>
      <div className='fixed z-50 h-screen'>
        <Button
          size='icon'
          // variant='ghost'
          className={cn(
            'fixed top-2 transition-all duration-300',
            expanded ? 'left-52' : 'left-4',
          )}
          onClick={() => setExpanded((prev) => !prev)}
        >
          {expanded ? <X strokeWidth={'3px'} /> : <Menu strokeWidth={'3px'} />}
        </Button>
        <div
          className={cn(
            'flex h-full flex-col items-end gap-1 overflow-hidden border-r bg-primary-foreground pt-12 shadow-sm transition-all duration-300',
            expanded ? 'w-64' : 'w-0',
          )}
        >
          <ModeToggle />

          <Filters />
        </div>
      </div>
      <div
        className={cn(
          'w-full transition-all duration-300',
          expanded && 'translate-x-64 sm:translate-x-0 sm:pl-64',
        )}
      >
        {children}
      </div>
    </div>
  );
}

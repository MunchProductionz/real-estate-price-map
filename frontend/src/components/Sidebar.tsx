import { cn } from '@/lib/utils';
import { ReactNode, useState } from 'react';
import Filters from './Filters';
import Navbar from './Navbar';

export default function Sidebar({ children }: { children: ReactNode }) {
  const [expanded, setExpanded] = useState(true);
  return (
    <div className='flex min-h-screen bg-background'>
      <div className='fixed z-50 h-screen'>
        <div
          className={cn(
            'flex h-full flex-col items-end gap-1 overflow-hidden border-r bg-primary-foreground shadow-sm transition-all duration-300',
            expanded ? 'w-64' : 'w-0',
          )}
        >
          <div className='w-64'>
            <Filters />
          </div>
        </div>
      </div>
      <div
        className={cn(
          'w-full transition-all duration-300',
          expanded && 'translate-x-64 sm:translate-x-0 sm:pl-64',
        )}
      >
        <Navbar expanded={expanded} setExpanded={setExpanded} />
        {children}
      </div>
    </div>
  );
}

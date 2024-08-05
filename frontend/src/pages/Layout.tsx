import Filters from '@/components/Filters';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import { cn } from '@/lib/utils';
import { ReactNode, useState } from 'react';

export default function Layout({ children }: { children: ReactNode }) {
  const [expanded, setExpanded] = useState(true);
  const [filterView, setFilterView] = useState(false);
  return (
    <div className='flex min-h-screen bg-background'>
      <Sidebar expanded={expanded} setFilterView={setFilterView} />
      <div
        className={cn(
          'w-full transition-all duration-300',
          expanded && 'translate-x-64 sm:translate-x-0 sm:pl-64',
        )}
      >
        <Navbar expanded={expanded} setExpanded={setExpanded} />
        {children}
        {/* ToDo  Velge om vi skal ha grået ut når sidebar er 
                  åpen på liten skjerm (koden under) */}
        {/* {expanded && (
          <div className='fixed inset-0 bg-black bg-opacity-50 sm:hidden' />
        )} */}
        <Filters
          filterView={filterView}
          expanded={expanded}
          setFilterView={setFilterView}
        />
      </div>
    </div>
  );
}

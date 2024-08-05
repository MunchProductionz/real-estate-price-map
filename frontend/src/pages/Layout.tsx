import DetailedInformation from '@/components/DetailedInformation';
import Filters from '@/components/Filters';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import { Button } from '@/components/shadcn/ui/button';
import { cn } from '@/lib/utils';
import { Filter } from 'lucide-react';
import { ReactNode, useState } from 'react';

export default function Layout({ children }: { children: ReactNode }) {
  const [expanded, setExpanded] = useState(true);
  const [filterView, setFilterView] = useState(false);
  return (
    <div className='flex min-h-screen bg-background'>
      <Sidebar expanded={expanded} />
      <div
        className={cn(
          'w-full transition-all duration-300',
          expanded && 'translate-x-64 sm:translate-x-0 sm:pl-64',
        )}
      >
        <Navbar expanded={expanded} setExpanded={setExpanded} />
        {children}
        <Button
          size='icon'
          variant='outline'
          className='fixed bottom-0 m-2'
          onClick={() => setFilterView((prev) => !prev)}
        >
          <Filter />
        </Button>
        <Filters
          filterView={filterView}
          expanded={expanded}
          setFilterView={setFilterView}
        />
        <DetailedInformation />
      </div>
    </div>
  );
}

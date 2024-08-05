import { cn } from '@/lib/utils';
import { Filter } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';
import Inputs from './Inputs';
import { Button } from './shadcn/ui/button';

export default function Sidebar({
  expanded,
  setFilterView,
}: {
  expanded: boolean;
  setFilterView: Dispatch<SetStateAction<boolean>>;
}) {
  return (
    <div className='fixed z-30 h-screen'>
      <div
        className={cn(
          'flex h-full flex-col items-end gap-1 overflow-hidden border-r bg-primary-foreground shadow-sm transition-all duration-300',
          expanded ? 'w-64' : 'w-0',
        )}
      >
        <div className='flex h-full w-64 flex-col items-end justify-between'>
          <Inputs />
          <div className='m-4'>
            <Button
              size='icon'
              variant='ghost'
              onClick={() => setFilterView((prev) => !prev)}
            >
              <Filter />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

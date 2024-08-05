import { cn } from '@/lib/utils';
import { Dispatch, SetStateAction } from 'react';
import Inputs from './Inputs';

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
          'flex h-full w-0 flex-col items-end gap-1 overflow-hidden border-r bg-primary-foreground shadow-sm transition-all duration-300',
          expanded && 'w-64',
        )}
      >
        <div className='flex h-full w-64 flex-col items-end justify-between'>
          <Inputs />
        </div>
      </div>
    </div>
  );
}

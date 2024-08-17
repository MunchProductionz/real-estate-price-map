import { cn } from '@/lib/utils';
import Inputs from './Inputs';

export default function Sidebar({ expanded }: { expanded: boolean }) {
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
        </div>
      </div>
    </div>
  );
}

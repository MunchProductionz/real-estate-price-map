import { cn } from '@/lib/utils';
import Inputs from './Inputs';
import { useMap } from '@/services/MapContext';

export default function DetailedInformation() {
  const { selectedPostcode } = useMap();

  return (
    <div
      className={cn(
        'fixed bottom-2 right-2 overflow-hidden rounded-lg bg-background transition-all duration-300',
        selectedPostcode ? 'w-64' : 'w-0',
      )}
    >
      <div
        className={cn(
          'flex h-full flex-col items-end gap-1 overflow-hidden border-r bg-primary-foreground shadow-sm transition-all duration-300',
          selectedPostcode ? 'w-64' : 'w-0',
        )}
      >
        <div className='flex h-full w-64 flex-col items-end justify-between'>
          <Inputs />
        </div>
      </div>
    </div>
  );
}

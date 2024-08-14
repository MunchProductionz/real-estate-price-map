import { Menu } from 'lucide-react';
import { Dispatch, SetStateAction } from 'react';
import ModeToggle from './ModeToggle';
import { Button } from './shadcn/ui/button';

export default function Navbar({
  setExpanded,
}: {
  expanded: boolean;
  setExpanded: Dispatch<SetStateAction<boolean>>;
}) {
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
      <ModeToggle />
    </div>
  );
}

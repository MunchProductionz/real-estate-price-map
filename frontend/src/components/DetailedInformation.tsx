import { cn } from '@/lib/utils';
import Inputs from './Inputs';
import { useMap } from '@/services/MapContext';
import { Label } from './shadcn/ui/label';
import { Slider } from './shadcn/ui/slider';
import { useState } from 'react';

export default function DetailedInformation() {
  const { selectedFeature, selectedDistance, city } = useMap();
  const [averageSize, setAverageSize] = useState(60);

  return (
    <div
      className={cn(
        'fixed bottom-2 right-2 overflow-hidden rounded-lg bg-background transition-all duration-300',
        selectedFeature ? 'w-80' : 'w-0',
      )}
    >
      <div
        className={cn(
          'flex h-full flex-col items-end gap-1 overflow-hidden border-r bg-primary-foreground shadow-sm transition-all duration-300',
          selectedFeature ? 'w-80' : 'w-0',
        )}
      >
        <div className='flex h-full w-80 flex-col items-end justify-between'>
          <div className='flex h-full w-80 flex-col items-end justify-between'>
            <div className='flex w-full flex-col items-center gap-4 p-4'>
              <Label className='text-lg'>INFO</Label>
              <div className='flex w-full flex-col gap-2 text-wrap'>
                <div>Postkode: {selectedFeature?.properties.postnummer}</div>
                <div>
                  Kvadratmeterpris:{' '}
                  {selectedFeature?.properties.averageSquareMeterPrice.toLocaleString()}
                </div>
                {city === 'oslo' && (
                  <div className='flex w-full flex-col gap-2'>
                    <div>
                      Nærmeste kjøpesenter: gå i ca{' '}
                      {
                        selectedDistance?.nearest_location.shopping_mall
                          .travel_data.walking.duration.minutes
                      }{' '}
                      minutter
                      {' - '}
                      {
                        selectedDistance?.nearest_location.shopping_mall
                          .destination_name
                      }
                    </div>
                    <div>
                      Nærmeste vinmonopol: gå i ca{' '}
                      {
                        selectedDistance?.nearest_location.vinmonopolet
                          .travel_data.walking.duration.minutes
                      }{' '}
                      minutter
                      {' - '}
                      {
                        selectedDistance?.nearest_location.vinmonopolet
                          .destination_name
                      }
                    </div>
                  </div>
                )}
              </div>
              <Label className='text-lg'>KJØP</Label>
              <div className='flex w-full flex-col gap-2 text-wrap'>
                <div>Postkode: {selectedFeature?.properties.postnummer}</div>
                <div>
                  Snittpris for:{' '}
                  <div className='flex gap-2'>
                    <Slider
                      defaultValue={[60]}
                      max={200}
                      min={20}
                      step={10}
                      onValueChange={(e: number[]) => setAverageSize(e[0])}
                    />
                    <div>{averageSize}</div>
                  </div>
                  {(
                    selectedFeature?.properties.averageSquareMeterPrice ??
                    0 * averageSize
                  ).toLocaleString()}
                </div>
                <div>
                  Nærmeste kjøpesenter: gå i ca{' '}
                  {
                    selectedDistance?.nearest_location.shopping_mall.travel_data
                      .walking.duration.minutes
                  }{' '}
                  minutter
                  {' - '}
                  {
                    selectedDistance?.nearest_location.shopping_mall
                      .destination_name
                  }
                </div>
                <div>
                  Nærmeste vinmonopol: gå i ca{' '}
                  {
                    selectedDistance?.nearest_location.vinmonopolet.travel_data
                      .walking.duration.minutes
                  }{' '}
                  minutter
                  {' - '}
                  {
                    selectedDistance?.nearest_location.vinmonopolet
                      .destination_name
                  }
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

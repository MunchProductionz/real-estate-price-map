export interface LocationDirectory {
  [postalCode: string]: PostalCodeEntry;
}
export interface PostalCodeEntry {
  nearest_location: NearestLocation;
}
export interface NearestLocation {
  vinmonopolet: Location;
  shopping_mall: Location;
}
export interface Location {
  destination_name: string;
  destination_address: string;
  travel_data: TravelData;
}
export interface TravelData {
  walking: TravelMethod;
  driving: TravelMethod;
}
export interface TravelMethod {
  distance: Distance;
  duration: Duration;
}
export interface Distance {
  text: string;
  meters: number;
  kilometers: number;
}
export interface Duration {
  text: string;
  seconds: number;
  minutes: number;
  hours: number;
  hours_and_minutes?: number[] | null;
}

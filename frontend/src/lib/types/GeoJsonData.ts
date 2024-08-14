export interface GeoJsonData {
  type: string;
  features: Feature[];
}

export interface Feature {
  type: string;
  geometry: Geometry;
  properties: Properties;
}

export interface Geometry {
  type: string;
  coordinates: number[][][];
}

export interface Properties {
  objtype: string;
  postnummer: string;
  poststed: string;
  averagePrice: number;
  averageSquareMeterPrice: number;
  pricePercentageChangeLastYear: number;
  pricePercentageChangeLastQuarter?: number;
  averageSalesTimeInDays: number;
  numberOfEstatesSoldLastQuarter?: number;
  numberOfEstatesSoldLastMonth?: number;
}

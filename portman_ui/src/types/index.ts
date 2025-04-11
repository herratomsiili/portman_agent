export interface Vessel {
  imoLloyds: number;
  vesselName: string;
  vesselTypeCode: string;
  mmsi?: string;
}

export interface Port {
  locode: string;
  name: string;
  country?: string;
}

export interface Berth {
  berthCode: string;
  berthName: string;
  portAreaCode: string;
  portAreaName: string;
}

export interface PortCall {
  // Basic information
  portcallid: number;
  imolloyds: number;
  vesselname: string;
  vesseltypecode: string;
  
  // Port information
  porttovisit: string;
  portareacode: string;
  portareaname: string;
  berthcode: string;
  berthname: string;
  prevport: string;
  nextport: string;
  
  // Timestamps
  eta: string;
  etd: string;
  ata?: string;
  atd?: string;
  
  // Passenger and crew counts
  passengersonarrival?: number;
  passengersondeparture?: number;
  crewonarrival?: number;
  crewondeparture?: number;
  
  // Company information
  agentname?: string;
  shippingcompany?: string;
  
  // Metadata
  created: string;
  modified: string;
}

export interface ArrivalUpdate {
  id: number;
  portCallId: number;
  eta: string;
  oldEta: string;
  ata: string;
  vesselName: string;
  portAreaName: string;
  berthName: string;
  created: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
}

export interface AppSettings {
  trackedVessels: number[]; // IMO numbers
  refreshInterval: number; // in seconds
  defaultView: 'map' | 'list' | 'timeline';
}

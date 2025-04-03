// Define types based on the portman_agent database schema

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
  portAreaCode?: string;
  portAreaName?: string;
}

export interface PortCall2 {
  agentname: string
  ata: string
  atd: string
  berthcode: string
  berthname: string
  created: string
  crewonarrival: string
  crewondeparture: number
  eta: string
  etd: string
  imolloyds: number
  modified: string
  nextport: string
  passengersonarrival: number
  passengersondeparture: number
  portareacode: string
  portareaname: string
  portcallid: number
  porttovisit: string
  prevport: number
  shippingcompany: string
  vesselname: string
  vesseltypecode: string
}

// TODO: refactor port call interface to match Azure API
export interface PortCall {
  portCallId: number;
  vessel: Vessel;
  port: Port;
  berth: Berth;
  eta: string; // ISO date string
  etd: string; // ISO date string
  ata?: string; // ISO date string
  atd?: string; // ISO date string
  passengerCount?: number;
  crewCount?: number;
  prevPort?: Port;
  nextPort?: Port;
  portCallStatus: string;
  cargoDescription?: string;
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

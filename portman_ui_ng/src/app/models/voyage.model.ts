export interface Voyage {
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
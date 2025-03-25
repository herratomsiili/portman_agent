import React from 'react';
import { PortCall } from '../types';

// Mock data for port calls
// @ts-ignore
// @ts-ignore
export const mockPortCalls: PortCall[] = [
  {
    portCallId: 1001,
    vessel: {
      imoLloyds: 9123456,
      vesselName: "Nordic Princess",
      vesselTypeCode: "PAX"
    },
    port: {
      locode: "FIHLK",
      name: "Helsinki",
      country: "Finland"
    },
    berth: {
      berthCode: "EK7",
      berthName: "Eteläsatama K7",
      portAreaCode: "ES",
      portAreaName: "Eteläsatama"
    },
    eta: "2025-03-20T08:30:00Z",
    etd: "2025-03-20T16:00:00Z",
    ata: "2025-03-20T08:45:00Z",
    // @ts-ignore
    atd: null,
    passengerCount: 1250,
    crewCount: 85,
    prevPort: {
      locode: "EESTL",
      name: "Tallinn",
      country: "Estonia"
    },
    nextPort: {
      locode: "SESTO",
      name: "Stockholm",
      country: "Sweden"
    },
    portCallStatus: "ACTIVE",
    cargoDescription: "Passengers and vehicles",
    created: "2025-03-15T10:00:00Z",
    modified: "2025-03-20T08:45:00Z"
  },
  {
    portCallId: 1002,
    vessel: {
      imoLloyds: 9234567,
      vesselName: "Baltic Carrier",
      vesselTypeCode: "CONT"
    },
    port: {
      locode: "FIHLK",
      name: "Helsinki",
      country: "Finland"
    },
    berth: {
      berthCode: "VL1",
      berthName: "Vuosaari L1",
      portAreaCode: "VS",
      portAreaName: "Vuosaari"
    },
    eta: "2025-03-21T06:00:00Z",
    etd: "2025-03-21T18:00:00Z",
    // @ts-ignore
    ata: null,
    // @ts-ignore
    atd: null,
    passengerCount: 0,
    crewCount: 22,
    prevPort: {
      locode: "DEHAM",
      name: "Hamburg",
      country: "Germany"
    },
    nextPort: {
      locode: "FIRAU",
      name: "Rauma",
      country: "Finland"
    },
    portCallStatus: "SCHEDULED",
    cargoDescription: "Containers",
    created: "2025-03-16T14:30:00Z",
    modified: "2025-03-16T14:30:00Z"
  },
  {
    portCallId: 1003,
    vessel: {
      imoLloyds: 9345678,
      vesselName: "Arctic Explorer",
      vesselTypeCode: "TANK"
    },
    port: {
      locode: "FIKOK",
      name: "Kokkola",
      country: "Finland"
    },
    berth: {
      berthCode: "D12",
      berthName: "Deep Port D12",
      portAreaCode: "DP",
      portAreaName: "Deep Port"
    },
    eta: "2025-03-19T22:00:00Z",
    etd: "2025-03-20T14:00:00Z",
    ata: "2025-03-19T21:45:00Z",
    atd: "2025-03-20T13:30:00Z",
    passengerCount: 0,
    crewCount: 18,
    prevPort: {
      locode: "SESKN",
      name: "Skellefteå",
      country: "Sweden"
    },
    nextPort: {
      locode: "RULUG",
      name: "Luga",
      country: "Russia"
    },
    portCallStatus: "COMPLETED",
    cargoDescription: "Crude oil",
    created: "2025-03-15T09:15:00Z",
    modified: "2025-03-20T13:30:00Z"
  },
  {
    portCallId: 1004,
    vessel: {
      imoLloyds: 9456789,
      vesselName: "Silja Serenade",
      vesselTypeCode: "PAX"
    },
    port: {
      locode: "FITRK",
      name: "Turku",
      country: "Finland"
    },
    berth: {
      berthCode: "T3",
      berthName: "Terminal 3",
      portAreaCode: "PT",
      portAreaName: "Passenger Terminal"
    },
    eta: "2025-03-20T19:30:00Z",
    etd: "2025-03-21T08:00:00Z",
    // @ts-ignore
    ata: null,
    // @ts-ignore
    atd: null,
    passengerCount: 2800,
    crewCount: 200,
    prevPort: {
      locode: "SESTO",
      name: "Stockholm",
      country: "Sweden"
    },
    nextPort: {
      locode: "SESTO",
      name: "Stockholm",
      country: "Sweden"
    },
    portCallStatus: "SCHEDULED",
    cargoDescription: "Passengers and vehicles",
    created: "2025-03-14T12:00:00Z",
    modified: "2025-03-14T12:00:00Z"
  },
  {
    portCallId: 1005,
    vessel: {
      imoLloyds: 9567890,
      vesselName: "Finnstar",
      vesselTypeCode: "RORO"
    },
    port: {
      locode: "FIHLK",
      name: "Helsinki",
      country: "Finland"
    },
    berth: {
      berthCode: "VL3",
      berthName: "Vuosaari L3",
      portAreaCode: "VS",
      portAreaName: "Vuosaari"
    },
    eta: "2025-03-22T10:00:00Z",
    etd: "2025-03-22T20:00:00Z",
    // @ts-ignore
    ata: null,
    // @ts-ignore
    atd: null,
    passengerCount: 0,
    crewCount: 30,
    prevPort: {
      locode: "DETRA",
      name: "Travemünde",
      country: "Germany"
    },
    nextPort: {
      locode: "DETRA",
      name: "Travemünde",
      country: "Germany"
    },
    portCallStatus: "SCHEDULED",
    cargoDescription: "Ro-ro cargo",
    created: "2025-03-18T08:45:00Z",
    modified: "2025-03-18T08:45:00Z"
  }
];

// Mock data for arrival updates
export const mockArrivalUpdates = [
  {
    id: 1,
    portCallId: 1001,
    eta: "2025-03-20T08:30:00Z",
    oldEta: "2025-03-20T07:00:00Z",
    ata: "2025-03-20T08:45:00Z",
    vesselName: "Nordic Princess",
    portAreaName: "Eteläsatama",
    berthName: "Eteläsatama K7",
    created: "2025-03-19T14:00:00Z"
  },
  {
    id: 2,
    portCallId: 1002,
    eta: "2025-03-21T06:00:00Z",
    oldEta: "2025-03-21T04:30:00Z",
    ata: null,
    vesselName: "Baltic Carrier",
    portAreaName: "Vuosaari",
    berthName: "Vuosaari L1",
    created: "2025-03-20T10:15:00Z"
  },
  {
    id: 3,
    portCallId: 1003,
    eta: "2025-03-19T22:00:00Z",
    oldEta: "2025-03-19T23:30:00Z",
    ata: "2025-03-19T21:45:00Z",
    vesselName: "Arctic Explorer",
    portAreaName: "Deep Port",
    berthName: "Deep Port D12",
    created: "2025-03-19T18:00:00Z"
  }
];

// Mock tracked vessels (IMO numbers)
export const mockTrackedVessels = [9123456, 9234567, 9345678, 9456789, 9567890];

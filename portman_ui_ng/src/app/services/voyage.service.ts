import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, catchError, map, throwError, of, delay } from 'rxjs';
import { Voyage } from '../models/voyage.model';
import { API_CONFIG } from '../config/api.config';
import { MOCK_VOYAGES } from '../data/mock-voyages';

@Injectable({
  providedIn: 'root'
})
export class VoyageService {
  private http = inject(HttpClient);
  private apiUrl = `${API_CONFIG.apiBaseUrl}${API_CONFIG.endpoints.rest.voyages}`;
  // Set to true to use mock data instead of API calls
  private useMockData = false;

  constructor() {
    console.log('VoyageService initialized with URL:', this.apiUrl);
    console.log('Using mock data:', this.useMockData);
  }

  getVoyages(params?: { imo?: string; from?: string; to?: string }): Observable<Voyage[]> {
    if (this.useMockData) {
      console.log('Using mock data for voyages');
      // Filter mock data based on params if needed
      let filteredVoyages = [...MOCK_VOYAGES];
      
      if (params?.imo) {
        const imoNumber = parseInt(params.imo);
        filteredVoyages = filteredVoyages.filter(voyage => voyage.imolloyds === imoNumber);
      }
      
      return of(filteredVoyages).pipe(
        delay(500) // Simulate network delay
      );
    }

    let httpParams = new HttpParams();
    
    if (params?.imo) {
      httpParams = httpParams.set('imo', params.imo);
    }
    
    if (params?.from) {
      httpParams = httpParams.set('from', params.from);
    }
    
    if (params?.to) {
      httpParams = httpParams.set('to', params.to);
    }

    console.log('Fetching voyages with params:', params);
    
    return this.http.get<{ value: Voyage[] }>(this.apiUrl, { params: httpParams })
      .pipe(
        map(response => {
          console.log('Received voyages response:', response);
          return response.value || [];
        }),
        catchError(error => {
          console.error('Error fetching voyages:', error);
          return throwError(() => error);
        })
      );
  }

  getVoyageById(id: number): Observable<Voyage> {
    if (this.useMockData) {
      console.log('Using mock data for voyage by id:', id);
      const voyage = MOCK_VOYAGES.find(v => v.portcallid === id);
      
      if (voyage) {
        return of(voyage).pipe(delay(300));
      } else {
        return throwError(() => new Error(`Voyage with id ${id} not found`));
      }
    }

    console.log('Fetching voyage by ID:', id);
    
    return this.http.get<Voyage>(`${this.apiUrl}/${id}`)
      .pipe(
        catchError(error => {
          console.error(`Error fetching voyage ${id}:`, error);
          return throwError(() => error);
        })
      );
  }
} 
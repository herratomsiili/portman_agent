import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MOCK_VOYAGES } from './data/mock-voyages';
import { Voyage } from './models/voyage.model';

@Component({
  selector: 'app-standalone-test',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 20px;">
      <h2>Standalone Test Component</h2>
      <p>This component doesn't use NgRx or API calls, just direct rendering.</p>
      
      <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
        <thead>
          <tr style="background-color: #f4f4f4;">
            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Vessel Name</th>
            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Port</th>
            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Berth</th>
            <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">ETA</th>
          </tr>
        </thead>
        <tbody>
          @for (voyage of voyages; track voyage.portcallid) {
            <tr style="border-bottom: 1px solid #ddd;">
              <td style="padding: 8px;">{{ voyage.vesselname }}</td>
              <td style="padding: 8px;">{{ voyage.portareaname }}</td>
              <td style="padding: 8px;">{{ voyage.berthname }}</td>
              <td style="padding: 8px;">{{ formatDate(voyage.eta) }}</td>
            </tr>
          }
        </tbody>
      </table>
    </div>
  `
})
export class StandaloneTestComponent {
  voyages: Voyage[] = MOCK_VOYAGES;
  
  formatDate(dateString: string | undefined): string {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  }
} 
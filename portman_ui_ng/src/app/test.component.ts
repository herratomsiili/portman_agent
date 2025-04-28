import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { Observable, map } from 'rxjs';
import { AppState } from './store';
import { testAction } from './store/test/test.actions';

@Component({
  selector: 'app-test',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 20px; background-color: #f0f0f0; border-radius: 5px; margin: 20px;">
      <h2>Test Component</h2>
      <p>If you can see this, basic Angular rendering is working!</p>
      <p *ngIf="tested$ | async">NgRx store is also working! 🎉</p>
      <button (click)="testStore()">Test NgRx Store</button>
    </div>
  `
})
export class TestComponent implements OnInit {
  tested$: Observable<boolean>;

  constructor(private store: Store<AppState>) {
    this.tested$ = this.store.select(state => state.test.tested);
  }

  ngOnInit(): void {
    console.log('Test component initialized');
  }

  testStore(): void {
    console.log('Dispatching test action');
    this.store.dispatch(testAction());
  }
} 
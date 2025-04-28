import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';

// Import the traditional component 
import { TraditionalAppComponent } from './traditional-app.component';

// Import standalone components
import { StandaloneTestComponent } from './standalone-test.component';

import { routes } from './app.routes';
import { reducers, effects } from './store';

@NgModule({
  declarations: [
    // Regular, non-standalone components
    TraditionalAppComponent
  ],
  imports: [
    // Angular core modules
    BrowserModule,
    CommonModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(routes),
    
    // NgRx
    StoreModule.forRoot(reducers),
    EffectsModule.forRoot(effects),
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: false,
      autoPause: true
    })
  ],
  providers: [],
  bootstrap: [TraditionalAppComponent]
})
export class AppModule { } 
import { createAction, props } from '@ngrx/store';
import { Voyage } from '../../models/voyage.model';

export const loadVoyages = createAction('[Voyage] Load Voyages');

export const loadVoyagesSuccess = createAction(
  '[Voyage] Load Voyages Success',
  props<{ voyages: Voyage[] }>()
);

export const loadVoyagesFailure = createAction(
  '[Voyage] Load Voyages Failure',
  props<{ error: any }>()
);

export const loadVoyage = createAction(
  '[Voyage] Load Voyage',
  props<{ id: number }>()
);

export const loadVoyageSuccess = createAction(
  '[Voyage] Load Voyage Success',
  props<{ voyage: Voyage }>()
);

export const loadVoyageFailure = createAction(
  '[Voyage] Load Voyage Failure',
  props<{ error: any }>()
); 
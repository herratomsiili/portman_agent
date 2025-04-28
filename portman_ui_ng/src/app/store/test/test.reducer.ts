import { createReducer, on } from '@ngrx/store';
import * as TestActions from './test.actions';

export interface TestState {
  tested: boolean;
}

export const initialState: TestState = {
  tested: false
};

export const testReducer = createReducer(
  initialState,
  on(TestActions.testAction, (state) => ({
    ...state,
    tested: true
  }))
); 
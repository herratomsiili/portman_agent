import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Navbar', () => {
  render(<App />);
  const element = screen.getByText(/Portman/i);
  expect(element).toBeInTheDocument();
});

test('renders Login button', () => {
  render(<App />);
  const e = screen.getByText(/Login/i);
    expect(e).toBeInTheDocument();
});

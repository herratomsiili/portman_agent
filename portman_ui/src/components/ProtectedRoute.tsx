import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  requiredRole?: 'admin' | 'user' | 'viewer';
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ requiredRole }) => {
  const { isAuthenticated, user } = useAuth();

  // Jos käyttäjä ei ole kirjautunut sisään, ohjataan kirjautumissivulle
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Jos vaaditaan tietty rooli ja käyttäjällä ei ole sitä
  if (requiredRole && user && user.role !== requiredRole && user.role !== 'admin') {
    return <Navigate to="/" replace />;
  }

  // Muuten näytetään suojattu sisältö
  return <Outlet />;
};

export default ProtectedRoute; 
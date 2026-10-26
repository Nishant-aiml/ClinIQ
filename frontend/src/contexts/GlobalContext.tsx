import React, { createContext, useContext, useState } from 'react';

interface GlobalContextType {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (isOpen: boolean) => void;
  isCopilotOpen: boolean;
  setIsCopilotOpen: (isOpen: boolean) => void;
  activePatientId: string | null;
  activePatientName: string | null;
  openCopilot: (patientId?: string, patientName?: string) => void;
  closeCopilot: () => void;
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

export const GlobalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);
  const [activePatientId, setActivePatientId] = useState<string | null>(null);
  const [activePatientName, setActivePatientName] = useState<string | null>(null);

  const toggleSidebar = () => setSidebarOpen(prev => !prev);

  const openCopilot = (patientId?: string, patientName?: string) => {
    if (patientId) setActivePatientId(patientId);
    if (patientName) setActivePatientName(patientName);
    setIsCopilotOpen(true);
  };

  const closeCopilot = () => {
    setIsCopilotOpen(false);
  };

  return (
    <GlobalContext.Provider
      value={{
        isSidebarOpen,
        toggleSidebar,
        setSidebarOpen,
        isCopilotOpen,
        setIsCopilotOpen,
        activePatientId,
        activePatientName,
        openCopilot,
        closeCopilot,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => {
  const context = useContext(GlobalContext);
  if (context === undefined) {
    throw new Error('useGlobalContext must be used within a GlobalProvider');
  }
  return context;
};


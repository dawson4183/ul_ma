import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ListingsProvider } from "@/contexts/ListingsContext";
import Index from "./pages/Index";
import Catalogue from "./pages/Catalogue";
import Messages from "./pages/Messages";
import Vendre from "./pages/Vendre";
import AnnoncePage from "./pages/AnnoncePage";
import MesAnnonces from "./pages/MesAnnonces";
import Auth from "./pages/Auth";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ListingsProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/catalogue" element={<Catalogue />} />
            <Route path="/messages" element={<Messages />} />
            <Route path="/vendre" element={<Vendre />} />
            <Route path="/mes-annonces" element={<MesAnnonces />} />
            <Route path="/annonce/:id" element={<AnnoncePage />} />
            <Route path="/auth" element={<Auth />} />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ListingsProvider>
  </QueryClientProvider>
);

export default App;

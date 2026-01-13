import { Link, useLocation } from "react-router-dom";
import { Home } from "lucide-react";
import ApiStatus from "./ApiStatus";

const Header = () => {
  const location = useLocation();
  
  return (
    <header className="fixed top-0 left-0 right-0 z-50">
      <div className="glass mx-4 mt-4 px-6 py-4 rounded-2xl">
        <div className="container mx-auto flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-200">
              <Home className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-display text-xl font-bold text-gradient">NestIQ</h1>
              <p className="text-xs text-muted-foreground hidden sm:block">Intelligent Forecasting</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-6">
            <Link
              to="/"
              className={`text-sm font-medium transition-colors duration-200 ${
                location.pathname === "/" 
                  ? "text-primary" 
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Home
            </Link>
            <Link
              to="/predict"
              className={`text-sm font-medium transition-colors duration-200 ${
                location.pathname === "/predict" 
                  ? "text-primary" 
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Predict
            </Link>
            <ApiStatus />
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;

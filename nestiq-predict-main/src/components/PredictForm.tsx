import { useState, useCallback, useEffect } from "react";
import { motion } from "framer-motion";
import { Home, Bath, Bed, Calendar, TrendingUp, Loader2, MapPin, Search, X, CheckCircle } from "lucide-react";
import GlassCard from "./ui/GlassCard";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

interface AreaInsights {
  schools: {
    nearest_distance_km: number;
    count: number;
  };
  hospitals: {
    nearest_distance_km: number;
    count: number;
  };
  public_transport: {
    nearest_distance_km: number;
    count: number;
  };
  crime_rate_percent: number;
}

interface PredictionResult {
  predicted_price: number;
  area_insights?: AreaInsights;
}

interface FormData {
  area_sqft: string;
  bedrooms: string;
  bathrooms: string;
  year: string;
}

interface LocationData {
  name: string;
  latitude: number;
  longitude: number;
}

interface LocationResult {
  display_name: string;
  lat: string;
  lon: string;
}

interface PredictFormProps {
  onResult: (result: PredictionResult | null, locationName?: string) => void;
  onError: (error: string | null) => void;
}

// Simple debounce hook
const useDebounce = (value: string, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

const PredictForm = ({ onResult, onError }: PredictFormProps) => {
  const [formData, setFormData] = useState<FormData>({
    area_sqft: "",
    bedrooms: "2",
    bathrooms: "1",
    year: "2025",
  });
  const [location, setLocation] = useState<LocationData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Location search state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<LocationResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  const debouncedQuery = useDebounce(searchQuery, 400);

  // Search locations when debounced query changes
  useEffect(() => {
    const searchLocations = async () => {
      if (debouncedQuery.length < 3) {
        setSearchResults([]);
        setIsDropdownOpen(false);
        return;
      }

      setIsSearching(true);
      setSearchError(null);

      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(debouncedQuery)}&format=json&limit=5&countrycodes=us,in,gb,ca,au`,
          {
            headers: {
              "Accept": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error("Search failed");
        }

        const data: LocationResult[] = await response.json();
        setSearchResults(data);
        setIsDropdownOpen(data.length > 0);

        if (data.length === 0 && debouncedQuery.length >= 3) {
          setSearchError("No locations found. Try a different search.");
        }
      } catch (err) {
        setSearchError("Unable to search. Please try again.");
        setSearchResults([]);
      } finally {
        setIsSearching(false);
      }
    };

    searchLocations();
  }, [debouncedQuery]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLocationSelect = (result: LocationResult) => {
    setLocation({
      name: result.display_name,
      latitude: parseFloat(result.lat),
      longitude: parseFloat(result.lon),
    });
    setSearchQuery("");
    setSearchResults([]);
    setIsDropdownOpen(false);
    setSearchError(null);
  };

  const handleLocationClear = () => {
    setLocation(null);
  };

  const formatLocationName = (name: string): string => {
    const parts = name.split(",").slice(0, 3);
    return parts.join(", ");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    onError(null);
    onResult(null);

    if (!location) {
      onError("Please select a location using the search.");
      return;
    }

    const areaSqft = parseFloat(formData.area_sqft);
    if (isNaN(areaSqft) || areaSqft < 100 || areaSqft > 100000) {
      onError("Please enter a valid area between 100 and 100,000 sq.ft.");
      return;
    }

    setIsLoading(true);

    try {
      const payload = {
        latitude: location.latitude,
        longitude: location.longitude,
        area_sqft: areaSqft,
        bedrooms: parseInt(formData.bedrooms),
        bathrooms: parseInt(formData.bathrooms),
        year: parseInt(formData.year),
      };

      const response = await fetch(`${API_BASE_URL}/api/predict/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to get prediction. Please check your inputs and try again.");
      }

      const data: PredictionResult = await response.json();
      onResult(data, formatLocationName(location.name));
    } catch (error) {
      onError(error instanceof Error ? error.message : "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const years = Array.from({ length: 6 }, (_, i) => 2025 + i);
  const bedrooms = [1, 2, 3, 4, 5, 6];
  const bathrooms = [1, 2, 3, 4, 5];

  return (
    <GlassCard className="w-full max-w-2xl mx-auto">
      <div className="mb-6">
        <h2 className="font-display text-2xl font-bold text-foreground mb-2">Property Details</h2>
        <p className="text-muted-foreground text-sm">Enter the property specifications for AI-powered price estimation</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Location Search */}
        <div className="space-y-3">
          <label className="flex items-center gap-2 text-sm font-medium text-foreground">
            <MapPin className="w-4 h-4 text-primary" />
            Location / Area / City
          </label>

          {location ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-3 p-4 rounded-xl bg-primary/10 border border-primary/30"
            >
              <CheckCircle className="w-5 h-5 text-primary flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground truncate">
                  {formatLocationName(location.name)}
                </p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Location selected • Ready for prediction
                </p>
              </div>
              <button
                type="button"
                onClick={handleLocationClear}
                className="p-1.5 rounded-lg hover:bg-white/10 transition-colors"
                aria-label="Clear location"
              >
                <X className="w-4 h-4 text-muted-foreground hover:text-foreground" />
              </button>
            </motion.div>
          ) : (
            <div className="relative">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="e.g., Gachibowli, Hyderabad"
                  className="input-glass text-foreground pl-11 pr-10"
                />
                {isSearching && (
                  <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-primary animate-spin" />
                )}
              </div>

              {/* Dropdown Results */}
              {isDropdownOpen && searchResults.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute z-50 w-full mt-2 rounded-xl glass overflow-hidden"
                >
                  <ul className="max-h-60 overflow-y-auto">
                    {searchResults.map((result, index) => (
                      <li key={`${result.lat}-${result.lon}-${index}`}>
                        <button
                          type="button"
                          onClick={() => handleLocationSelect(result)}
                          className="w-full px-4 py-3 text-left hover:bg-white/10 transition-colors flex items-start gap-3"
                        >
                          <MapPin className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-foreground leading-snug">
                            {formatLocationName(result.display_name)}
                          </span>
                        </button>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}

              {/* Error Message */}
              {searchError && !isSearching && (
                <p className="mt-2 text-xs text-amber-400 flex items-center gap-1">
                  <span>⚠</span> {searchError}
                </p>
              )}
            </div>
          )}
        </div>

        {/* Area */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-foreground">
            <Home className="w-4 h-4 text-primary" />
            Area (sq.ft)
          </label>
          <input
            type="number"
            name="area_sqft"
            value={formData.area_sqft}
            onChange={handleInputChange}
            placeholder="e.g., 1200"
            min="100"
            max="100000"
            required
            className="input-glass text-foreground"
          />
        </div>

        {/* Bedrooms & Bathrooms */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Bed className="w-4 h-4 text-primary" />
              Bedrooms
            </label>
            <select
              name="bedrooms"
              value={formData.bedrooms}
              onChange={handleInputChange}
              className="input-glass text-foreground"
            >
              {bedrooms.map((num) => (
                <option key={num} value={num} className="bg-background text-foreground">
                  {num} {num === 1 ? "Bedroom" : "Bedrooms"}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-foreground">
              <Bath className="w-4 h-4 text-primary" />
              Bathrooms
            </label>
            <select
              name="bathrooms"
              value={formData.bathrooms}
              onChange={handleInputChange}
              className="input-glass text-foreground"
            >
              {bathrooms.map((num) => (
                <option key={num} value={num} className="bg-background text-foreground">
                  {num} {num === 1 ? "Bathroom" : "Bathrooms"}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Year */}
        <div className="space-y-2">
          <label className="flex items-center gap-2 text-sm font-medium text-foreground">
            <Calendar className="w-4 h-4 text-primary" />
            Target Year
          </label>
          <select
            name="year"
            value={formData.year}
            onChange={handleInputChange}
            className="input-glass text-foreground"
          >
            {years.map((year) => (
              <option key={year} value={year} className="bg-background text-foreground">
                {year}
              </option>
            ))}
          </select>
        </div>

        {/* Submit Button */}
        <motion.button
          type="submit"
          disabled={isLoading || !location}
          className="w-full py-4 rounded-xl font-display font-semibold text-primary-foreground bg-gradient-to-r from-primary to-accent btn-glow transition-all duration-300 hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2 relative overflow-hidden"
          whileTap={{ scale: 0.98 }}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <TrendingUp className="w-5 h-5" />
              Predict Price
            </>
          )}
        </motion.button>

        {!location && (
          <p className="text-center text-xs text-muted-foreground flex items-center justify-center gap-1">
            <MapPin className="w-3 h-3" />
            Select a location to enable prediction
          </p>
        )}
      </form>
    </GlassCard>
  );
};

export default PredictForm;

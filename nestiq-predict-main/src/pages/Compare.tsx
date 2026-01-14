import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    MapPin,
    Plus,
    Trash2,
    ArrowRight,
    Loader2,
    CheckCircle2,
    TrendingUp,
    AlertCircle
} from "lucide-react";
import { Link } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import GlassCard from "@/components/ui/GlassCard";
import PageTransition from "@/components/PageTransition";
import ResultCard from "@/components/ResultCard";

// Reuse types (should ideally be in a shared types file)
interface AreaInsights {
    schools: { nearest_distance_km: number; count: number };
    hospitals: { nearest_distance_km: number; count: number };
    public_transport: { nearest_distance_km: number; count: number };
    crime_rate_percent: number;
}

interface PredictionResult {
    predicted_price: number;
    current_price?: number;
    year?: number;
    area_insights?: AreaInsights;
    currency?: { symbol: string; code: string };
    price_trend?: { year: number; price: number }[];
}

interface Location {
    id: string;
    name: string;
    lat: number;
    lon: number;
    result?: PredictionResult;
    loading?: boolean;
    error?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

const Compare = () => {
    // Inputs
    const [areaSqft, setAreaSqft] = useState<string>("1500");
    const [bedrooms, setBedrooms] = useState<number>(3);
    const [bathrooms, setBathrooms] = useState<number>(2);
    const [year, setYear] = useState<number>(2025);

    // Locations State
    const [locations, setLocations] = useState<Location[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState<any[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const [isComparing, setIsComparing] = useState(false);

    // --- Handlers ---

    const handleSearch = async (val: string) => {
        setSearchQuery(val);
        if (val.length < 3) return;
        setIsSearching(true);
        try {
            const resp = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(val)}&format=json&limit=5`);
            const data = await resp.json();
            setSearchResults(data);
        } catch (e) {
            console.error(e);
        } finally {
            setIsSearching(false);
        }
    };

    const addLocation = (res: any) => {
        // Prevent duplicates
        if (locations.find(l => l.name === res.display_name)) return;

        if (locations.length >= 3) {
            alert("You can compare up to 3 locations at a time.");
            return;
        }

        const newLoc: Location = {
            id: Math.random().toString(36).substr(2, 9),
            name: res.display_name,
            lat: parseFloat(res.lat),
            lon: parseFloat(res.lon)
        };

        setLocations([...locations, newLoc]);
        setSearchQuery("");
        setSearchResults([]);

        // Auto-warmup cache
        fetch(`${API_BASE_URL}/api/warmup/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ latitude: newLoc.lat, longitude: newLoc.lon }),
        }).catch(console.error);
    };

    const removeLocation = (id: string) => {
        setLocations(locations.filter(l => l.id !== id));
    };

    const runComparison = async () => {
        if (locations.length === 0) return;
        setIsComparing(true);

        // Run parallel requests
        const promises = locations.map(async (loc) => {
            try {
                const resp = await fetch(`${API_BASE_URL}/api/predict/`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        latitude: loc.lat,
                        longitude: loc.lon,
                        area_sqft: parseFloat(areaSqft),
                        bedrooms,
                        bathrooms,
                        year
                    })
                });

                if (!resp.ok) throw new Error("Failed");
                const data = await resp.json();
                return { ...loc, result: data, loading: false };
            } catch (e) {
                return { ...loc, error: "Failed to fetch data", loading: false };
            }
        });

        const updatedLocations = await Promise.all(promises);
        setLocations(updatedLocations);
        setIsComparing(false);
    };

    const hasResults = locations.some(l => l.result);

    return (
        <PageTransition>
            <div className="min-h-screen flex flex-col">
                <Header />

                <main className="flex-1 pt-32 pb-16 px-4">
                    <div className="container mx-auto max-w-6xl space-y-12">

                        {/* Header */}
                        <div className="text-center space-y-4">
                            <h1 className="font-display text-4xl md:text-5xl font-bold text-gradient">Compare Locations</h1>
                            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
                                Analyze how property value changes across different neighborhoods for the exact same home configuration.
                            </p>
                        </div>

                        {/* Controls Section */}
                        {!hasResults && (
                            <div className="grid lg:grid-cols-2 gap-8">
                                {/* 1. Property Config */}
                                <GlassCard className="space-y-6">
                                    <div className="flex items-center gap-3 mb-4">
                                        <div className="p-2 rounded-lg bg-primary/20 text-primary">
                                            <Plus className="w-5 h-5" />
                                        </div>
                                        <h2 className="text-xl font-bold text-white">Property Details</h2>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <label className="text-sm text-muted-foreground">Area (sq ft)</label>
                                            <input
                                                type="number"
                                                value={areaSqft}
                                                onChange={e => setAreaSqft(e.target.value)}
                                                className="w-full p-3 rounded-xl bg-white/5 border border-white/10 text-white focus:ring-2 focus:ring-primary/50 outline-none"
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm text-muted-foreground">Year</label>
                                            <select
                                                value={year}
                                                onChange={e => setYear(parseInt(e.target.value))}
                                                className="w-full p-3 rounded-xl bg-white/5 border border-white/10 text-white focus:ring-2 focus:ring-primary/50 outline-none"
                                            >
                                                {[2025, 2026, 2027, 2028, 2029].map(y => (
                                                    <option key={y} value={y} className="bg-black text-white">{y}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm text-muted-foreground">Bedrooms</label>
                                            <div className="flex gap-2">
                                                {[1, 2, 3, 4, 5].map(n => (
                                                    <button
                                                        key={n}
                                                        onClick={() => setBedrooms(n)}
                                                        className={`flex-1 p-2 rounded-lg border transition-colors ${bedrooms === n ? 'bg-primary text-black border-primary' : 'bg-white/5 border-white/10'}`}
                                                    >
                                                        {n}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm text-muted-foreground">Bathrooms</label>
                                            <div className="flex gap-2">
                                                {[1, 2, 3, 4].map(n => (
                                                    <button
                                                        key={n}
                                                        onClick={() => setBathrooms(n)}
                                                        className={`flex-1 p-2 rounded-lg border transition-colors ${bathrooms === n ? 'bg-primary text-black border-primary' : 'bg-white/5 border-white/10'}`}
                                                    >
                                                        {n}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </GlassCard>

                                {/* 2. Location Manager */}
                                <GlassCard className="space-y-6 flex flex-col">
                                    <div className="flex items-center gap-3 mb-4">
                                        <div className="p-2 rounded-lg bg-emerald-500/20 text-emerald-400">
                                            <MapPin className="w-5 h-5" />
                                        </div>
                                        <h2 className="text-xl font-bold text-white">Select Locations (Max 3)</h2>
                                    </div>

                                    {/* Search Input */}
                                    <div className="relative z-20">
                                        <input
                                            type="text"
                                            value={searchQuery}
                                            onChange={e => handleSearch(e.target.value)}
                                            placeholder="Search city or area..."
                                            className="w-full p-3 pl-10 rounded-xl bg-white/5 border border-white/10 text-white focus:ring-2 focus:ring-primary/50 outline-none"
                                        />
                                        <MapPin className="absolute left-3 top-3.5 w-5 h-5 text-muted-foreground" />

                                        {/* Dropdown */}
                                        {searchResults.length > 0 && (
                                            <div className="absolute top-full mt-2 w-full bg-black border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                                                {searchResults.map((res, i) => (
                                                    <button
                                                        key={i}
                                                        onClick={() => addLocation(res)}
                                                        className="w-full text-left p-3 hover:bg-white/10 text-sm text-white border-b border-white/5 last:border-0"
                                                    >
                                                        {res.display_name}
                                                    </button>
                                                ))}
                                            </div>
                                        )}
                                    </div>

                                    {/* Selected List */}
                                    <div className="flex-1 space-y-3 mt-4">
                                        {locations.length === 0 && (
                                            <p className="text-sm text-muted-foreground text-center py-8">
                                                No locations added yet. Search above to add.
                                            </p>
                                        )}
                                        {locations.map(loc => (
                                            <div key={loc.id} className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/10">
                                                <div className="flex items-center gap-3 overflow-hidden">
                                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center flex-shrink-0">
                                                        <span className="text-xs font-bold">{loc.name.substring(0, 2).toUpperCase()}</span>
                                                    </div>
                                                    <span className="text-sm font-medium truncate">{loc.name}</span>
                                                </div>
                                                <button onClick={() => removeLocation(loc.id)} className="p-2 hover:bg-red-500/20 hover:text-red-400 rounded-lg transition-colors">
                                                    <Trash2 className="w-4 h-4" />
                                                </button>
                                            </div>
                                        ))}
                                    </div>

                                    <button
                                        onClick={runComparison}
                                        disabled={locations.length < 2 || isComparing}
                                        className="w-full py-4 mt-auto bg-gradient-to-r from-primary to-emerald-400 text-black font-bold rounded-xl shadow-lg hover:scale-[1.02] transition-transform disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                    >
                                        {isComparing ? <Loader2 className="animate-spin w-5 h-5" /> : <TrendingUp className="w-5 h-5" />}
                                        Compare {locations.length} Locations
                                    </button>
                                </GlassCard>
                            </div>
                        )}

                        {/* 3. Results View */}
                        {hasResults && (
                            <div className="space-y-12">
                                <div className="flex justify-between items-center bg-black/40 p-4 rounded-xl border border-white/10 backdrop-blur-md sticky top-20 z-40">
                                    <div>
                                        <h3 className="text-lg font-bold text-white">Comparison Results</h3>
                                        <p className="text-xs text-muted-foreground">{areaSqft} sqft • {bedrooms} Bed • {bathrooms} Bath • {year}</p>
                                    </div>
                                    <button
                                        onClick={() => { setLocations(locations.map(l => ({ ...l, result: undefined }))); }}
                                        className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-sm transition-colors"
                                    >
                                        New Comparison
                                    </button>
                                </div>

                                <div className={`grid gap-6 ${locations.length === 2 ? 'lg:grid-cols-2' : 'lg:grid-cols-3'}`}>
                                    {locations.map(loc => (
                                        <div key={loc.id} className="relative">
                                            {loc.result ? (
                                                <ResultCard
                                                    predictedPrice={loc.result.predicted_price}
                                                    currentPrice={loc.result.current_price}
                                                    year={loc.result.year}
                                                    areaInsights={loc.result.area_insights}
                                                    locationName={loc.name}
                                                    currency={loc.result.currency}
                                                    priceTrend={loc.result.price_trend}
                                                />
                                            ) : (
                                                <GlassCard className="h-[400px] flex items-center justify-center">
                                                    {loc.error ? (
                                                        <div className="text-red-400 text-center">
                                                            <AlertCircle className="w-8 h-8 mx-auto mb-2" />
                                                            <p>Failed to load data</p>
                                                        </div>
                                                    ) : (
                                                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                                                    )}
                                                </GlassCard>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                    </div>
                </main>
                <Footer />
            </div>
        </PageTransition>
    );
};

export default Compare;

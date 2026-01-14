import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MapPin, Home, Bed, Bath, Calendar, Loader2, ArrowRight, X, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import GlassCard from "./ui/GlassCard";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// --- Types ---
interface LocationResult {
    display_name: string;
    lat: string;
    lon: string;
}

interface PredictionResult {
    predicted_price: number;
    area_insights?: any;
}

interface WizardProps {
    onResult: (result: PredictionResult | null, locationName?: string) => void;
    onError: (error: string | null) => void;
}

// --- Steps Config ---
// Adjusting the concept:
// Video 1: Plays triggers transition TO Step 2? Or background for Step 1?
// User pattern implies: "Video 1" is the background for "Step 1". 
// When we finish Step 1, we play Video 1 to completion (or transition) OR we switch to Video 2?
// Let's assume: Each step has a background video. The "Transition" is playing that video or cross-fading.
// BUT, if it's a "journey", usually you play the video to *move* to the next spot.
// Strategy: 
// 1. Show Step 1 UI. Video 1 is paused at 0s (or looping if ambient).
// 2. User inputs -> Click Next.
// 3. UI Disappears. Video 1 Plays (The "Travel" shot).
// 4. Video 1 Ends.
// 5. Load Video 2.
// 6. Show Step 2 UI.
// --- Steps Config ---
const getAssetPath = (path: string) => {
    // Videos are copied to the root 'videos/' directory in dist/
    // So '/videos/step1.mp4' is correct for both Dev and Prod.
    // Nginx serves root /var/www/nestiq/, so /videos/ works.
    return path;
};

const STEPS = [
    { id: 1, video: getAssetPath("/videos/step1.mp4"), label: "Location" },
    { id: 2, video: getAssetPath("/videos/step2.mp4"), label: "Size" },
    { id: 3, video: getAssetPath("/videos/step3.mp4"), label: "Bedrooms" },
    { id: 4, video: getAssetPath("/videos/step4.mp4"), label: "Bathrooms" },
    { id: 5, video: getAssetPath("/videos/step4.mp4"), label: "Year" }, // Reusing step 4 for year as no step 5 video provided
];

export default function PredictionWizard({ onResult, onError }: WizardProps) {
    const [step, setStep] = useState(1);
    const [isPlaying, setIsPlaying] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false); // Fix: Add this missing state
    const videoRef = useRef<HTMLVideoElement>(null);

    // Form State
    const [location, setLocation] = useState<{ name: string; lat: number; lon: number } | null>(null);
    const [areaSqft, setAreaSqft] = useState<string>("");
    const [bedrooms, setBedrooms] = useState<number>(2);
    const [bathrooms, setBathrooms] = useState<number>(1);
    const [year, setYear] = useState<number>(2025);

    // Search State
    const [query, setQuery] = useState("");
    const [searchResults, setSearchResults] = useState<LocationResult[]>([]);
    const [isSearching, setIsSearching] = useState(false);

    // Load video when step changes
    useEffect(() => {
        if (videoRef.current) {
            // New step loaded.
            videoRef.current.load();
            setIsPlaying(false); // Ready for input
        }
    }, [step]);

    // --- Background Fetch ---
    const triggerWarmup = async (lat: number, lon: number) => {
        try {
            fetch(`${API_BASE_URL}/api/warmup/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ latitude: lat, longitude: lon }),
            }).catch(console.error); // Fire and forget
        } catch (e) {
            console.error(e);
        }
    };

    // --- Handlers ---

    const handleNext = () => {
        setIsPlaying(true);
        if (videoRef.current) {
            const promise = videoRef.current.play();
            if (promise !== undefined) {
                promise.catch(error => {
                    console.error("Video play failed", error);
                    // Fallback if video fails: just advance immediately
                    onVideoEnded();
                });
            }
        } else {
            onVideoEnded();
        }
    };

    const onVideoEnded = () => {
        // If we are submitting, we DO NOT want to show the UI again or advance step.
        // We wait for the API to return onResult.
        setIsPlaying(false);
        if (step < STEPS.length) {
            setStep(s => s + 1);
        } else {
            // Logic for end of step 5 video (if we want to play it before predicting)
        }
    };

    const handleLocationSelect = (res: LocationResult) => {
        const lat = parseFloat(res.lat);
        const lon = parseFloat(res.lon);
        setLocation({ name: res.display_name, lat, lon });
        setSearchResults([]);
        setQuery(res.display_name);

        triggerWarmup(lat, lon);
        handleNext(); // Play video 1 -> Go to Step 2
    };

    const handleSearch = async (val: string) => {
        setQuery(val);
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

    const submitPrediction = async () => {
        if (!location) return;

        setIsSubmitting(true); // START SUBMISSION
        setIsPlaying(true);    // Hide UI

        // Ensure video plays (it serves as the loading spinner)
        videoRef.current?.play().catch(e => console.error(e));

        try {
            const payload = {
                latitude: location.lat,
                longitude: location.lon,
                area_sqft: parseFloat(areaSqft),
                bedrooms,
                bathrooms,
                year
            };

            const resp = await fetch(`${API_BASE_URL}/api/predict/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) throw new Error("Prediction failed");

            const data = await resp.json();
            // Transition immediately when data is ready.
            onResult(data, location.name);

        } catch (e) {
            console.error("Prediction Error Details:", e);
            onError("Failed to predict price. Please check console/network.");
            setIsSubmitting(false); // Reset
            setIsPlaying(false);    // Show form again so they can retry
        }
    };


    // --- Render Steps ---
    const renderStepContent = () => {
        if (isPlaying && !isSubmitting) return null;

        if (isSubmitting) {
            return (
                <motion.div
                    key="loading-overlay"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-black/80 text-white"
                >
                    <Loader2 className="h-24 w-24 animate-spin text-primary" />
                    <p className="mt-8 text-3xl font-display font-bold">Calculating your property's value...</p>
                    <p className="mt-2 text-xl text-muted-foreground">This might take a moment as we analyze market data.</p>
                </motion.div>
            );
        }

        return (
            <div className="w-full max-w-3xl mx-auto">
                <GlassCard className="backdrop-blur-xl bg-black/40 border-white/10 shadow-2xl min-h-[500px] flex flex-col justify-start">
                    {renderStepInner()}
                </GlassCard>
            </div>
        )
    };

    const renderStepInner = () => {
        const contentClass = "space-y-8 p-10"; // Increased padding and spacing

        switch (step) {
            case 1: // Location
                return (
                    <div className={contentClass}>
                        <div className="flex items-center gap-4 mb-4">
                            <div className="p-4 rounded-full bg-primary/20 text-primary">
                                <MapPin className="w-10 h-10" />
                            </div>
                            <div>
                                <h2 className="text-4xl font-display font-bold">Where?</h2>
                                <p className="text-xl text-muted-foreground">Enter the property location</p>
                            </div>
                        </div>

                        <div className="relative">
                            <input
                                autoFocus
                                type="text"
                                value={query}
                                onChange={e => handleSearch(e.target.value)}
                                placeholder="City or Area (e.g. New York)"
                                className="w-full p-6 text-lg rounded-2xl bg-white/5 border border-white/10 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                            />
                            {isSearching && <Loader2 className="absolute right-6 top-6 animate-spin text-white/50 w-6 h-6" />}

                            {searchResults.length > 0 && (
                                <div className="absolute top-full mt-4 w-full bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl z-50 max-h-[60vh] overflow-y-auto">
                                    {searchResults.map((res, i) => (
                                        <button
                                            key={i}
                                            onClick={() => handleLocationSelect(res)}
                                            className="w-full text-left p-6 hover:bg-white/5 transition-colors border-b border-white/5 last:border-0 flex items-center gap-3 text-lg"
                                        >
                                            <MapPin className="w-6 h-6 text-white/40 flex-shrink-0" />
                                            <span className="truncate font-medium whitespace-normal leading-tight">{res.display_name}</span>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                );

            case 2: // Size
                return (
                    <div className={contentClass}>
                        <div className="flex items-center gap-4 mb-4">
                            <div className="p-4 rounded-full bg-primary/20 text-primary">
                                <Home className="w-10 h-10" />
                            </div>
                            <div>
                                <h2 className="text-4xl font-display font-bold">How Big?</h2>
                                <p className="text-xl text-muted-foreground">Square footage of the property</p>
                            </div>
                        </div>
                        <input
                            type="number"
                            value={areaSqft}
                            onChange={e => setAreaSqft(e.target.value)}
                            placeholder="e.g. 1500"
                            className="w-full p-8 text-5xl font-mono text-center rounded-2xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                        />
                        <button
                            disabled={!areaSqft}
                            onClick={handleNext}
                            className="w-full py-6 bg-primary text-black text-2xl font-bold rounded-2xl hover:brightness-110 transition-all flex items-center justify-center gap-3 mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Next Step <ArrowRight className="w-6 h-6" />
                        </button>
                    </div>
                );

            case 3: // Bedrooms
                return (
                    <div className={contentClass}>
                        <div className="flex items-center gap-4 mb-4">
                            <div className="p-4 rounded-full bg-primary/20 text-primary">
                                <Bed className="w-10 h-10" />
                            </div>
                            <div>
                                <h2 className="text-4xl font-display font-bold">Bedrooms</h2>
                                <p className="text-xl text-muted-foreground">Number of sleeping rooms</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-3 gap-6">
                            {[1, 2, 3, 4, 5, 6].map(num => (
                                <button
                                    key={num}
                                    onClick={() => { setBedrooms(num); handleNext(); }}
                                    className="p-10 rounded-2xl bg-white/5 border border-white/10 hover:bg-primary hover:text-black hover:scale-105 transition-all text-4xl font-bold"
                                >
                                    {num}
                                </button>
                            ))}
                        </div>
                    </div>
                );

            case 4: // Bathrooms
                return (
                    <div className={contentClass}>
                        <div className="flex items-center gap-4 mb-4">
                            <div className="p-4 rounded-full bg-primary/20 text-primary">
                                <Bath className="w-10 h-10" />
                            </div>
                            <div>
                                <h2 className="text-4xl font-display font-bold">Bathrooms</h2>
                                <p className="text-xl text-muted-foreground">Number of washrooms</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-3 gap-6">
                            {[1, 2, 3, 4, 5].map(num => (
                                <button
                                    key={num}
                                    onClick={() => { setBathrooms(num); handleNext(); }}
                                    className="p-10 rounded-2xl bg-white/5 border border-white/10 hover:bg-primary hover:text-black hover:scale-105 transition-all text-4xl font-bold"
                                >
                                    {num}
                                </button>
                            ))}
                        </div>
                    </div>
                );

            case 5: // Year
                return (
                    <div className={contentClass}>
                        <div className="flex items-center gap-4 mb-4">
                            <div className="p-4 rounded-full bg-primary/20 text-primary">
                                <Calendar className="w-10 h-10" />
                            </div>
                            <div>
                                <h2 className="text-4xl font-display font-bold">Year Built</h2>
                                <p className="text-xl text-muted-foreground">Target valuation year</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4 mb-8">
                            {[2025, 2026, 2027, 2028].map(y => (
                                <button
                                    key={y}
                                    onClick={() => setYear(y)}
                                    className={`p-6 rounded-2xl border transition-all text-xl font-bold ${year === y
                                        ? 'bg-primary text-black border-primary scale-105 shadow-lg shadow-primary/20'
                                        : 'bg-white/5 border-white/10 hover:bg-white/10'
                                        }`}
                                >
                                    {y}
                                </button>
                            ))}
                        </div>

                        <button
                            onClick={async () => {
                                setIsPlaying(true);
                                videoRef.current?.play();
                                await submitPrediction();
                            }}
                            className="w-full py-6 bg-gradient-to-r from-primary to-emerald-400 text-black font-bold rounded-2xl text-2xl shadow-xl shadow-primary/20 hover:scale-[1.02] transition-transform flex items-center justify-center gap-3"
                        >
                            Predict Price Now <ArrowRight className="w-6 h-6" />
                        </button>
                    </div>
                );
        }
    }


    return (
        <div className="fixed inset-0 z-50 bg-black flex items-center justify-center overflow-hidden">
            {/* 1. Full Screen Video Layer - Single Stable Player */}
            <div className="absolute inset-0 z-0 bg-black">
                <AnimatePresence>
                    {/* Overlay that fades in/out to hide src swap blips */}
                    {!isPlaying && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 0 }}
                            exit={{ opacity: 0 }}
                            className="absolute inset-0 bg-black pointer-events-none"
                        />
                    )}
                </AnimatePresence>
                <video
                    ref={videoRef}
                    key="main-video"
                    src={STEPS[step - 1].video}
                    className={`w-full h-full object-cover transition-opacity duration-1000 ${isPlaying ? 'opacity-100' : 'opacity-40 blur-sm'}`}
                    muted
                    playsInline
                    onEnded={onVideoEnded}
                // Force reload when src changes if needed, but React usually handles key prop on Source or src attr
                />
            </div>


            {/* 2. Content Overlay Layer */}
            <AnimatePresence mode="wait">
                {(!isPlaying || isSubmitting) && (
                    <motion.div
                        key={isSubmitting ? "loading" : `step-${step}`} // different key for loading to trigger transition? 
                        // Actually, renderStepContent handles the switch. 
                        // If we keep key=`step-${step}`, the overlay replaces the content within the same motion div?
                        // No, renderStepContent returns a NEW motion.div for loading.
                        // So let's stick to simple condition change first.
                        initial={{ opacity: 0, y: 40, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -40, scale: 1.05 }}
                        transition={{ duration: 0.5, ease: "easeOut" }}
                        className="relative z-10 w-full px-4"
                    >
                        {renderStepContent()}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* 3. Progress / Step Indicators */}
            <div className="absolute top-8 left-0 w-full px-8 md:px-16 flex justify-between z-20">
                {STEPS.map(s => (
                    <div key={s.id} className={`h-1.5 flex-1 mx-2 rounded-full transition-all duration-500 ${s.id <= step ? 'bg-primary shadow-[0_0_10px_rgba(34,197,94,0.6)]' : 'bg-white/10'
                        }`} />
                ))}
            </div>

            {/* Back Button (Only step > 1) */}
            {step > 1 && (
                <button
                    onClick={() => setStep(s => s - 1)}
                    className="absolute top-6 left-6 z-50 p-3 rounded-full bg-black/20 backdrop-blur-md border border-white/10 text-white/70 hover:text-white hover:bg-white/10 transition-all"
                    title="Go Back"
                >
                    <ArrowLeft className="w-6 h-6" />
                </button>
            )}

            {/* Exit Button */}
            <Link
                to="/"
                className="absolute top-6 right-6 z-50 p-3 rounded-full bg-black/20 backdrop-blur-md border border-white/10 text-white/70 hover:text-white hover:bg-white/10 transition-all"
                title="Back to Home"
            >
                <X className="w-6 h-6" />
            </Link>
        </div>
    );
}

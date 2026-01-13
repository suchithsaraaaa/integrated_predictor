import { useState } from "react";
import { motion } from "framer-motion";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import VideoBackground from "@/components/VideoBackground";
import PageTransition from "@/components/PageTransition";
import PredictForm from "@/components/PredictForm";
import ResultCard from "@/components/ResultCard";
import GlassCard from "@/components/ui/GlassCard";

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

const Predict = () => {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [locationName, setLocationName] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);

  const handleResult = (res: PredictionResult | null, locName?: string) => {
    setResult(res);
    setLocationName(locName);
    setError(null);
  };

  const handleError = (err: string | null) => {
    setError(err);
    setResult(null);
    setLocationName(undefined);
  };

  return (
    <PageTransition>
      <div className="min-h-screen flex flex-col">
        <VideoBackground videoSrc="/videos/predict-background.mp4" />
        <Header />

      <main className="flex-1 pt-32 pb-16">
        <div className="container mx-auto px-4">
          {/* Back Link */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
          >
            <Link
              to="/"
              className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-8"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Link>
          </motion.div>

          {/* Page Header */}
          <motion.div 
            className="text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="font-display text-4xl sm:text-5xl font-bold text-foreground mb-4">
              Price <span className="text-gradient">Prediction</span>
            </h1>
            <p className="text-muted-foreground max-w-xl mx-auto">
              Enter your property details below and let our AI analyze the market data to provide an accurate price estimate.
            </p>
          </motion.div>

          {/* Form Section */}
          <motion.div 
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <PredictForm 
              onResult={handleResult}
              onError={handleError}
            />
          </motion.div>

          {/* Error Display */}
          {error && (
            <motion.div 
              className="max-w-2xl mx-auto mb-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <GlassCard className="border-destructive/50">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="font-semibold text-foreground mb-1">Prediction Error</h3>
                    <p className="text-muted-foreground text-sm">{error}</p>
                    <p className="text-muted-foreground text-xs mt-2">
                      Make sure the backend server is running at http://127.0.0.1:8000
                    </p>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          )}

          {/* Result Display */}
          {result && (
            <motion.div 
              className="mb-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
            >
              <ResultCard 
                predictedPrice={result.predicted_price} 
                areaInsights={result.area_insights}
                locationName={locationName}
              />
            </motion.div>
          )}

          {/* Tips Section */}
          {!result && (
            <motion.div 
              className="max-w-2xl mx-auto mt-12"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <GlassCard className="opacity-80">
                <h3 className="font-display text-lg font-semibold text-foreground mb-3">
                  Tips for Accurate Predictions
                </h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    Search for your area by name (e.g., "Gachibowli, Hyderabad")
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    Enter the actual carpet/super built-up area in square feet
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary">•</span>
                    Target year helps forecast future property values based on market trends
                  </li>
                </ul>
              </GlassCard>
            </motion.div>
          )}
        </div>
      </main>

        <Footer />
      </div>
    </PageTransition>
  );
};

export default Predict;

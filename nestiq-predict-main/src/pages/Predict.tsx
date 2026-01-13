import { useState } from "react";
import { motion } from "framer-motion";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import PageTransition from "@/components/PageTransition";
import PredictionWizard from "@/components/PredictionWizard";
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
  current_price?: number;
  year?: number;
  area_insights?: AreaInsights;
  currency?: {
    symbol: string;
    code: string;
  };
  price_trend?: { year: number; price: number }[];
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
        {!result && <Header />}

        <main className="flex-1">
          {!result ? (
            <PredictionWizard
              onResult={handleResult}
              onError={handleError}
            />
          ) : (
            <div className="container mx-auto px-4 pt-32 pb-16">
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

              <ResultCard
                predictedPrice={result.predicted_price}
                currentPrice={result.current_price}
                year={result.year}
                areaInsights={result.area_insights}
                locationName={locationName}
                currency={result.currency}
                priceTrend={result.price_trend}
              />
            </div>
          )}

          {/* Error Display - Floating over wizard if needed, or in result view */}
          {error && (
            <motion.div
              className="fixed bottom-8 left-1/2 -translate-x-1/2 z-[100] max-w-md w-full px-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <GlassCard className="border-destructive/50 bg-black/80 backdrop-blur-xl">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="font-semibold text-white mb-1">Prediction Error</h3>
                    <p className="text-white/70 text-sm">{error}</p>
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          )}
        </main>

        {/* Only show footer if not in wizard (or sticky bottom?) Wizard is full screen... */}
        {result && <Footer />}
      </div>
    </PageTransition>
  );
};

export default Predict;

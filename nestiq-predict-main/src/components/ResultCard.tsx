import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  IndianRupee,
  DollarSign,
  PoundSterling,
  Sparkles,
  TrendingUp,
  GraduationCap,
  Hospital,
  Bus,
  Shield,
  MapPin
} from "lucide-react";
import GlassCard from "./ui/GlassCard";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

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

interface ResultCardProps {
  predictedPrice: number;
  areaInsights?: AreaInsights;
  locationName?: string;
  currency?: { symbol: string; code: string };
  currentPrice?: number;
  year?: number;
  priceTrend?: { year: number; price: number }[];
}

const ResultCard = ({ predictedPrice, areaInsights, locationName, currency = { symbol: "$", code: "USD" }, currentPrice, year, priceTrend }: ResultCardProps) => {
  const [displayValue, setDisplayValue] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    setIsAnimating(true);
    setDisplayValue(0);

    const duration = 1500;
    const steps = 60;
    const increment = predictedPrice / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current += increment;

      if (step >= steps) {
        setDisplayValue(predictedPrice);
        setIsAnimating(false);
        clearInterval(timer);
      } else {
        setDisplayValue(Math.round(current));
      }
    }, duration / steps);

    return () => clearInterval(timer);
  }, [predictedPrice]);

  const formatPrice = (price: number): string => {
    // currency specific formatting
    if (currency.code === "INR") {
      if (price >= 10000000) {
        return `${(price / 10000000).toFixed(2)} Cr`;
      } else if (price >= 100000) {
        return `${(price / 100000).toFixed(2)} Lac`;
      }
      return price.toLocaleString("en-IN");
    }

    // International big number formatting (M, k)
    if (price >= 1000000) {
      return `${(price / 1000000).toFixed(2)} M`;
    } else if (price >= 1000) {
      return `${(price / 1000).toFixed(2)} k`;
    }

    return price.toLocaleString("en-US");
  };

  const formatFullPrice = (price: number): string => {
    if (currency.code === "INR") return price.toLocaleString("en-IN");
    return price.toLocaleString("en-US");
  };

  const getCurrencyIcon = () => {
    if (currency.code === "INR") return <IndianRupee className="w-10 h-10 text-primary" />;
    if (currency.code === "GBP") return <PoundSterling className="w-10 h-10 text-primary" />;
    return <DollarSign className="w-10 h-10 text-primary" />;
  };

  const getCrimeLevel = (percent: number): { label: string; color: string; bgColor: string } => {
    if (percent <= 20) {
      return { label: "Low Crime Area", color: "text-emerald-400", bgColor: "bg-emerald-400/20" };
    } else if (percent <= 50) {
      return { label: "Moderate Crime", color: "text-amber-400", bgColor: "bg-amber-400/20" };
    } else {
      return { label: "High Crime Area", color: "text-red-400", bgColor: "bg-red-400/20" };
    }
  };

  const accessibilityCards = areaInsights ? [
    {
      icon: GraduationCap,
      title: "Schools",
      distance: areaInsights.schools.nearest_distance_km,
      count: areaInsights.schools.count,
      countLabel: "within 3 km",
      gradient: "from-blue-500/20 to-cyan-500/20",
      iconColor: "text-blue-400",
    },
    {
      icon: Hospital,
      title: "Hospitals",
      distance: areaInsights.hospitals.nearest_distance_km,
      count: areaInsights.hospitals.count,
      countLabel: "within 3 km",
      gradient: "from-rose-500/20 to-pink-500/20",
      iconColor: "text-rose-400",
    },
    {
      icon: Bus,
      title: "Public Transport",
      distance: areaInsights.public_transport.nearest_distance_km,
      count: areaInsights.public_transport.count,
      countLabel: "within 3 km",
      gradient: "from-violet-500/20 to-purple-500/20",
      iconColor: "text-violet-400",
    },
  ] : [];

  const crimeLevel = areaInsights ? getCrimeLevel(areaInsights.crime_rate_percent) : null;

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      {/* Main Price Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <GlassCard className="relative overflow-visible" glow>
          {/* Decorative sparkle */}
          <motion.div
            className="absolute -top-3 -right-3 w-12 h-12 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg"
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
          >
            <Sparkles className="w-6 h-6 text-primary-foreground" />
          </motion.div>

          <div className="text-center py-6">
            {/* Location */}
            {locationName && (
              <div className="flex items-center justify-center gap-2 mb-4">
                <MapPin className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm text-muted-foreground truncate max-w-md">
                  {locationName}
                </span>
              </div>
            )}

            {/* Label */}
            <div className="flex items-center justify-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-primary" />
              <span className="text-sm font-medium text-primary uppercase tracking-wider">
                Projected Value {year ? `(${year})` : ''}
              </span>
            </div>

            {/* Price Display */}
            <div className="relative">
              <motion.div
                className="flex items-center justify-center gap-2"
                initial={{ scale: 0.9 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.3, delay: 0.2 }}
              >
                {getCurrencyIcon()}
                <span className={`font-display text-5xl sm:text-6xl font-bold text-gradient counter ${isAnimating ? 'animate-count-up' : ''}`}>
                  {formatPrice(displayValue)}
                </span>
              </motion.div>

              <motion.p
                className="mt-3 text-muted-foreground text-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                {currency.symbol}{formatFullPrice(displayValue)}
              </motion.p>
            </div>

            {/* Current vs Future Comparison */}
            {currentPrice && (
              <div className="mt-8 border-t border-glass-border pt-6">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="text-center border-r border-glass-border">
                    <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Current Value (2025)</p>
                    <p className="text-xl font-bold text-white/80">
                      {currency.symbol}{formatPrice(currentPrice)}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Growth</p>
                    <p className={`text-xl font-bold ${predictedPrice >= currentPrice ? 'text-emerald-400' : 'text-red-400'}`}>
                      {predictedPrice >= currentPrice ? '+' : ''}
                      {((predictedPrice - currentPrice) / currentPrice * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>

                {/* GRAPH SECTION */}
                {priceTrend && (
                  <div className="h-[250px] w-full mt-6 pr-4">
                    <p className="text-xs text-muted-foreground uppercase tracking-wider mb-4 text-left pl-4">Market Trend Forecast (2021-2029)</p>
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={priceTrend}>
                        <defs>
                          <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                        <XAxis
                          dataKey="year"
                          stroke="#ffffff50"
                          tick={{ fontSize: 12 }}
                          axisLine={false}
                          tickLine={false}
                        />
                        <YAxis
                          stroke="#ffffff50"
                          tick={{ fontSize: 10 }}
                          tickFormatter={(val) => {
                            if (val >= 1000000) return `${(val / 1000000).toFixed(1)}M`;
                            if (val >= 1000) return `${(val / 1000).toFixed(0)}k`;
                            return val;
                          }}
                          axisLine={false}
                          tickLine={false}
                          width={40}
                        />
                        <Tooltip
                          contentStyle={{ backgroundColor: '#000', border: '1px solid #ffffff20', borderRadius: '8px' }}
                          itemStyle={{ color: '#fff' }}
                          formatter={(value: number) => [`${currency.symbol}${formatPrice(value)}`, 'Price']}
                          labelStyle={{ color: '#ffffff80' }}
                        />
                        <Area
                          type="monotone"
                          dataKey="price"
                          stroke="#22c55e"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorPrice)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>
            )}

            {/* Disclaimer */}
            <div className="mt-6 pt-4 border-t border-glass-border">
              <p className="text-xs text-muted-foreground flex items-center justify-center gap-1">
                <Sparkles className="w-3 h-3" />
                AI-generated estimate based on market data analysis
              </p>
            </div>
          </div>
        </GlassCard>
      </motion.div>

      {/* Area Insights Section */}
      {areaInsights && (
        <>
          {/* Section Header */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-center"
          >
            <h3 className="font-display text-xl font-semibold text-foreground mb-2">
              Area Accessibility
            </h3>
            <p className="text-sm text-muted-foreground">
              Nearby amenities and infrastructure
            </p>
          </motion.div>

          {/* Accessibility Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {accessibilityCards.map((card, index) => (
              <motion.div
                key={card.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
              >
                <GlassCard className="h-full" hover>
                  <div className="text-center">
                    {/* Icon */}
                    <div className={`w-12 h-12 mx-auto mb-3 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center`}>
                      <card.icon className={`w-6 h-6 ${card.iconColor}`} />
                    </div>

                    {/* Title */}
                    <h4 className="font-display font-semibold text-foreground mb-3">
                      {card.title}
                    </h4>

                    {/* Distance */}
                    <div className="mb-2">
                      <span className="text-2xl font-bold text-foreground">
                        {card.distance.toFixed(1)}
                      </span>
                      <span className="text-sm text-muted-foreground ml-1">km</span>
                    </div>
                    <p className="text-xs text-muted-foreground mb-3">
                      nearest {card.title.toLowerCase()}
                    </p>

                    {/* Count */}
                    <div className="pt-3 border-t border-glass-border">
                      <span className="text-lg font-semibold text-primary">{card.count}</span>
                      <p className="text-xs text-muted-foreground">{card.countLabel}</p>
                    </div>
                  </div>
                </GlassCard>
              </motion.div>
            ))}
          </div>

          {/* Crime Rate Indicator */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.7 }}
          >
            <GlassCard>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-xl ${crimeLevel?.bgColor} flex items-center justify-center`}>
                    <Shield className={`w-6 h-6 ${crimeLevel?.color}`} />
                  </div>
                  <div>
                    <h4 className="font-display font-semibold text-foreground">
                      Safety Index
                    </h4>
                    <p className={`text-sm font-medium ${crimeLevel?.color}`}>
                      {crimeLevel?.label}
                    </p>
                  </div>
                </div>

                <div className="text-right">
                  <div className="flex items-center gap-2">
                    <span className={`text-3xl font-bold ${crimeLevel?.color}`}>
                      {areaInsights.crime_rate_percent.toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">crime rate</p>
                </div>
              </div>

              {/* Progress bar */}
              <div className="mt-4 h-2 bg-muted rounded-full overflow-hidden">
                <motion.div
                  className={`h-full rounded-full ${areaInsights.crime_rate_percent <= 20
                    ? "bg-gradient-to-r from-emerald-500 to-emerald-400"
                    : areaInsights.crime_rate_percent <= 50
                      ? "bg-gradient-to-r from-amber-500 to-amber-400"
                      : "bg-gradient-to-r from-red-500 to-red-400"
                    }`}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(areaInsights.crime_rate_percent, 100)}%` }}
                  transition={{ duration: 1, delay: 0.8, ease: "easeOut" }}
                />
              </div>

              <div className="mt-2 flex justify-between text-xs text-muted-foreground">
                <span>Safe</span>
                <span>Moderate</span>
                <span>High Risk</span>
              </div>
            </GlassCard>
          </motion.div>
        </>
      )}
    </div>
  );
};

export default ResultCard;

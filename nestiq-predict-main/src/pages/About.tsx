import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
    Code2,
    Database,
    Brain,
    Map as MapIcon,
    ShieldCheck,
    ArrowRight,
    Layers,
    Cpu,
    Globe,
    TrendingUp
} from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import GlassCard from "@/components/ui/GlassCard";
import PageTransition from "@/components/PageTransition";

const TechItem = ({ icon: Icon, title, desc }: { icon: any, title: string, desc: string }) => (
    <div className="flex items-start gap-4 p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
        <div className="p-2 rounded-lg bg-primary/20 text-primary">
            <Icon className="w-5 h-5" />
        </div>
        <div>
            <h4 className="font-semibold text-white mb-1">{title}</h4>
            <p className="text-sm text-muted-foreground">{desc}</p>
        </div>
    </div>
);

const About = () => {
    return (
        <PageTransition>
            <div className="min-h-screen flex flex-col">
                <Header />

                <main className="flex-1 pt-32 pb-16 px-4">
                    <div className="container mx-auto max-w-5xl space-y-16">

                        {/* Hero Section */}
                        <section className="text-center space-y-6">
                            <motion.h1
                                className="font-display text-4xl md:text-6xl font-bold text-gradient"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5 }}
                            >
                                Intelligent Real Estate Forecasting
                            </motion.h1>
                            <motion.p
                                className="text-xl text-muted-foreground max-w-2xl mx-auto"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1, duration: 0.5 }}
                            >
                                NestIQ combines advanced Machine Learning with real-time geospatial data to provide hyper-local property value estimations and risk assessments.
                            </motion.p>
                        </section>

                        {/* How It Works */}
                        <section>
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.2 }}
                            >
                                <h2 className="text-2xl font-bold text-white mb-8 flex items-center gap-2">
                                    <Brain className="w-6 h-6 text-primary" />
                                    The Engine
                                </h2>

                                <div className="grid md:grid-cols-2 gap-6">
                                    <GlassCard className="space-y-4" glow>
                                        <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 mb-4">
                                            <Cpu className="w-6 h-6" />
                                        </div>
                                        <h3 className="text-xl font-bold text-white">Machine Learning Core</h3>
                                        <p className="text-muted-foreground">
                                            Our price prediction engine runs on a **Random Forest Regressor**, a robust ensemble learning method.
                                            It analyzes historical property data features (Year Built, Area, Bedrooms) to learn complex non-linear relationships that traditional linear models miss.
                                        </p>
                                    </GlassCard>

                                    <GlassCard className="space-y-4" glow>
                                        <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4">
                                            <ShieldCheck className="w-6 h-6" />
                                        </div>
                                        <h3 className="text-xl font-bold text-white">Risk & Safety Index</h3>
                                        <p className="text-muted-foreground">
                                            We calculate a dynamic Safety Score using a **Proximity-based Heuristic Model**.
                                            By analyzing distance from dense urban centers and correlating it with historical safety data patterns, we generate a localized risk profile (Low/Moderate/High) for every neighborhood.
                                        </p>
                                    </GlassCard>

                                    <GlassCard className="space-y-4 md:col-span-2" glow>
                                        <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 mb-4">
                                            <TrendingUp className="w-6 h-6" />
                                        </div>
                                        <h3 className="text-xl font-bold text-white">Market Trend Forecasting</h3>
                                        <p className="text-muted-foreground">
                                            Our system generates a **Multi-Year Price Trajectory (2021-2029)** for every property.
                                            It allows you to visualize historic value appreciation and future potential using our predictive time-series analysis, giving you a clear picture of long-term investment potential.
                                        </p>
                                    </GlassCard>
                                </div>
                            </motion.div>
                        </section>

                        {/* Tech Stack */}
                        <section>
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.3 }}
                            >
                                <h2 className="text-2xl font-bold text-white mb-8 flex items-center gap-2">
                                    <Layers className="w-6 h-6 text-primary" />
                                    Technology Stack
                                </h2>

                                <GlassCard>
                                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                                        <TechItem
                                            icon={Code2}
                                            title="Frontend"
                                            desc="React, TypeScript, Vite, Tailwind CSS, Framer Motion"
                                        />
                                        <TechItem
                                            icon={Database}
                                            title="Backend API"
                                            desc="Python, Django, Django REST Framework"
                                        />
                                        <TechItem
                                            icon={Brain}
                                            title="AI / ML"
                                            desc="Scikit-Learn, Pandas, NumPy, Joblib"
                                        />
                                        <TechItem
                                            icon={Globe}
                                            title="Geospatial"
                                            desc="OSMnx (OpenStreetMap), NetworkX, Shapely"
                                        />
                                        <TechItem
                                            icon={MapIcon}
                                            title="Interactive Maps"
                                            desc="Leaflet, React-Leaflet (Visualization)"
                                        />
                                        <TechItem
                                            icon={Cpu}
                                            title="Deployment"
                                            desc="Vite Build Pipeline, Whitenoise, SQLite"
                                        />
                                    </div>
                                </GlassCard>
                            </motion.div>
                        </section>

                        {/* Call to Action */}
                        <section className="text-center pt-8">
                            <Link to="/predict">
                                <GlassCard className="inline-flex items-center gap-3 px-8 py-4 hover:bg-white/5 transition-colors cursor-pointer group">
                                    <span className="text-lg font-semibold text-white">Try the Predictor</span>
                                    <ArrowRight className="w-5 h-5 text-primary group-hover:translate-x-1 transition-transform" />
                                </GlassCard>
                            </Link>
                        </section>

                    </div>
                </main>

                <Footer />
            </div>
        </PageTransition>
    );
};

export default About;

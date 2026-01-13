import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface VideoBackgroundProps {
  videoSrc?: string;
}

const VideoBackground = ({ videoSrc = "/videos/hero-background.mp4" }: VideoBackgroundProps) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div className="fixed inset-0 overflow-hidden" style={{ zIndex: -1 }}>
      {/* Loading spinner */}
      <AnimatePresence>
        {!isLoaded && (
          <motion.div
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            className="absolute inset-0 z-10 flex items-center justify-center bg-background"
          >
            <div className="relative">
              {/* Outer spinning ring */}
              <motion.div
                className="w-16 h-16 rounded-full border-4 border-primary/20"
                style={{ borderTopColor: "hsl(var(--primary))" }}
                animate={{ rotate: 360 }}
                transition={{
                  duration: 1,
                  repeat: Infinity,
                  ease: "linear",
                }}
              />
              
              {/* Inner pulsing dot */}
              <motion.div
                className="absolute inset-0 flex items-center justify-center"
                animate={{ scale: [0.8, 1, 0.8], opacity: [0.5, 1, 0.5] }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              >
                <div className="w-4 h-4 rounded-full bg-primary" />
              </motion.div>
            </div>
            
            {/* Loading text */}
            <motion.p
              className="absolute mt-28 text-sm text-muted-foreground"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              Loading...
            </motion.p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Video element */}
      <video
        autoPlay
        muted
        loop
        playsInline
        onCanPlayThrough={() => setIsLoaded(true)}
        onLoadedData={() => setIsLoaded(true)}
        className="absolute inset-0 w-full h-full object-cover"
      >
        <source src={videoSrc} type="video/mp4" />
      </video>
      
      {/* Dark overlay for better text readability */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: isLoaded ? 1 : 0 }}
        transition={{ duration: 0.5 }}
        className="absolute inset-0 bg-gradient-to-b from-background/70 via-background/50 to-background/80" 
      />
      
      {/* Subtle animated glow overlay */}
      <motion.div
        className="absolute inset-0"
        style={{
          background: "radial-gradient(ellipse at 30% 20%, hsla(var(--primary) / 0.1) 0%, transparent 50%)",
        }}
        initial={{ opacity: 0 }}
        animate={{
          opacity: isLoaded ? [0.5, 0.8, 0.5] : 0,
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Vignette effect */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          background: "radial-gradient(ellipse at center, transparent 0%, hsla(var(--background) / 0.6) 100%)",
        }}
      />
    </div>
  );
};

export default VideoBackground;

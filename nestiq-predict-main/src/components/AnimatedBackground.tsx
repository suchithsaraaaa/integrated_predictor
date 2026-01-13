import { motion } from "framer-motion";

const AnimatedBackground = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none" style={{ zIndex: -1 }}>
      {/* Main gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-[hsl(25,30%,8%)] via-[hsl(30,25%,6%)] to-[hsl(20,35%,5%)]" />
      
      {/* Animated mesh gradient orbs */}
      <motion.div
        className="absolute w-[800px] h-[800px] rounded-full"
        style={{
          background: "radial-gradient(circle, hsla(38, 90%, 50%, 0.15) 0%, transparent 70%)",
          filter: "blur(60px)",
          top: "-20%",
          right: "-10%",
        }}
        animate={{
          x: [0, 50, 0, -50, 0],
          y: [0, 30, -30, 20, 0],
          scale: [1, 1.1, 0.95, 1.05, 1],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
      
      <motion.div
        className="absolute w-[600px] h-[600px] rounded-full"
        style={{
          background: "radial-gradient(circle, hsla(32, 85%, 50%, 0.12) 0%, transparent 70%)",
          filter: "blur(80px)",
          bottom: "-15%",
          left: "-10%",
        }}
        animate={{
          x: [0, -40, 30, -20, 0],
          y: [0, -40, 20, -30, 0],
          scale: [1, 0.9, 1.1, 0.95, 1],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
      
      <motion.div
        className="absolute w-[500px] h-[500px] rounded-full"
        style={{
          background: "radial-gradient(circle, hsla(28, 80%, 55%, 0.1) 0%, transparent 70%)",
          filter: "blur(70px)",
          top: "40%",
          left: "30%",
        }}
        animate={{
          x: [0, 60, -40, 30, 0],
          y: [0, -50, 40, -20, 0],
          scale: [1, 1.15, 0.9, 1.1, 1],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Floating particles */}
      {[...Array(20)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 rounded-full bg-primary/30"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
          animate={{
            y: [0, -30, 0],
            opacity: [0.2, 0.6, 0.2],
          }}
          transition={{
            duration: 3 + Math.random() * 4,
            repeat: Infinity,
            delay: Math.random() * 2,
            ease: "easeInOut",
          }}
        />
      ))}

      {/* Grid overlay */}
      <div 
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(hsla(38, 90%, 55%, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, hsla(38, 90%, 55%, 0.3) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
        }}
      />

      {/* Vignette effect */}
      <div 
        className="absolute inset-0"
        style={{
          background: "radial-gradient(ellipse at center, transparent 0%, hsla(25, 30%, 5%, 0.5) 100%)",
        }}
      />
    </div>
  );
};

export default AnimatedBackground;

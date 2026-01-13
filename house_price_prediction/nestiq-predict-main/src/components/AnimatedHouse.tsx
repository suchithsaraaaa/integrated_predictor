import { motion } from "framer-motion";

const AnimatedHouse = () => {
  return (
    <div className="relative w-full max-w-lg mx-auto h-[300px] sm:h-[400px]">
      {/* Glow behind the house */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        animate={{
          opacity: [0.5, 0.8, 0.5],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      >
        <div 
          className="w-64 h-64 rounded-full"
          style={{
            background: "radial-gradient(circle, hsla(175, 80%, 55%, 0.3) 0%, transparent 70%)",
            filter: "blur(40px)",
          }}
        />
      </motion.div>

      {/* Main house SVG */}
      <svg
        viewBox="0 0 200 180"
        className="absolute inset-0 w-full h-full"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* House base - glass effect */}
        <motion.path
          d="M30 90 L100 30 L170 90 L170 150 L30 150 Z"
          fill="url(#houseGradient)"
          stroke="url(#strokeGradient)"
          strokeWidth="1.5"
          initial={{ pathLength: 0, opacity: 0 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 2, ease: "easeOut" }}
        />

        {/* Roof highlight */}
        <motion.path
          d="M30 90 L100 30 L170 90"
          fill="none"
          stroke="url(#roofGradient)"
          strokeWidth="2"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.5, delay: 0.5, ease: "easeOut" }}
        />

        {/* Door */}
        <motion.rect
          x="85"
          y="110"
          width="30"
          height="40"
          rx="2"
          fill="url(#doorGradient)"
          stroke="hsla(175, 80%, 55%, 0.5)"
          strokeWidth="1"
          initial={{ scaleY: 0 }}
          animate={{ scaleY: 1 }}
          transition={{ duration: 0.8, delay: 1.2, ease: "easeOut" }}
          style={{ transformOrigin: "center bottom" }}
        />

        {/* Windows */}
        <motion.rect
          x="45"
          y="100"
          width="25"
          height="25"
          rx="2"
          fill="url(#windowGradient)"
          stroke="hsla(175, 80%, 55%, 0.4)"
          strokeWidth="1"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 1.5 }}
        />
        <motion.rect
          x="130"
          y="100"
          width="25"
          height="25"
          rx="2"
          fill="url(#windowGradient)"
          stroke="hsla(175, 80%, 55%, 0.4)"
          strokeWidth="1"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 1.7 }}
        />

        {/* Window glow animation */}
        <motion.rect
          x="45"
          y="100"
          width="25"
          height="25"
          rx="2"
          fill="hsla(175, 80%, 55%, 0.3)"
          animate={{
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.rect
          x="130"
          y="100"
          width="25"
          height="25"
          rx="2"
          fill="hsla(175, 80%, 55%, 0.3)"
          animate={{
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
        />

        {/* Chimney */}
        <motion.rect
          x="135"
          y="45"
          width="15"
          height="30"
          fill="url(#houseGradient)"
          stroke="url(#strokeGradient)"
          strokeWidth="1"
          initial={{ scaleY: 0 }}
          animate={{ scaleY: 1 }}
          transition={{ duration: 0.5, delay: 0.8, ease: "easeOut" }}
          style={{ transformOrigin: "center bottom" }}
        />

        {/* Smoke particles */}
        {[0, 1, 2].map((i) => (
          <motion.circle
            key={i}
            cx={142 + i * 3}
            cy={40}
            r={3 - i * 0.5}
            fill="hsla(175, 80%, 55%, 0.2)"
            animate={{
              y: [-10, -40],
              opacity: [0.4, 0],
              scale: [1, 2],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              delay: i * 0.8,
              ease: "easeOut",
            }}
          />
        ))}

        {/* Gradients */}
        <defs>
          <linearGradient id="houseGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsla(220, 30%, 20%, 0.6)" />
            <stop offset="100%" stopColor="hsla(220, 30%, 10%, 0.8)" />
          </linearGradient>
          <linearGradient id="strokeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsla(175, 80%, 55%, 0.6)" />
            <stop offset="100%" stopColor="hsla(260, 60%, 60%, 0.4)" />
          </linearGradient>
          <linearGradient id="roofGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsla(175, 80%, 55%, 0.8)" />
            <stop offset="50%" stopColor="hsla(185, 85%, 60%, 1)" />
            <stop offset="100%" stopColor="hsla(260, 60%, 65%, 0.8)" />
          </linearGradient>
          <linearGradient id="doorGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="hsla(220, 30%, 15%, 0.8)" />
            <stop offset="100%" stopColor="hsla(220, 30%, 8%, 0.9)" />
          </linearGradient>
          <linearGradient id="windowGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="hsla(175, 80%, 55%, 0.2)" />
            <stop offset="100%" stopColor="hsla(185, 85%, 60%, 0.1)" />
          </linearGradient>
        </defs>
      </svg>

      {/* Floating data points */}
      {[
        { label: "₹72L", x: "10%", y: "30%", delay: 2 },
        { label: "₹1.2Cr", x: "80%", y: "25%", delay: 2.5 },
        { label: "+12%", x: "5%", y: "70%", delay: 3 },
        { label: "AI", x: "85%", y: "65%", delay: 3.5 },
      ].map((point, i) => (
        <motion.div
          key={i}
          className="absolute px-3 py-1.5 rounded-full glass text-xs font-medium text-primary"
          style={{ left: point.x, top: point.y }}
          initial={{ opacity: 0, scale: 0 }}
          animate={{ 
            opacity: 1, 
            scale: 1,
            y: [0, -8, 0],
          }}
          transition={{
            opacity: { duration: 0.5, delay: point.delay },
            scale: { duration: 0.5, delay: point.delay },
            y: { duration: 3, repeat: Infinity, delay: point.delay + 0.5, ease: "easeInOut" },
          }}
        >
          {point.label}
        </motion.div>
      ))}
    </div>
  );
};

export default AnimatedHouse;

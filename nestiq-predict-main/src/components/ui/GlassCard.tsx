import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
}

export const GlassCard = ({ children, className, hover = false, glow = false }: GlassCardProps) => {
  return (
    <div
      className={cn(
        "glass p-6",
        hover && "glass-hover cursor-pointer",
        glow && "glow",
        className
      )}
    >
      {children}
    </div>
  );
};

export default GlassCard;

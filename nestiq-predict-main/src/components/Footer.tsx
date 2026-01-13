import { Heart, Github } from "lucide-react";

const Footer = () => {
  return (
    <footer className="py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="glass rounded-2xl p-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>Built with</span>
              <Heart className="w-4 h-4 text-red-400 fill-red-400" />
              <span>for Engineering Mini Project</span>
            </div>
            
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <span>© 2025 NestIQ</span>
              <span className="hidden sm:inline">•</span>
              <span className="hidden sm:inline">AI-Powered Price Forecasting</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

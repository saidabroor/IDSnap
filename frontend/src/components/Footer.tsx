import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const Footer: React.FC = () => {
  const { language } = useLanguage();

  return (
    <footer className="bg-gray-800 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          {/* Left side - Company info */}
          <div className="text-center md:text-left">
            <div className="text-sm text-gray-300 mb-2">
              © 2025 <span className="font-semibold text-white">NexusTech</span>. 
              {language === 'ko' ? ' 모든 권리 보유.' : ' All rights reserved.'}
            </div>
            <div className="text-xs text-gray-400">
              {language === 'ko' ? '개발자: ' : 'Developed by '}
              <span className="font-medium text-gray-200">Saidabrorkhon Shavkatbekov</span>
            </div>
          </div>

          {/* Right side - Contact info */}
          <div className="text-center md:text-right">
            <div className="space-y-1">
              <div className="text-sm text-gray-300">
                <a 
                  href="mailto:info@nexustech.to.com" 
                  className="hover:text-emerald-400 transition-colors"
                >
                  info@nexustech.to.com
                </a>
              </div>
              <div className="text-sm text-gray-300">
                <a 
                  href="https://nexustech.it.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="hover:text-blue-400 transition-colors"
                >
                  nexustech.it.com
                </a>
              </div>
              <div className="text-xs text-gray-400">
                +82 10 5644-0728
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Camera, Globe } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const Header: React.FC = () => {
  const location = useLocation();
  const { language, setLanguage, t } = useLanguage();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Camera className="h-8 w-8 text-emerald-600" />
            <span className="text-xl font-bold text-gray-900">{t('appName')}</span>
          </Link>

          <nav className="hidden md:flex space-x-8">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/') 
                  ? 'text-emerald-600 bg-emerald-50' 
                  : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-50'
              }`}
            >
              {t('home')}
            </Link>
            <Link
              to="/recognition"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/recognition') 
                  ? 'text-emerald-600 bg-emerald-50' 
                  : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-50'
              }`}
            >
              {t('recognition')}
            </Link>
            <Link
              to="/add-user"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/add-user') 
                  ? 'text-emerald-600 bg-emerald-50' 
                  : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-50'
              }`}
            >
              {t('addUser')}
            </Link>
          </nav>

          <div className="flex items-center space-x-4">
            <button
              onClick={() => setLanguage(language === 'en' ? 'ko' : 'en')}
              className="flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Globe className="h-4 w-4" />
              <span>{language === 'en' ? '한국어' : 'English'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden border-t border-gray-100">
        <div className="px-4 py-3 space-y-1">
          <Link
            to="/"
            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
              isActive('/') 
                ? 'text-emerald-600 bg-emerald-50' 
                : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-50'
            }`}
          >
            {t('home')}
          </Link>
          <Link
            to="/recognition"
            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
              isActive('/recognition') 
                ? 'text-emerald-600 bg-emerald-50' 
                : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-50'
            }`}
          >
            {t('recognition')}
          </Link>
          <Link
            to="/add-user"
            className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
              isActive('/add-user') 
                ? 'text-emerald-600 bg-emerald-50' 
                : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-50'
            }`}
          >
            {t('addUser')}
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
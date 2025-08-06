import React from 'react';
import { Link } from 'react-router-dom';
import { Camera, UserPlus, Zap, Shield, Clock } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const Home: React.FC = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-blue-50 to-white">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <div className="flex justify-center mb-8">
            <div className="bg-gradient-to-r from-emerald-500 to-blue-500 p-4 rounded-2xl shadow-lg">
              <Camera className="h-16 w-16 text-white" />
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            <span className="bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
              {t('appName')}
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
            {t('appDescription')}
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              to="/recognition"
              className="bg-gradient-to-r from-emerald-600 to-emerald-500 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-emerald-700 hover:to-emerald-600 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center space-x-2"
            >
              <Camera className="h-5 w-5" />
              <span>{t('goToRecognition')}</span>
            </Link>
            
            <Link
              to="/add-user"
              className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg border-2 border-blue-200 hover:bg-blue-50 hover:border-blue-300 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center space-x-2"
            >
              <UserPlus className="h-5 w-5" />
              <span>{t('addNewUser')}</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-emerald-100 p-3 rounded-xl w-fit mb-4">
              <Zap className="h-8 w-8 text-emerald-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              {t('language') === 'ko' ? '즉시 인식' : 'Instant Recognition'}
            </h3>
            <p className="text-gray-600">
              {t('language') === 'ko' 
                ? '고급 AI 기술로 몇 초 만에 얼굴을 인식하고 정보를 제공합니다.'
                : 'Advanced AI technology recognizes faces and provides information within seconds.'
              }
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-blue-100 p-3 rounded-xl w-fit mb-4">
              <Shield className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              {t('language') === 'ko' ? '보안 우선' : 'Security First'}
            </h3>
            <p className="text-gray-600">
              {t('language') === 'ko' 
                ? '모든 데이터는 안전하게 처리되며 개인정보 보호를 최우선으로 합니다.'
                : 'All data is processed securely with privacy protection as our top priority.'
              }
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="bg-purple-100 p-3 rounded-xl w-fit mb-4">
              <Clock className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              {t('language') === 'ko' ? '사용자 친화적' : 'User Friendly'}
            </h3>
            <p className="text-gray-600">
              {t('language') === 'ko' 
                ? '직관적인 인터페이스로 누구나 쉽게 사용할 수 있습니다.'
                : 'Intuitive interface makes it easy for anyone to use.'
              }
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
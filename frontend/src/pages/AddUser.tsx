import React, { useState } from 'react';
import { UserPlus, Check, AlertCircle } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import FileUpload from '../components/FileUpload';

const AddUser: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    info: '',
  });
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { t } = useLanguage();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError(null);
    setSuccess(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name.trim() || !selectedFile) {
      setError('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(false);

    const submitData = new FormData();
    submitData.append('name', formData.name);
    submitData.append('info', formData.info);
    submitData.append('image', selectedFile);

    try {
      const response = await fetch('/add_user', {
        method: 'POST',
        body: submitData,
      });

      if (!response.ok) {
        throw new Error('Failed to add user');
      }

      setSuccess(true);
      setFormData({ name: '', info: '' });
      setSelectedFile(null);
    } catch (err) {
      setError('Failed to add user. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-blue-50 to-white py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-r from-emerald-500 to-blue-500 p-3 rounded-xl shadow-lg">
              <UserPlus className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            {t('addNewUserTitle')}
          </h1>
          <p className="text-gray-600 text-lg">
            {t('language') === 'ko' 
              ? '새로운 사용자를 데이터베이스에 추가하세요' 
              : 'Add a new person to the recognition database'
            }
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8 space-y-8">
          {/* Name Input */}
          <div>
            <label htmlFor="name" className="block text-sm font-semibold text-gray-700 mb-2">
              {t('name')} <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder={t('namePlaceholder')}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
              required
            />
          </div>

          {/* Info Input */}
          <div>
            <label htmlFor="info" className="block text-sm font-semibold text-gray-700 mb-2">
              {t('info')}
            </label>
            <textarea
              id="info"
              name="info"
              value={formData.info}
              onChange={handleInputChange}
              placeholder={t('infoPlaceholder')}
              rows={4}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors resize-none"
            />
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {t('language') === 'ko' ? '사진' : 'Photo'} <span className="text-red-500">*</span>
            </label>
            <FileUpload onFileSelect={handleFileSelect} />
          </div>

          {/* Success Message */}
          {success && (
            <div className="bg-green-50 border border-green-200 rounded-xl p-4">
              <div className="flex items-center space-x-3">
                <div className="bg-green-100 p-2 rounded-lg">
                  <Check className="h-5 w-5 text-green-600" />
                </div>
                <p className="text-green-800 font-medium">{t('userAdded')}</p>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-4">
              <div className="flex items-center space-x-3">
                <div className="bg-red-100 p-2 rounded-lg">
                  <AlertCircle className="h-5 w-5 text-red-600" />
                </div>
                <p className="text-red-800 font-medium">{error}</p>
              </div>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading || !formData.name.trim() || !selectedFile}
            className="w-full bg-gradient-to-r from-emerald-600 to-blue-600 text-white py-4 px-6 rounded-xl font-semibold text-lg hover:from-emerald-700 hover:to-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>{t('loading')}</span>
              </>
            ) : (
              <>
                <UserPlus className="h-5 w-5" />
                <span>{t('submitUser')}</span>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AddUser;
import React, { createContext, useContext, useState, ReactNode } from 'react';

type Language = 'en' | 'ko';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const translations = {
  en: {
    // Navigation
    home: 'Home',
    recognition: 'Recognition',
    addUser: 'Add User',
    
    // Home Page
    appName: 'IDSnap',
    appDescription: 'Upload a photo and get the person\'s name and information instantly.',
    goToRecognition: 'Go to Recognition',
    addNewUser: 'Add New User',
    
    // Recognition Page
    faceRecognition: 'Face Recognition',
    uploadImage: 'Upload Image',
    dropImage: 'Drop your image here or click to browse',
    supportedFormats: 'Supported formats: JPG, PNG, WEBP',
    analyzing: 'Analyzing...',
    recognizedPerson: 'Recognized Person',
    noFaceDetected: 'No face detected in the image',
    
    // Add User Page
    addNewUserTitle: 'Add New User',
    name: 'Name',
    namePlaceholder: 'Enter person\'s name',
    info: 'Information',
    infoPlaceholder: 'Enter additional information about this person',
    submitUser: 'Add User',
    userAdded: 'User added successfully!',
    
    // Common
    upload: 'Upload',
    submit: 'Submit',
    error: 'Error',
    success: 'Success',
    loading: 'Loading...',
  },
  ko: {
    // Navigation
    home: '홈',
    recognition: '인식',
    addUser: '사용자 추가',
    
    // Home Page
    appName: 'IDSnap',
    appDescription: '사진을 업로드하고 즉시 사람의 이름과 정보를 확인하세요.',
    goToRecognition: '인식 시작',
    addNewUser: '새 사용자 추가',
    
    // Recognition Page
    faceRecognition: '얼굴 인식',
    uploadImage: '이미지 업로드',
    dropImage: '이미지를 여기에 드롭하거나 클릭하여 찾아보세요',
    supportedFormats: '지원 형식: JPG, PNG, WEBP',
    analyzing: '분석 중...',
    recognizedPerson: '인식된 사람',
    noFaceDetected: '이미지에서 얼굴을 감지할 수 없습니다',
    
    // Add User Page
    addNewUserTitle: '새 사용자 추가',
    name: '이름',
    namePlaceholder: '사람의 이름을 입력하세요',
    info: '정보',
    infoPlaceholder: '이 사람에 대한 추가 정보를 입력하세요',
    submitUser: '사용자 추가',
    userAdded: '사용자가 성공적으로 추가되었습니다!',
    
    // Common
    upload: '업로드',
    submit: '제출',
    error: '오류',
    success: '성공',
    loading: '로딩 중...',
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [language, setLanguage] = useState<Language>('en');

  const t = (key: string): string => {
    return translations[language][key as keyof typeof translations['en']] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
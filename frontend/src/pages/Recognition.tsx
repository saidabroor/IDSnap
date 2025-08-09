import React, { useState } from "react";
import { Camera, User, Info, Loader } from "lucide-react";
import { useLanguage } from "../contexts/LanguageContext";
import FileUpload from "../components/FileUpload";

interface RecognitionResult {
  name: string;
  info: string;
  image_with_landmarks?: string;
}

const Recognition: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<RecognitionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { t } = useLanguage();

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
  };

  const handleRecognition = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:5000";

    try {
      const response = await fetch(`${apiUrl}/recognize`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Recognition failed");
      }

      const data: RecognitionResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(t("error"));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-emerald-50 to-white py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-gradient-to-r from-blue-500 to-emerald-500 p-3 rounded-xl shadow-lg">
              <Camera className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            {t("faceRecognition")}
          </h1>
          <p className="text-gray-600 text-lg">{t("uploadImage")}</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <FileUpload onFileSelect={handleFileSelect} />

          {selectedFile && (
            <div className="mt-6 text-center">
              <button
                onClick={handleRecognition}
                disabled={isLoading}
                className="bg-gradient-to-r from-blue-600 to-emerald-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-emerald-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 mx-auto"
              >
                {isLoading ? (
                  <>
                    <Loader className="h-5 w-5 animate-spin" />
                    <span>{t("analyzing")}</span>
                  </>
                ) : (
                  <>
                    <Camera className="h-5 w-5" />
                    <span>{t("recognition")}</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
            <div className="flex items-center space-x-3">
              <div className="bg-red-100 p-2 rounded-lg">
                <Info className="h-5 w-5 text-red-600" />
              </div>
              <p className="text-red-800 font-medium">{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-3">
              <User className="h-6 w-6 text-emerald-600" />
              <span>{t("recognizedPerson")}</span>
            </h2>

            <div className="grid md:grid-cols-2 gap-8">
              {result.image_with_landmarks && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">
                    {t("language") === "ko"
                      ? "얼굴 랜드마크"
                      : "Face Landmarks"}
                  </h3>
                  <img
                    src={`data:image/jpeg;base64,${result.image_with_landmarks}`}
                    alt="Face with landmarks"
                    className="w-full rounded-lg shadow-md"
                  />
                </div>
              )}

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 flex items-center space-x-2">
                    <User className="h-5 w-5 text-blue-600" />
                    <span>{t("name")}</span>
                  </h3>
                  <p className="text-xl text-gray-800 bg-gray-50 p-4 rounded-lg">
                    {result.name}
                  </p>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 flex items-center space-x-2">
                    <Info className="h-5 w-5 text-emerald-600" />
                    <span>{t("info")}</span>
                  </h3>
                  <p className="text-gray-700 bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
                    {result.info}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Recognition;

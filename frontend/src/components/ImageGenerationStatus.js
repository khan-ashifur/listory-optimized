import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Image, Loader, CheckCircle, XCircle, RefreshCw, Eye } from 'lucide-react';
import { listingAPI } from '../services/api';
import toast from 'react-hot-toast';

const ImageGenerationStatus = ({ listingId }) => {
  const [images, setImages] = useState([]);
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);

  const imageTypeLabels = {
    hero: 'Hero Shot',
    infographic: 'Infographic',
    lifestyle: 'Lifestyle',
    testimonial: 'Testimonial',
    whats_in_box: "What's in the Box"
  };

  const imageTypeDescriptions = {
    hero: 'Main product photo with professional lighting',
    infographic: 'Visual representation of key features',
    lifestyle: 'Product shown in real-world use',
    testimonial: 'Visual story of customer satisfaction',
    whats_in_box: 'Flat lay of all included items'
  };

  const fetchImageStatus = async () => {
    try {
      const response = await listingAPI.getImages(listingId);
      setImages(response.data.images);
      setSummary(response.data.summary);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching image status:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImageStatus();
    
    // Poll for updates every 5 seconds if images are still generating
    const interval = setInterval(() => {
      if (!summary.all_completed) {
        fetchImageStatus();
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [listingId, summary.all_completed]);

  const handleRegenerateImages = async () => {
    try {
      await listingAPI.regenerateImages(listingId);
      toast.success('Failed images queued for regeneration');
      fetchImageStatus();
    } catch (error) {
      toast.error('Error regenerating images');
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'generating':
        return <Loader className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Loader className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'Ready';
      case 'generating':
        return 'Generating...';
      case 'failed':
        return 'Failed';
      default:
        return 'Queued';
    }
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <Loader className="h-8 w-8 animate-spin mx-auto text-primary-500" />
        <p className="text-gray-600 mt-2">Loading image status...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Image className="h-5 w-5 mr-2" />
            AI-Generated Product Images
          </h3>
          {summary.failed > 0 && (
            <button
              onClick={handleRegenerateImages}
              className="flex items-center text-sm text-purple-600 hover:text-purple-700"
            >
              <RefreshCw className="h-4 w-4 mr-1" />
              Retry Failed
            </button>
          )}
        </div>
        
        <div className="grid grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-gray-900">{summary.total}</div>
            <div className="text-sm text-gray-600">Total Images</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{summary.completed}</div>
            <div className="text-sm text-gray-600">Completed</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">{summary.in_progress}</div>
            <div className="text-sm text-gray-600">In Progress</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-red-600">{summary.failed}</div>
            <div className="text-sm text-gray-600">Failed</div>
          </div>
        </div>

        {!summary.all_completed && summary.in_progress > 0 && (
          <div className="mt-4">
            <div className="bg-gray-200 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${(summary.completed / summary.total) * 100}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Generating images... This may take a few minutes.
            </p>
          </div>
        )}
      </div>

      {/* Image Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(imageTypeLabels).map(([type, label]) => {
          const image = images.find(img => img.image_type === type);
          
          return (
            <motion.div
              key={type}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
            >
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{label}</h4>
                  {image && getStatusIcon(image.status)}
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  {imageTypeDescriptions[type]}
                </p>
                
                {image && image.status === 'completed' && image.image_url ? (
                  <div className="relative group cursor-pointer" onClick={() => setSelectedImage(image)}>
                    <img 
                      src={image.image_url} 
                      alt={label}
                      className="w-full h-48 object-cover rounded-lg"
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity rounded-lg flex items-center justify-center">
                      <Eye className="h-8 w-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </div>
                ) : (
                  <div className="bg-gray-100 rounded-lg h-48 flex items-center justify-center">
                    <div className="text-center">
                      {image ? getStatusIcon(image.status) : <Image className="h-8 w-8 text-gray-400 mx-auto" />}
                      <p className="text-sm text-gray-600 mt-2">
                        {image ? getStatusText(image.status) : 'Not started'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.2 }}
            className="max-w-4xl max-h-[90vh] relative"
          >
            <img 
              src={selectedImage.image_url} 
              alt={imageTypeLabels[selectedImage.image_type]}
              className="w-full h-full object-contain rounded-lg"
            />
            <button
              onClick={() => setSelectedImage(null)}
              className="absolute top-4 right-4 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100"
            >
              <XCircle className="h-6 w-6 text-gray-700" />
            </button>
            <div className="absolute bottom-4 left-4 bg-white rounded-lg px-4 py-2 shadow-lg">
              <p className="font-medium text-gray-900">
                {imageTypeLabels[selectedImage.image_type]}
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default ImageGenerationStatus;
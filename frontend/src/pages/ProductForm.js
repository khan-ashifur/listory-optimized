import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Sparkles, Upload, X, Image } from 'lucide-react';
import toast from 'react-hot-toast';
import { productAPI, listingAPI } from '../services/api';

const ProductForm = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedPlatform = location.state?.platform || 'amazon';
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    brand_name: '',
    brand_tone: 'professional',
    price: '',
    categories: '',
    features: '',
    competitor_urls: '',
    target_keywords: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [productImage, setProductImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const brandTones = [
    { value: 'professional', label: 'Professional' },
    { value: 'casual', label: 'Casual' },
    { value: 'luxury', label: 'Luxury' },
    { value: 'playful', label: 'Playful' },
    { value: 'minimal', label: 'Minimal' },
    { value: 'bold', label: 'Bold' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        toast.error('Image size should be less than 5MB');
        return;
      }
      
      setProductImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setProductImage(null);
    setImagePreview(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Create FormData for multipart upload
      const productFormData = new FormData();
      
      // Add all text fields
      Object.keys(formData).forEach(key => {
        productFormData.append(key, formData[key]);
      });
      
      // Add platform
      productFormData.append('target_platform', selectedPlatform);
      
      // Add image if exists
      if (productImage) {
        productFormData.append('product_image', productImage);
      }
      
      const productResponse = await productAPI.create(productFormData);
      const productId = productResponse.data.id;
      
      // Generate listing
      const listingResponse = await listingAPI.generate(productId, selectedPlatform);
      const listingId = listingResponse.data.id;
      
      toast.success('Listing generated successfully!');
      navigate(`/results/${listingId}`);
    } catch (error) {
      console.error('Error generating listing:', error);
      if (error.response?.status === 402) {
        toast.error('No credits remaining. Please upgrade your plan.');
      } else {
        toast.error('Failed to generate listing. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const getPlatformIcon = (platform) => {
    const icons = {
      amazon: '🛒',
      walmart: '🏪',
      etsy: '🎨',
      tiktok: '📱',
      shopify: '🛍️'
    };
    return icons[platform] || '🛒';
  };

  const getPlatformName = (platform) => {
    const names = {
      amazon: 'Amazon',
      walmart: 'Walmart',
      etsy: 'Etsy',
      tiktok: 'TikTok Shop',
      shopify: 'Shopify'
    };
    return names[platform] || 'Amazon';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <button
            onClick={() => navigate('/')}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Back to Platform Selection
          </button>
          
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <div className="flex items-center">
              <span className="text-3xl mr-4">{getPlatformIcon(selectedPlatform)}</span>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Create {getPlatformName(selectedPlatform)} Listing
                </h1>
                <p className="text-gray-600">
                  Tell us about your product and we'll generate an optimized listing
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <form onSubmit={handleSubmit} className="p-8 space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Product Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Enter your product name"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Brand Name *
                </label>
                <input
                  type="text"
                  name="brand_name"
                  value={formData.brand_name}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Your brand name"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Product Description *
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows="4"
                className="form-input"
                placeholder="Describe your product in detail..."
                required
              />
            </div>

            {/* Product Image Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Product Image
              </label>
              <div className="mt-1">
                {!imagePreview ? (
                  <label className="relative cursor-pointer bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-6 hover:border-primary-400 transition-colors">
                    <div className="text-center">
                      <Upload className="mx-auto h-12 w-12 text-gray-400" />
                      <p className="mt-2 text-sm text-gray-600">
                        Click to upload product image
                      </p>
                      <p className="text-xs text-gray-500">PNG, JPG up to 5MB</p>
                    </div>
                    <input
                      type="file"
                      className="sr-only"
                      accept="image/*"
                      onChange={handleImageChange}
                    />
                  </label>
                ) : (
                  <div className="relative">
                    <img
                      src={imagePreview}
                      alt="Product preview"
                      className="h-48 w-full object-cover rounded-lg"
                    />
                    <button
                      type="button"
                      onClick={removeImage}
                      className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                )}
              </div>
              <p className="mt-2 text-xs text-gray-500">
                Upload a clear image of your product for AI to generate better listing images
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Brand Tone
                </label>
                <select
                  name="brand_tone"
                  value={formData.brand_tone}
                  onChange={handleInputChange}
                  className="form-input"
                >
                  {brandTones.map(tone => (
                    <option key={tone.value} value={tone.value}>
                      {tone.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price ($)
                </label>
                <input
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleInputChange}
                  className="form-input"
                  placeholder="Product price"
                  step="0.01"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Categories
              </label>
              <input
                type="text"
                name="categories"
                value={formData.categories}
                onChange={handleInputChange}
                className="form-input"
                placeholder="Electronics, Home & Garden, Fashion (comma-separated)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Key Features
              </label>
              <textarea
                name="features"
                value={formData.features}
                onChange={handleInputChange}
                rows="3"
                className="form-input"
                placeholder="List your product's key features (comma-separated)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Competitor URLs
              </label>
              <textarea
                name="competitor_urls"
                value={formData.competitor_urls}
                onChange={handleInputChange}
                rows="2"
                className="form-input"
                placeholder="Paste competitor product URLs (one per line)"
              />
              <p className="text-sm text-gray-500 mt-1">
                We'll analyze these to help optimize your listing
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Keywords (Optional)
              </label>
              <input
                type="text"
                name="target_keywords"
                value={formData.target_keywords}
                onChange={handleInputChange}
                className="form-input"
                placeholder="wireless earbuds, bluetooth headphones, noise cancelling"
              />
            </div>

            <div className="pt-6">
              <button
                type="submit"
                disabled={isLoading}
                className={`w-full flex items-center justify-center ${
                  isLoading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'btn-primary hover:bg-primary-700'
                } py-4 text-lg`}
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                    Generating Your Listing...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5 mr-2" />
                    Generate {getPlatformName(selectedPlatform)} Listing
                  </>
                )}
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </div>
  );
};

export default ProductForm;
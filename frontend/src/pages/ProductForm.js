import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Sparkles, Plus, X, Globe, Info } from 'lucide-react';
import toast from 'react-hot-toast';
import { productAPI, listingAPI } from '../services/api';

const ProductForm = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedPlatform = location.state?.platform || 'amazon';
  
  const [formData, setFormData] = useState({
    // Required fields
    name: '',
    description: '',
    brand_name: '',
    marketplace: selectedPlatform === 'walmart' ? 'walmart_usa' : selectedPlatform === 'etsy' ? 'etsy' : 'us',
    price: '',
    categories: '',
    features: '',
    // Optional fields
    brand_tone: 'professional',
    brand_persona: '',
    target_audience: '',
    target_keywords: '',
    occasion: ''
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [showOptionalFields, setShowOptionalFields] = useState(false);
  const [customOccasion, setCustomOccasion] = useState('');

  const brandTones = [
    { value: 'professional', label: 'Professional' },
    { value: 'casual', label: 'Casual' },
    { value: 'luxury', label: 'Luxury' },
    { value: 'trendy', label: 'Trendy' },
    ...(selectedPlatform === 'etsy' ? [
      { value: 'handmade', label: 'Handmade', description: 'Emphasizes craftsmanship and personal touch' },
      { value: 'artistic', label: 'Artistic', description: 'Creative and expressive tone' },
      { value: 'vintage', label: 'Vintage', description: 'Classic and timeless appeal' },
      { value: 'bohemian', label: 'Bohemian', description: 'Free-spirited and eclectic style' },
      { value: 'minimalist', label: 'Minimalist', description: 'Clean, simple, and refined' },
      { value: 'luxury_craft', label: 'Luxury Craft', description: 'Premium handmade quality' },
      { value: 'eco_friendly', label: 'Eco-Friendly', description: 'Sustainable and environmentally conscious' },
      { value: 'whimsical', label: 'Whimsical', description: 'Playful and imaginative' },
      { value: 'rustic', label: 'Rustic', description: 'Natural and countryside charm' },
      { value: 'modern_craft', label: 'Modern Craft', description: 'Contemporary meets handmade' }
    ] : selectedPlatform !== 'walmart' ? [
      { value: 'playful', label: 'Playful' },
      { value: 'minimal', label: 'Minimal' },
      { value: 'bold', label: 'Bold' }
    ] : [])
  ];

  const getOccasions = () => {
    const baseOccasions = [
      { value: '', label: 'Select an Occasion (Optional)' },
      { value: 'christmas', label: '🎄 Christmas' },
      { value: 'black_friday', label: '🛍️ Black Friday' },
      { value: 'cyber_monday', label: '💻 Cyber Monday' },
      { value: 'mothers_day', label: '🌸 Mother\'s Day' },
      { value: 'fathers_day', label: '👔 Father\'s Day' },
      { value: 'halloween', label: '🎃 Halloween' },
      { value: 'easter', label: '🐰 Easter' },
      { value: 'birthday', label: '🎂 Birthday' },
      { value: 'graduation', label: '🎓 Graduation' },
      { value: 'anniversary', label: '💕 Anniversary' },
      { value: 'new_year', label: '🎉 New Year' },
      { value: 'back_to_school', label: '📚 Back to School' }
    ];

    if (selectedPlatform === 'etsy') {
      return [
        ...baseOccasions,
        { value: 'wedding', label: '💍 Wedding' },
        { value: 'baby_shower', label: '🍼 Baby Shower' },
        { value: 'valentines_day', label: '💝 Valentine\'s Day' },
        { value: 'housewarming', label: '🏠 Housewarming' },
        { value: 'bridal_shower', label: '👰 Bridal Shower' },
        { value: 'engagement', label: '💎 Engagement' },
        { value: 'thanksgiving', label: '🦃 Thanksgiving' },
        { value: 'custom', label: '✏️ Other (Custom)' }
      ];
    } else if (selectedPlatform === 'walmart') {
      return [
        ...baseOccasions,
        { value: 'thanksgiving', label: '🦃 Thanksgiving' },
        { value: 'independence_day', label: '🇺🇸 Independence Day (July 4th)' },
        { value: 'memorial_day', label: '🎖️ Memorial Day' },
        { value: 'labor_day', label: '🔨 Labor Day' },
        { value: 'valentines_day', label: '💝 Valentine\'s Day' },
        { value: 'wedding_season', label: '💍 Wedding Season' },
        { value: 'baby_shower', label: '🍼 Baby Shower' },
        { value: 'housewarming', label: '🏠 Housewarming' },
        { value: 'custom', label: '✏️ Other (Custom)' }
      ];
    } else {
      return [
        ...baseOccasions,
        { value: 'valentines', label: '💝 Valentine\'s Day' },
        { value: 'thanksgiving', label: '🦃 Thanksgiving' },
        { value: 'wedding', label: '💍 Wedding' },
        { value: 'custom', label: '✏️ Other (Custom)' }
      ];
    }
  };

  const amazonMarketplaces = [
    { value: 'us', label: 'United States', flag: '🇺🇸', language: 'en', domain: 'amazon.com' },
    { value: 'ca', label: 'Canada', flag: '🇨🇦', language: 'en', domain: 'amazon.ca' },
    { value: 'uk', label: 'United Kingdom', flag: '🇬🇧', language: 'en', domain: 'amazon.co.uk' },
    { value: 'de', label: 'Germany', flag: '🇩🇪', language: 'de', domain: 'amazon.de' },
    { value: 'fr', label: 'France', flag: '🇫🇷', language: 'fr', domain: 'amazon.fr' },
    { value: 'it', label: 'Italy', flag: '🇮🇹', language: 'it', domain: 'amazon.it' },
    { value: 'es', label: 'Spain', flag: '🇪🇸', language: 'es', domain: 'amazon.es' },
    { value: 'nl', label: 'Netherlands', flag: '🇳🇱', language: 'nl', domain: 'amazon.nl' },
    { value: 'se', label: 'Sweden', flag: '🇸🇪', language: 'sv', domain: 'amazon.se' },
    { value: 'pl', label: 'Poland', flag: '🇵🇱', language: 'pl', domain: 'amazon.pl' },
    { value: 'be', label: 'Belgium', flag: '🇧🇪', language: 'fr', domain: 'amazon.com.be' },
    { value: 'jp', label: 'Japan', flag: '🇯🇵', language: 'ja', domain: 'amazon.co.jp' },
    { value: 'in', label: 'India', flag: '🇮🇳', language: 'en', domain: 'amazon.in' },
    { value: 'sg', label: 'Singapore', flag: '🇸🇬', language: 'en', domain: 'amazon.sg' },
    { value: 'ae', label: 'UAE', flag: '🇦🇪', language: 'ar', domain: 'amazon.ae' },
    { value: 'mx', label: 'Mexico', flag: '🇲🇽', language: 'es-mx', domain: 'amazon.com.mx' },
    { value: 'sa', label: 'Saudi Arabia', flag: '🇸🇦', language: 'ar', domain: 'amazon.sa' },
    { value: 'br', label: 'Brazil', flag: '🇧🇷', language: 'pt-br', domain: 'amazon.com.br' },
    { value: 'au', label: 'Australia', flag: '🇦🇺', language: 'en', domain: 'amazon.com.au' },
    { value: 'tr', label: 'Turkey', flag: '🇹🇷', language: 'tr', domain: 'amazon.com.tr' },
    { value: 'eg', label: 'Egypt', flag: '🇪🇬', language: 'ar', domain: 'amazon.eg' }
  ];

  const walmartMarketplaces = [
    { value: 'walmart_usa', label: 'United States', flag: '🇺🇸', language: 'en-us', domain: 'walmart.com' },
    { value: 'walmart_canada', label: 'Canada', flag: '🇨🇦', language: 'en-ca', domain: 'walmart.ca' },
    { value: 'walmart_mexico', label: 'Mexico', flag: '🇲🇽', language: 'es-mx', domain: 'walmart.com.mx' }
  ];

  const etsyMarketplaces = [
    { value: 'etsy', label: 'Global Marketplace', flag: '🌍', language: 'en', domain: 'etsy.com' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleArrayInputChange = (field, index, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].map((item, i) => i === index ? value : item)
    }));
  };

  const addArrayField = (field) => {
    setFormData(prev => ({
      ...prev,
      [field]: [...prev[field], '']
    }));
  };

  const removeArrayField = (field, index) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index)
    }));
  };

  const getSelectedMarketplace = () => {
    if (selectedPlatform === 'walmart') {
      return walmartMarketplaces.find(m => m.value === formData.marketplace);
    } else if (selectedPlatform === 'etsy') {
      return etsyMarketplaces.find(m => m.value === formData.marketplace);
    } else {
      return amazonMarketplaces.find(m => m.value === formData.marketplace);
    }
  };

  const getCurrentMarketplaces = () => {
    if (selectedPlatform === 'walmart') {
      return walmartMarketplaces;
    } else if (selectedPlatform === 'etsy') {
      return etsyMarketplaces;
    } else {
      return amazonMarketplaces;
    }
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    let productId = null;
    
    try {
      // Create product data
      const selectedMarketplace = getSelectedMarketplace();
      const productData = {
        ...formData,
        target_platform: selectedPlatform,
        marketplace: formData.marketplace,
        marketplace_language: selectedMarketplace?.language || 'en',
        // Handle occasion - use custom input if 'custom' is selected, otherwise use selected value
        occasion: formData.occasion === 'custom' ? customOccasion : formData.occasion
      };
      
      try {
        const productResponse = await productAPI.create(productData);
        productId = productResponse.data.id;
      } catch (productError) {
        console.error('Product creation error:', productError);
        
        // If product creation fails with 500, it might still be created due to Unicode console error
        // Try to find the recently created product
        if (productError.response?.status === 500) {
          console.log('Attempting to find recently created product...');
          try {
            const productsResponse = await productAPI.list();
            // Find the most recent product that matches our data
            const recentProduct = productsResponse.data.results?.find(p => 
              p.name === productData.name && 
              p.brand_name === productData.brand_name &&
              p.target_platform === productData.target_platform
            );
            
            if (recentProduct) {
              productId = recentProduct.id;
              console.log('Found recently created product:', productId);
              toast.success('Product created successfully!');
            } else {
              throw new Error('Product creation failed and could not locate created product');
            }
          } catch (findError) {
            console.error('Could not find created product:', findError);
            throw productError; // Re-throw original error
          }
        } else {
          throw productError; // Re-throw non-500 errors
        }
      }
      
      if (!productId) {
        throw new Error('No product ID available');
      }
      
      // Generate listing
      const listingResponse = await listingAPI.generate(productId, selectedPlatform);
      const listingId = listingResponse.data.id;
      
      toast.success('Listing generated successfully!');
      navigate(`/results/${listingId}`);
      
    } catch (error) {
      console.error('Error in product form:', error);
      if (error.response?.status === 402) {
        toast.error('No credits remaining. Please upgrade your plan.');
      } else if (error.message?.includes('Product creation failed')) {
        toast.error('Failed to create product. Please try again.');
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
            {/* Marketplace Selection - For Amazon, Walmart, and Etsy */}
            <div className={`${
              selectedPlatform === 'amazon' ? 'bg-blue-50 border-blue-200' : 
              selectedPlatform === 'walmart' ? 'bg-green-50 border-green-200' : 
              selectedPlatform === 'etsy' ? 'bg-orange-50 border-orange-200' : 
              'bg-gray-50 border-gray-200'
            } border rounded-lg p-4 mb-6`}>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Globe className="inline h-4 w-4 mr-1" />
                {selectedPlatform === 'amazon' ? 'Amazon' : 
                 selectedPlatform === 'walmart' ? 'Walmart' : 
                 selectedPlatform === 'etsy' ? 'Etsy' : 'Platform'} Marketplace *
              </label>
              <select
                name="marketplace"
                value={formData.marketplace}
                onChange={handleInputChange}
                className="form-input"
                required
              >
                {getCurrentMarketplaces().map(market => (
                  <option key={market.value} value={market.value}>
                    {market.flag} {market.label} ({market.domain})
                  </option>
                ))}
              </select>
              {formData.marketplace && (
                <p className={`text-sm mt-2 ${
                  selectedPlatform === 'amazon' ? 'text-blue-600' : 
                  selectedPlatform === 'walmart' ? 'text-green-600' : 
                  selectedPlatform === 'etsy' ? 'text-orange-600' : 
                  'text-gray-600'
                }`}>
                  <Info className="inline h-3 w-3 mr-1" />
                  Listing will be generated in {getSelectedMarketplace()?.language === 'en' || getSelectedMarketplace()?.language === 'en-us' || getSelectedMarketplace()?.language === 'en-ca' ? 'English' : 
                    getSelectedMarketplace()?.language === 'es-mx' ? 'Spanish (Mexico)' :
                    `${getSelectedMarketplace()?.label}'s local language`}
                  {selectedPlatform === 'walmart' && (
                    <span className="block mt-1 text-xs">
                      💡 Brand tone helps optimize Walmart content quality
                    </span>
                  )}
                  {selectedPlatform === 'etsy' && (
                    <span className="block mt-1 text-xs">
                      🎨 Optimized for Etsy's handmade and artistic marketplace
                    </span>
                  )}
                </p>
              )}
            </div>

            {/* Required Fields Section */}
            <div className="border-b pb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Required Information</h3>
              
              <div className="grid md:grid-cols-2 gap-6 mb-6">
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


              <div className="mb-6">
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

              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Price * ($)
                  </label>
                  <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="29.99"
                    step="0.01"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Categories *
                  </label>
                  <input
                    type="text"
                    name="categories"
                    value={formData.categories}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Electronics, Home & Garden"
                    required
                  />
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Key Features *
                </label>
                <textarea
                  name="features"
                  value={formData.features}
                  onChange={handleInputChange}
                  rows="3"
                  className="form-input"
                  placeholder="List your product's key features (one per line)"
                  required
                />
              </div>
            </div>

            {/* Optional Fields Section */}
            <div className="pt-6">
              <button
                type="button"
                onClick={() => setShowOptionalFields(!showOptionalFields)}
                className="flex items-center text-primary-600 hover:text-primary-700 font-medium mb-4"
              >
                {showOptionalFields ? (
                  <>
                    <X className="h-4 w-4 mr-2" />
                    Hide Optional Fields
                  </>
                ) : (
                  <>
                    <Plus className="h-4 w-4 mr-2" />
                    Add Optional Information (Recommended for Better Results)
                  </>
                )}
              </button>

              {showOptionalFields && (
                <div className="space-y-6 pt-4 border-t">
                  <h3 className="text-lg font-semibold text-gray-900">Optional Information</h3>
                  
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Brand Tone
                        {selectedPlatform === 'walmart' && <span className="text-xs text-green-600 block">Recommended for better Walmart optimization</span>}
                        {selectedPlatform === 'etsy' && <span className="text-xs text-orange-600 block">Optional - defaults to 'handmade' if not selected</span>}
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
                      {selectedPlatform === 'walmart' && formData.brand_tone && (
                        <p className="text-xs text-green-600 mt-1">
                          ✓ Walmart content will be optimized for {brandTones.find(t => t.value === formData.brand_tone)?.label.toLowerCase()} tone
                        </p>
                      )}
                      {selectedPlatform === 'etsy' && formData.brand_tone && (
                        <p className="text-xs text-orange-600 mt-1">
                          ✓ {brandTones.find(t => t.value === formData.brand_tone)?.description || 
                             `Etsy listing optimized for ${brandTones.find(t => t.value === formData.brand_tone)?.label.toLowerCase()} tone`}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Target Keywords
                      </label>
                      <input
                        type="text"
                        name="target_keywords"
                        value={formData.target_keywords}
                        onChange={handleInputChange}
                        className="form-input"
                        placeholder="wireless earbuds, bluetooth headphones"
                      />
                    </div>
                  </div>

                  {/* Occasion Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Special Occasion
                    </label>
                    <select
                      name="occasion"
                      value={formData.occasion}
                      onChange={(e) => {
                        handleInputChange(e);
                        if (e.target.value !== 'custom') {
                          setCustomOccasion('');
                        }
                      }}
                      className="form-input"
                    >
                      {getOccasions().map(occasion => (
                        <option key={occasion.value} value={occasion.value}>
                          {occasion.label}
                        </option>
                      ))}
                    </select>
                    
                    {formData.occasion === 'custom' && (
                      <div className="mt-3">
                        <input
                          type="text"
                          value={customOccasion}
                          onChange={(e) => setCustomOccasion(e.target.value)}
                          className="form-input"
                          placeholder="Enter custom occasion (e.g., Baby Shower, Housewarming)"
                        />
                      </div>
                    )}
                    
                    <p className="text-sm text-gray-500 mt-1">
                      Select an occasion to generate themed content and keywords
                    </p>
                  </div>

                  {selectedPlatform === 'amazon' && (
                    <>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Brand Persona
                        </label>
                        <textarea
                          name="brand_persona"
                          value={formData.brand_persona}
                          onChange={handleInputChange}
                          rows="3"
                          className="form-input"
                          placeholder="Describe your brand's personality, values, and voice. E.g., 'Innovative tech company focused on simplifying daily life through intuitive design and reliable performance.'"
                        />
                        <p className="text-sm text-gray-500 mt-1">
                          This helps create a consistent brand voice across your listing
                        </p>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Target Audience
                        </label>
                        <textarea
                          name="target_audience"
                          value={formData.target_audience}
                          onChange={handleInputChange}
                          rows="3"
                          className="form-input"
                          placeholder="Describe your ideal customer. E.g., 'Tech-savvy professionals aged 25-45 who value productivity and efficiency in their daily workflow.'"
                        />
                        <p className="text-sm text-gray-500 mt-1">
                          Understanding your audience helps tailor the listing's messaging
                        </p>
                      </div>

                    </>
                  )}
                </div>
              )}
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
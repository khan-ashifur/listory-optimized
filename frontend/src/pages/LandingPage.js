import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShoppingBag, Target, Zap, TrendingUp } from 'lucide-react';
import PlatformSelector from '../components/PlatformSelector';

const LandingPage = () => {
  const [selectedPlatform, setSelectedPlatform] = useState('');
  const navigate = useNavigate();

  const platforms = [
    { 
      id: 'amazon', 
      name: 'Amazon', 
      icon: '🛒',
      description: 'Generate optimized listings with A+ content, keywords, and SEO',
      features: ['A+ Content Suggestions', 'Backend Keywords', 'Bullet Points', 'Title Optimization']
    },
    { 
      id: 'walmart', 
      name: 'Walmart', 
      icon: '🏪',
      description: 'Create marketplace-ready listings with rich product details',
      features: ['Rich Descriptions', 'Key Features', 'Specifications', 'Search Optimization']
    },
    { 
      id: 'etsy', 
      name: 'Etsy', 
      icon: '🎨',
      description: 'Craft story-driven listings that connect with buyers',
      features: ['Story-driven Copy', '13 SEO Tags', 'Materials List', 'Personal Touch']
    },
    { 
      id: 'tiktok', 
      name: 'TikTok Shop', 
      icon: '📱',
      description: 'Generate viral-ready content with video script ideas',
      features: ['Video Scripts', 'Trending Hashtags', 'Hook Ideas', 'Gen Z Copy']
    },
    { 
      id: 'shopify', 
      name: 'Shopify', 
      icon: '🛍️',
      description: 'Build conversion-focused product pages with SEO',
      features: ['SEO Optimization', 'Meta Descriptions', 'HTML Formatting', 'Conversion Copy']
    }
  ];

  const handleGetStarted = () => {
    if (selectedPlatform) {
      navigate('/create', { state: { platform: selectedPlatform } });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Navigation Header */}
      <nav className="absolute top-0 left-0 right-0 z-50 bg-transparent">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <ShoppingBag className="h-8 w-8 text-white mr-2" />
              <span className="text-2xl font-bold text-white">Listory</span>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="px-6 py-2 bg-white text-blue-600 font-semibold rounded-full hover:bg-yellow-300 hover:text-blue-700 transition shadow-lg"
              >
                Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="gradient-bg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <div className="flex justify-center mb-6">
              <div className="bg-white p-4 rounded-full shadow-lg">
                <ShoppingBag className="h-12 w-12 text-blue-600" />
              </div>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Welcome to <span className="text-yellow-300">Listory</span>
            </h1>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Generate high-converting product listings for Amazon, Walmart, Etsy, TikTok Shop, and Shopify. 
              Our AI creates optimized content that sells.
            </p>
            <div className="flex justify-center space-x-4">
              <div className="flex items-center text-white">
                <Target className="h-5 w-5 mr-2" />
                <span>AI-Powered</span>
              </div>
              <div className="flex items-center text-white">
                <Zap className="h-5 w-5 mr-2" />
                <span>5 Platforms</span>
              </div>
              <div className="flex items-center text-white">
                <TrendingUp className="h-5 w-5 mr-2" />
                <span>Higher Conversions</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Platform Selection */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Platform
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Select the marketplace where you want to create your optimized product listing
          </p>
        </motion.div>

        <PlatformSelector
          platforms={platforms}
          selectedPlatform={selectedPlatform}
          onPlatformSelect={setSelectedPlatform}
        />

        {selectedPlatform && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center mt-12"
          >
            <button
              onClick={handleGetStarted}
              className="btn-primary text-lg px-12 py-4"
            >
              Get Started with {platforms.find(p => p.id === selectedPlatform)?.name} ✨
            </button>
          </motion.div>
        )}
      </div>

      {/* Features Section */}
      <div className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Sell More
            </h2>
            <p className="text-xl text-gray-600">
              Comprehensive listing optimization for every major platform
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="text-center p-8 rounded-xl bg-blue-50"
            >
              <div className="bg-blue-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Target className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                AI-Powered Content
              </h3>
              <p className="text-gray-600">
                Advanced AI analyzes your product and creates compelling, optimized content that converts visitors into buyers.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-center p-8 rounded-xl bg-purple-50"
            >
              <div className="bg-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Zap className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Multi-Platform Ready
              </h3>
              <p className="text-gray-600">
                Generate optimized listings for Amazon, Walmart, Etsy, TikTok Shop, and Shopify with platform-specific features.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="text-center p-8 rounded-xl bg-green-50"
            >
              <div className="bg-green-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <TrendingUp className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Boost Conversions
              </h3>
              <p className="text-gray-600">
                Our optimized listings are designed to rank higher in search results and convert more browsers into buyers.
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
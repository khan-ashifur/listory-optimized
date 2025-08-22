import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Copy, Download, Star, Heart, Share2, Camera, 
  DollarSign, TrendingUp, Users, MessageCircle, 
  ShoppingBag, Calendar, Instagram, Target, 
  BarChart3, Zap, Crown, Gift, MapPin, Award, Clock, Tag
} from 'lucide-react';
import toast from 'react-hot-toast';

const EtsyPremiumResults = ({ listing }) => {
  const [activeTab, setActiveTab] = useState('listing');
  
  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copied to clipboard!`);
  };

  const WOWFeatureTabs = [
    { id: 'listing', label: '🎨 Listing Content', icon: Star, description: 'Perfect Etsy listing' },
    { id: 'shop_setup', label: '🏪 Shop Setup', icon: Crown, description: 'Complete shop guide' },
    { id: 'social_media', label: '📱 Social Media', icon: Instagram, description: '30-day content plan' },
    { id: 'photography', label: '📸 Photography', icon: Camera, description: 'Pro photo guide' },
    { id: 'pricing', label: '💰 Pricing Strategy', icon: DollarSign, description: 'Smart pricing analysis' },
    { id: 'seo', label: '🔍 SEO Report', icon: TrendingUp, description: 'Traffic optimization' },
    { id: 'customer_service', label: '💌 Customer Service', icon: MessageCircle, description: 'Email templates' },
    { id: 'policies', label: '📋 Shop Policies', icon: Award, description: 'Legal protection' },
    { id: 'variations', label: '🎯 Upsells & Variations', icon: Target, description: 'Revenue optimization' },
    { id: 'competitor', label: '🕵️ Market Intelligence', icon: BarChart3, description: 'Competitor insights' },
    { id: 'seasonal', label: '📅 Marketing Calendar', icon: Calendar, description: '12-month strategy' }
  ];

  const EtsyFieldDisplay = ({ label, content, copyLabel, icon: Icon }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
    >
      <div className="p-4 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {Icon && <Icon className="h-5 w-5 text-purple-600" />}
          <h3 className="text-lg font-semibold text-gray-900">{label}</h3>
        </div>
        <button
          onClick={() => copyToClipboard(content, copyLabel)}
          className="text-sm bg-purple-100 text-purple-700 px-3 py-1 rounded-md hover:bg-purple-200 transition-colors flex items-center space-x-1"
        >
          <Copy className="h-4 w-4" />
          <span>Copy</span>
        </button>
      </div>
      <div className="p-4">
        <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
          {content}
        </div>
      </div>
    </motion.div>
  );

  const renderListingContent = () => (
    <div className="space-y-6">
      {/* Hero Stats */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-6 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">🎉 Premium Etsy Listing Generated!</h2>
            <p className="text-purple-100">Ready to dominate Etsy with professional-grade content</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">90%+</div>
            <div className="text-sm text-purple-100">Quality Score</div>
          </div>
        </div>
        
        <div className="grid grid-cols-4 gap-4 mt-6">
          <div className="text-center">
            <div className="text-lg font-semibold">{listing.etsy_title?.length || 0}/140</div>
            <div className="text-xs text-purple-200">Title Characters</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold">13</div>
            <div className="text-xs text-purple-200">SEO Tags</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold">{listing.keywords?.split(',').length || 0}</div>
            <div className="text-xs text-purple-200">Keywords</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold">6</div>
            <div className="text-xs text-purple-200">Description Sections</div>
          </div>
        </div>
      </motion.div>

      {/* Core Etsy Fields */}
      <div className="grid gap-6">
        <EtsyFieldDisplay
          label="📝 Etsy Title (SEO Optimized)"
          content={listing.etsy_title || listing.title || 'No title available'}
          copyLabel="Title"
          icon={Star}
        />
        
        <EtsyFieldDisplay
          label="🏷️ 13 Strategic Tags"
          content={listing.etsy_tags ? 
            JSON.parse(listing.etsy_tags).map((tag, index) => `${index + 1}. ${tag}`).join('\n') : 
            'No tags available'}
          copyLabel="Tags"
          icon={Tag}
        />
        
        <EtsyFieldDisplay
          label="📄 Complete Description (6 Sections)"
          content={listing.etsy_description || listing.long_description || 'No description available'}
          copyLabel="Description"
          icon={MessageCircle}
        />
        
        <EtsyFieldDisplay
          label="🧱 Materials List"
          content={listing.etsy_materials || 'Premium quality materials, ethically sourced'}
          copyLabel="Materials"
          icon={Award}
        />
        
        <EtsyFieldDisplay
          label="⏱️ Processing Time"
          content={listing.etsy_processing_time || '3-5 business days'}
          copyLabel="Processing Time"
          icon={Clock}
        />
        
        <EtsyFieldDisplay
          label="🔍 Keywords for SEO"
          content={listing.keywords || 'No keywords available'}
          copyLabel="Keywords"
          icon={TrendingUp}
        />
      </div>
    </div>
  );

  const renderWOWFeature = (featureId) => {
    const featureContent = {
      shop_setup: listing.etsy_shop_setup_guide,
      social_media: listing.etsy_social_media_package,
      photography: listing.etsy_photography_guide,
      pricing: listing.etsy_pricing_analysis,
      seo: listing.etsy_seo_report,
      customer_service: listing.etsy_customer_service_templates,
      policies: listing.etsy_policies_templates,
      variations: listing.etsy_variations_guide,
      competitor: listing.etsy_competitor_insights,
      seasonal: listing.etsy_seasonal_calendar
    };

    const content = featureContent[featureId];
    const feature = WOWFeatureTabs.find(tab => tab.id === featureId);

    if (!content) {
      return (
        <div className="text-center py-12">
          <div className="text-gray-400 text-lg">
            {feature?.label} content not available
          </div>
        </div>
      );
    }

    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Feature Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 text-white">
          <div className="flex items-center space-x-3">
            <feature.icon className="h-8 w-8" />
            <div>
              <h2 className="text-2xl font-bold">{feature.label}</h2>
              <p className="text-indigo-100">{feature.description}</p>
            </div>
          </div>
          <div className="mt-4 flex items-center space-x-4">
            <button
              onClick={() => copyToClipboard(content, feature.label)}
              className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
            >
              <Copy className="h-4 w-4" />
              <span>Copy All Content</span>
            </button>
            <div className="text-indigo-100 text-sm">
              🎯 Exclusive Feature - Not Available Anywhere Else!
            </div>
          </div>
        </div>

        {/* Feature Content */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="p-6">
            <div className="prose prose-sm max-w-none whitespace-pre-wrap text-gray-700">
              {content}
            </div>
          </div>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Premium Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-3 rounded-lg">
                  <Crown className="h-8 w-8 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">
                    Premium Etsy Business Package
                  </h1>
                  <p className="text-gray-600">
                    Complete business toolkit - Everything you need to dominate Etsy
                  </p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-gray-500">Estimated Value</div>
                <div className="text-3xl font-bold text-green-600">$497</div>
                <div className="text-sm text-gray-500">Included FREE</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Navigation Tabs */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2">
            {WOWFeatureTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'bg-white text-gray-700 border border-gray-200 hover:bg-purple-50'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <tab.icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Content Display */}
        <div className="space-y-8">
          {activeTab === 'listing' ? renderListingContent() : renderWOWFeature(activeTab)}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 bg-gradient-to-r from-green-600 to-blue-600 rounded-xl p-8 text-white text-center"
        >
          <h3 className="text-2xl font-bold mb-4">
            🚀 Your Etsy Empire Starts Here!
          </h3>
          <p className="text-lg text-green-100 mb-6">
            You now have everything professional Etsy sellers pay $497+ for. 
            Start implementing these strategies today!
          </p>
          <div className="flex justify-center space-x-4">
            <button className="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Download Complete Package
            </button>
            <button className="bg-green-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-800 transition-colors">
              Generate Another Listing
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default EtsyPremiumResults;
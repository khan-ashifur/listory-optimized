import React from 'react';
import { motion } from 'framer-motion';
import { Plus, Clock, CheckCircle, AlertCircle } from 'lucide-react';

const Dashboard = () => {
  const mockListings = [
    {
      id: 1,
      name: 'Wireless Bluetooth Earbuds',
      platform: 'amazon',
      status: 'completed',
      createdAt: '2024-01-15',
      icon: '🛒'
    },
    {
      id: 2,
      name: 'Handmade Ceramic Mug',
      platform: 'etsy',
      status: 'processing',
      createdAt: '2024-01-14',
      icon: '🎨'
    },
    {
      id: 3,
      name: 'Smartphone Case',
      platform: 'tiktok',
      status: 'completed',
      createdAt: '2024-01-13',
      icon: '📱'
    }
  ];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'processing':
        return <Clock className="h-5 w-5 text-yellow-500" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getPlatformName = (platform) => {
    const names = {
      amazon: 'Amazon',
      walmart: 'Walmart',
      etsy: 'Etsy',
      tiktok: 'TikTok Shop',
      shopify: 'Shopify'
    };
    return names[platform] || platform;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  Welcome back! 👋
                </h1>
                <p className="text-gray-600">
                  Manage your product listings and track their performance
                </p>
              </div>
              <button className="btn-primary flex items-center">
                <Plus className="h-4 w-4 mr-2" />
                Create New Listing
              </button>
            </div>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="grid md:grid-cols-4 gap-6 mb-8"
        >
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="bg-blue-100 p-3 rounded-full">
                <CheckCircle className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">12</p>
                <p className="text-gray-600 text-sm">Total Listings</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="bg-green-100 p-3 rounded-full">
                <Clock className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">8</p>
                <p className="text-gray-600 text-sm">This Month</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="bg-purple-100 p-3 rounded-full">
                <Plus className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">5</p>
                <p className="text-gray-600 text-sm">Platforms</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="bg-yellow-100 p-3 rounded-full">
                <AlertCircle className="h-6 w-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-bold text-gray-900">15</p>
                <p className="text-gray-600 text-sm">Credits Left</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Recent Listings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Recent Listings</h2>
          </div>
          
          <div className="divide-y divide-gray-200">
            {mockListings.map((listing) => (
              <div key={listing.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="text-2xl mr-4">{listing.icon}</span>
                    <div>
                      <h3 className="font-medium text-gray-900">{listing.name}</h3>
                      <p className="text-sm text-gray-600">
                        {getPlatformName(listing.platform)} • Created {listing.createdAt}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center">
                      {getStatusIcon(listing.status)}
                      <span className="ml-2 text-sm text-gray-600 capitalize">
                        {listing.status}
                      </span>
                    </div>
                    <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
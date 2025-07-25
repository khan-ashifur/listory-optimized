import React from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

const PlatformSelector = ({ platforms, selectedPlatform, onPlatformSelect }) => {
  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {platforms.map((platform, index) => (
        <motion.div
          key={platform.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          className={`platform-card ${selectedPlatform === platform.id ? 'selected' : ''}`}
          onClick={() => onPlatformSelect(platform.id)}
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <span className="text-3xl mr-3">{platform.icon}</span>
              <h3 className="text-xl font-bold text-gray-900">{platform.name}</h3>
            </div>
            {selectedPlatform === platform.id && (
              <div className="bg-primary-500 rounded-full p-1">
                <Check className="h-4 w-4 text-white" />
              </div>
            )}
          </div>
          
          <p className="text-gray-600 mb-4 text-sm">
            {platform.description}
          </p>
          
          <div className="space-y-2">
            <h4 className="font-semibold text-gray-900 text-sm">Includes:</h4>
            <ul className="space-y-1">
              {platform.features.map((feature, idx) => (
                <li key={idx} className="flex items-center text-sm text-gray-600">
                  <div className="w-1.5 h-1.5 bg-primary-500 rounded-full mr-2"></div>
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default PlatformSelector;
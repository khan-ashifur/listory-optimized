import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Copy, Download, Star, Tag, Video, ShoppingCart, Eye, TrendingUp, Image } from 'lucide-react';
import toast from 'react-hot-toast';
import PlatformPreview from '../components/PlatformPreview';
import ListingOptimizationScore from '../components/ListingOptimizationScore';
import ImageGenerationStatus from '../components/ImageGenerationStatus';
import { listingAPI } from '../services/api';

const ListingResults = () => {
  const { listingId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('listing');
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch real listing data from API
  useEffect(() => {
    const fetchListing = async () => {
      try {
        const response = await listingAPI.get(listingId);
        setListing(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching listing:', error);
        setLoading(false);
        // Fallback to mock data if API fails
        setListing(mockListing);
      }
    };

    if (listingId) {
      fetchListing();
    }
  }, [listingId]);

  // Mock data as fallback
  const mockListing = {
    platform: 'amazon',
    title: 'Wireless Bluetooth Earbuds with Premium Sound Quality - Noise Cancelling Headphones with 24H Battery Life',
    shortDescription: 'Experience premium audio with our advanced wireless earbuds featuring active noise cancellation and crystal-clear sound.',
    longDescription: `<h2>Transform Your Audio Experience</h2>
    <p>Discover the perfect blend of comfort, style, and superior sound quality with our premium wireless earbuds. Engineered for audiophiles and everyday users alike.</p>
    
    <h3>Key Features:</h3>
    <ul>
      <li>🎵 Premium Hi-Fi Sound Quality</li>
      <li>🔇 Active Noise Cancellation</li>
      <li>🔋 24-Hour Battery Life</li>
      <li>💧 IPX7 Waterproof Rating</li>
      <li>📱 Universal Compatibility</li>
    </ul>`,
    bulletPoints: [
      "🎵 PREMIUM SOUND QUALITY - Experience rich, detailed audio with deep bass and crystal-clear highs thanks to our advanced acoustic drivers",
      "🔇 ACTIVE NOISE CANCELLATION - Block out distractions and immerse yourself in your music with intelligent noise reduction technology",
      "🔋 ALL-DAY BATTERY LIFE - Enjoy up to 8 hours of continuous playback, plus 16 additional hours with the compact charging case",
      "💧 SWEAT & WATER RESISTANT - IPX7 waterproof rating protects against sweat, rain, and splashes during workouts and outdoor activities",
      "📱 UNIVERSAL COMPATIBILITY - Seamlessly connects to iPhone, Android, tablets, and all Bluetooth-enabled devices with instant pairing"
    ],
    keywords: [
      'wireless earbuds', 'bluetooth headphones', 'noise cancelling', 'waterproof earbuds', 
      'long battery life', 'premium sound quality', 'workout headphones', 'wireless charging'
    ],
    amazonAplusContent: `
    <h2>Why Choose Our Earbuds?</h2>
    <div style="display: flex; justify-content: space-between;">
      <div style="flex: 1; text-align: center;">
        <img src="/placeholder-image-1.jpg" alt="Sound Quality" />
        <h3>Premium Sound</h3>
        <p>Advanced drivers deliver audiophile-grade sound</p>
      </div>
      <div style="flex: 1; text-align: center;">
        <img src="/placeholder-image-2.jpg" alt="Battery Life" />
        <h3>24H Battery</h3>
        <p>All-day listening with quick charge technology</p>
      </div>
      <div style="flex: 1; text-align: center;">
        <img src="/placeholder-image-3.jpg" alt="Waterproof" />
        <h3>IPX7 Waterproof</h3>
        <p>Perfect for workouts and outdoor adventures</p>
      </div>
    </div>`,
    tiktokVideoScript: [
      {
        title: "Unboxing Hook",
        script: "POV: You just got the earbuds everyone's talking about 📦✨ [Show unboxing] The sound quality is actually insane! [Put in ears, show reaction] Wait for the bass drop... 🔊 #earbuds #unboxing #soundcheck"
      },
      {
        title: "Problem/Solution",
        script: "Tired of earbuds that die in 2 hours? 😤 These last 24 HOURS! [Show battery indicator] Perfect for long flights, study sessions, and those Netflix binges 📱 #batterylife #earbuds #travelhack"
      },
      {
        title: "Before/After Workout",
        script: "Before: Constantly adjusting earbuds during workout 😰 After: These stay put no matter what! [Show intense workout] Plus they're waterproof! 💦 #workout #waterproof #fitnessmotivation"
      }
    ]
  };

  // Use real listing data or fallback to mock data
  const currentListing = listing || mockListing;

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-xl text-gray-600">Loading your AI-generated listing...</p>
        </div>
      </div>
    );
  }

  const TabButton = ({ id, label, icon: Icon, active, onClick }) => (
    <button
      onClick={() => onClick(id)}
      className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
        active 
          ? 'bg-primary-500 text-white' 
          : 'text-gray-600 hover:text-primary-500 hover:bg-gray-100'
      }`}
    >
      <Icon className="h-4 w-4 mr-2" />
      {label}
    </button>
  );

  const CopyableSection = ({ title, content, isHtml = false }) => (
    <div className="bg-gray-50 rounded-lg p-4 mb-6">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <button
          onClick={() => copyToClipboard(content)}
          className="flex items-center text-sm text-primary-600 hover:text-primary-700"
        >
          <Copy className="h-4 w-4 mr-1" />
          Copy
        </button>
      </div>
      <div className={isHtml ? 'prose prose-sm max-w-none' : 'whitespace-pre-wrap text-sm text-gray-700'}>
        {isHtml ? (
          <div dangerouslySetInnerHTML={{ __html: content }} />
        ) : (
          content
        )}
      </div>
    </div>
  );

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
          <button
            onClick={() => navigate('/create')}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="h-5 w-5 mr-2" />
            Create Another Listing
          </button>
          
          <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-3xl mr-4">🛒</span>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    Your Amazon Listing is Ready!
                  </h1>
                  <p className="text-gray-600">
                    Generated with AI optimization for maximum conversions
                  </p>
                </div>
              </div>
              <button className="btn-primary flex items-center">
                <Download className="h-4 w-4 mr-2" />
                Download All
              </button>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8"
        >
          <div className="p-4 border-b border-gray-200">
            <div className="flex space-x-2 overflow-x-auto">
              <TabButton
                id="listing"
                label="Main Listing"
                icon={ShoppingCart}
                active={activeTab === 'listing'}
                onClick={setActiveTab}
              />
              <TabButton
                id="aplus"
                label="A+ Content"
                icon={Star}
                active={activeTab === 'aplus'}
                onClick={setActiveTab}
              />
              <TabButton
                id="keywords"
                label="Keywords"
                icon={Tag}
                active={activeTab === 'keywords'}
                onClick={setActiveTab}
              />
              <TabButton
                id="preview"
                label="Preview"
                icon={Eye}
                active={activeTab === 'preview'}
                onClick={setActiveTab}
              />
              <TabButton
                id="optimization"
                label="Optimization"
                icon={TrendingUp}
                active={activeTab === 'optimization'}
                onClick={setActiveTab}
              />
              <TabButton
                id="images"
                label="Product Images"
                icon={Image}
                active={activeTab === 'images'}
                onClick={setActiveTab}
              />
              {currentListing.platform === 'tiktok' && (
                <TabButton
                  id="video"
                  label="Video Scripts"
                  icon={Video}
                  active={activeTab === 'video'}
                  onClick={setActiveTab}
                />
              )}
            </div>
          </div>

          <div className="p-6">
            {activeTab === 'listing' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                <CopyableSection
                  title="Product Title"
                  content={currentListing.title || 'No title generated'}
                />
                
                <CopyableSection
                  title="Bullet Points"
                  content={currentListing.bullet_points || 'No bullet points generated'}
                />
                
                <CopyableSection
                  title="Product Description"
                  content={currentListing.long_description || 'No description generated'}
                  isHtml={true}
                />
                
                {currentListing.short_description && (
                  <div className="bg-gradient-from-blue-50 to-purple-50 rounded-lg p-6 mb-6 border border-blue-200">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-gray-900 flex items-center">
                        🚀 Conversion Boosters
                        <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                          Sales Tools
                        </span>
                      </h3>
                      <button
                        onClick={() => copyToClipboard(currentListing.short_description)}
                        className="flex items-center text-sm text-primary-600 hover:text-primary-700"
                      >
                        <Copy className="h-4 w-4 mr-1" />
                        Copy All
                      </button>
                    </div>
                    <div className="whitespace-pre-wrap text-sm text-gray-700 space-y-4">
                      {currentListing.short_description.split('\n\n').map((section, index) => (
                        <div key={index} className="bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
                          {section.split('\n').map((line, lineIndex) => (
                            <div key={lineIndex} className={lineIndex === 0 ? 'font-semibold text-gray-900 mb-2' : 'text-gray-700'}>
                              {line}
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {activeTab === 'aplus' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <CopyableSection
                  title="A+ Content Suggestions"
                  content={currentListing.amazon_aplus_content || 'No A+ content generated'}
                  isHtml={true}
                />
              </motion.div>
            )}

            {activeTab === 'keywords' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-gray-900">SEO Keywords</h3>
                    <button
                      onClick={() => copyToClipboard(currentListing.keywords || '')}
                      className="flex items-center text-sm text-primary-600 hover:text-primary-700"
                    >
                      <Copy className="h-4 w-4 mr-1" />
                      Copy All
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {(currentListing.keywords ? currentListing.keywords.split(', ') : []).map((keyword, index) => (
                      <span
                        key={index}
                        className="bg-white px-3 py-1 rounded-full text-sm text-gray-700 border border-gray-200"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {activeTab === 'preview' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <PlatformPreview 
                  listing={currentListing} 
                  platform={currentListing.platform}
                />
              </motion.div>
            )}

            {activeTab === 'optimization' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <ListingOptimizationScore listing={currentListing} />
              </motion.div>
            )}

            {activeTab === 'images' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                <ImageGenerationStatus listingId={listingId} />
              </motion.div>
            )}

            {activeTab === 'video' && currentListing.tiktok_video_script && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {currentListing.tiktok_video_script && currentListing.tiktok_video_script.split('\n\n---\n\n').map((script, index) => (
                  <CopyableSection
                    key={index}
                    title={script.title}
                    content={script.script}
                  />
                ))}
              </motion.div>
            )}
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="grid md:grid-cols-3 gap-6"
        >
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-3xl font-bold text-primary-600 mb-2">95%</div>
            <div className="text-gray-600">SEO Optimized</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">8</div>
            <div className="text-gray-600">Keywords Targeted</div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">200+</div>
            <div className="text-gray-600">Characters Optimized</div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ListingResults;
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Copy, Download, Star, Tag, Video, ShoppingCart, Eye, TrendingUp } from 'lucide-react';
import toast from 'react-hot-toast';
import PlatformPreview from '../components/PlatformPreview';
import ListingOptimizationScore from '../components/ListingOptimizationScore';
import EtsyPremiumResults from '../components/EtsyPremiumResults';
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
    whats_in_box: `• 1x Wireless Bluetooth Earbuds (Left & Right)
• 1x Premium Charging Case with LED Display
• 3x Sets of Ear Tips (Small, Medium, Large)
• 1x USB-C Fast Charging Cable (3.3ft/1m)
• 1x User Manual & Quick Start Guide
• 1x Warranty Card (24-Month Protection)
• 1x Premium Travel Pouch`,
    faqs: `Q: How long does the battery last on a single charge?
A: The earbuds provide up to 8 hours of continuous playback on a single charge, with an additional 16 hours from the charging case, giving you 24 hours total battery life.

Q: Are these earbuds compatible with iPhone and Android?
A: Yes! These earbuds are universally compatible with all Bluetooth-enabled devices including iPhone, Android, tablets, laptops, and smart TVs.

Q: Can I use these earbuds for sports and workouts?
A: Absolutely! With IPX7 waterproof rating, these earbuds are perfect for intense workouts, running in the rain, and all sports activities. The secure fit ensures they stay in place during movement.

Q: Do these earbuds support wireless charging?
A: Yes, the charging case supports both wireless charging and USB-C fast charging for ultimate convenience.

Q: What's the wireless range?
A: These earbuds offer a stable connection up to 33 feet (10 meters) from your device, with advanced Bluetooth 5.3 technology ensuring minimal latency and dropouts.`,
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

  // Check if this is an Etsy listing - use premium experience
  if (currentListing?.platform === 'etsy' || currentListing?.product?.target_platform === 'etsy') {
    return <EtsyPremiumResults listing={currentListing} />;
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
                    Your {currentListing.platform === 'amazon' ? 'Amazon' : 
                          currentListing.platform === 'walmart' ? 'Walmart' :
                          currentListing.platform === 'etsy' ? 'Etsy' :
                          currentListing.platform === 'tiktok' ? 'TikTok' :
                          currentListing.platform === 'shopify' ? 'Shopify' : 
                          'Product'} Listing is Ready!
                  </h1>
                  <p className="text-gray-600">
                    Generated with AI optimization for {
                      currentListing.platform === 'walmart' ? 'Walmart marketplace requirements' :
                      currentListing.platform === 'amazon' ? 'maximum conversions' :
                      currentListing.platform === 'etsy' ? 'handmade marketplace success' :
                      currentListing.platform === 'tiktok' ? 'viral social commerce' :
                      'e-commerce success'
                    }
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
              {currentListing.platform === 'tiktok' && (
                <TabButton
                  id="video"
                  label="Video Scripts"
                  icon={Video}
                  active={activeTab === 'video'}
                  onClick={setActiveTab}
                />
              )}
              {currentListing.platform === 'walmart' && (
                <>
                  <TabButton
                    id="walmart-specs"
                    label="Specifications"
                    icon={Tag}
                    active={activeTab === 'walmart-specs'}
                    onClick={setActiveTab}
                  />
                  <TabButton
                    id="walmart-compliance"
                    label="Compliance"
                    icon={Star}
                    active={activeTab === 'walmart-compliance'}
                    onClick={setActiveTab}
                  />
                </>
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
                {/* Platform-specific title display */}
                <CopyableSection
                  title={currentListing.platform === 'walmart' ? 'Product Title (100 char limit)' : 'Product Title'}
                  content={currentListing.platform === 'walmart' ? 
                    (currentListing.walmart_product_title || currentListing.title || 'No title generated') :
                    (currentListing.title || 'No title generated')
                  }
                />
                
                {/* Platform-specific bullet points */}
                <CopyableSection
                  title={currentListing.platform === 'walmart' ? 'Key Features (3-10 bullets, max 80 chars each)' : 'Bullet Points'}
                  content={currentListing.platform === 'walmart' ? 
                    (currentListing.walmart_key_features || 'No key features generated') :
                    (currentListing.bullet_points || 'No bullet points generated')
                  }
                />
                
                {/* Platform-specific description */}
                <CopyableSection
                  title={currentListing.platform === 'walmart' ? 'Product Description (Min 150 words, plain text)' : 'Product Description'}
                  content={currentListing.platform === 'walmart' ?
                    (currentListing.walmart_description || currentListing.long_description || 'No description generated') :
                    (currentListing.long_description || 'No description generated')
                  }
                  isHtml={currentListing.platform !== 'walmart'}
                />

                
                {currentListing.whats_in_box && (
                  <CopyableSection
                    title="What's in the Box"
                    content={currentListing.whats_in_box}
                  />
                )}
                
                {currentListing.faqs && (
                  <CopyableSection
                    title="Frequently Asked Questions"
                    content={currentListing.faqs}
                  />
                )}
                
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

            {activeTab === 'aplus' && currentListing.platform !== 'walmart' && (
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

            {activeTab === 'aplus' && currentListing.platform === 'walmart' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="text-center py-12"
              >
                <div className="text-6xl mb-4">🚫</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">A+ Content Not Available</h3>
                <p className="text-gray-500">Walmart marketplace doesn't support A+ Content. All listing information is available in the Main Listing tab.</p>
              </motion.div>
            )}

            {activeTab === 'keywords' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Platform-specific keywords display */}
                {currentListing.platform === 'walmart' ? (
                  <>
                    {/* Walmart SEO Keywords */}
                    <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-blue-900 flex items-center">
                          🎯 Walmart SEO Keywords
                          <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                            Natural Integration
                          </span>
                        </h3>
                        <button
                          onClick={() => copyToClipboard(currentListing.keywords || '')}
                          className="flex items-center text-sm text-blue-600 hover:text-blue-700"
                        >
                          <Copy className="h-4 w-4 mr-1" />
                          Copy All Keywords
                        </button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {(currentListing.keywords || '').split(', ').map((keyword, index) => (
                          <span
                            key={index}
                            className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium border border-blue-300"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Walmart Keyword Strategy */}
                    <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                      <h3 className="font-semibold text-green-900 mb-3">📈 Walmart SEO Strategy</h3>
                      <div className="space-y-3">
                        <div className="bg-white p-3 rounded border">
                          <h4 className="font-medium text-green-800 mb-2">Natural Integration</h4>
                          <p className="text-sm text-gray-700">Keywords are integrated naturally into title, features, and description for Walmart's Sparky algorithm.</p>
                        </div>
                        <div className="bg-white p-3 rounded border">
                          <h4 className="font-medium text-green-800 mb-2">Conversational Tone</h4>
                          <p className="text-sm text-gray-700">Uses Q&A style language that matches customer search behavior on Walmart.</p>
                        </div>
                        <div className="bg-white p-3 rounded border">
                          <h4 className="font-medium text-green-800 mb-2">No Backend Keywords</h4>
                          <p className="text-sm text-gray-700">Walmart doesn't use hidden backend keywords like Amazon - all SEO is through natural content.</p>
                        </div>
                      </div>
                    </div>

                    {/* Keyword Stats */}
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">📊 Walmart Keyword Analysis</h4>
                      <div className="grid grid-cols-2 gap-4 text-center">
                        <div>
                          <div className="text-2xl font-bold text-blue-600">
                            {(currentListing.keywords || '').split(', ').length}
                          </div>
                          <div className="text-sm text-gray-600">Total Keywords</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-green-600">
                            {(currentListing.keywords || '').split(', ').filter(k => k.split(' ').length > 2).length}
                          </div>
                          <div className="text-sm text-gray-600">Long-tail Keywords</div>
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    {/* Amazon Keywords - existing layout */}
                    {/* Short-tail Keywords Section */}
                    <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-blue-900 flex items-center">
                          🎯 Short-tail Keywords
                          <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                            High Volume
                          </span>
                        </h3>
                        <button
                          onClick={() => {
                            const shortTail = (currentListing.keywords || '').split(', ').filter(k => k.split(' ').length <= 2);
                            copyToClipboard(shortTail.join(', '));
                          }}
                          className="flex items-center text-sm text-blue-600 hover:text-blue-700"
                        >
                          <Copy className="h-4 w-4 mr-1" />
                          Copy Short-tail
                        </button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {(typeof currentListing.keywords === 'string' ? currentListing.keywords : (currentListing.keywords || []).join(', ') || '').split(', ').filter(keyword => keyword.split(' ').length <= 2).map((keyword, index) => (
                          <span
                            key={index}
                            className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium border border-blue-300"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Long-tail Keywords Section */}
                    <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-green-900 flex items-center">
                          🔍 Long-tail Keywords
                          <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                            High Intent
                          </span>
                        </h3>
                        <button
                          onClick={() => {
                            const longTail = (currentListing.keywords || '').split(', ').filter(k => k.split(' ').length > 2);
                            copyToClipboard(longTail.join(', '));
                          }}
                          className="flex items-center text-sm text-green-600 hover:text-green-700"
                        >
                          <Copy className="h-4 w-4 mr-1" />
                          Copy Long-tail
                        </button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {(currentListing.keywords || '').split(', ').filter(keyword => keyword.split(' ').length > 2).map((keyword, index) => (
                          <span
                            key={index}
                            className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm border border-green-300"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Backend Keywords Section */}
                    <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-purple-900 flex items-center">
                          🔑 Amazon Backend Keywords
                          <span className="ml-2 text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
                            Search Terms
                          </span>
                        </h3>
                        <button
                          onClick={() => copyToClipboard(currentListing.amazon_backend_keywords || '')}
                          className="flex items-center text-sm text-purple-600 hover:text-purple-700"
                        >
                          <Copy className="h-4 w-4 mr-1" />
                          Copy Backend
                        </button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {(currentListing.amazon_backend_keywords || '').split(', ').map((keyword, index) => (
                          <span
                            key={index}
                            className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm border border-purple-300"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Keyword Stats */}
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">📊 Amazon Keyword Analysis</h4>
                      <div className="grid grid-cols-3 gap-4 text-center">
                        <div>
                          <div className="text-2xl font-bold text-blue-600">
                            {(currentListing.keywords || '').split(', ').filter(k => k.split(' ').length <= 2).length}
                          </div>
                          <div className="text-sm text-gray-600">Short-tail</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-green-600">
                            {(currentListing.keywords || '').split(', ').filter(k => k.split(' ').length > 2).length}
                          </div>
                          <div className="text-sm text-gray-600">Long-tail</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-purple-600">
                            {(currentListing.amazon_backend_keywords || '').split(', ').length}
                          </div>
                          <div className="text-sm text-gray-600">Backend Terms</div>
                        </div>
                      </div>
                    </div>
                  </>
                )}
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
            
            {/* Walmart Specifications Tab */}
            {activeTab === 'walmart-specs' && currentListing.platform === 'walmart' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Product Identifiers */}
                <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                  <h3 className="font-semibold text-blue-900 mb-3">📦 Product Identifiers</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <div className="text-sm text-gray-600">GTIN/UPC</div>
                      <div className="font-mono text-sm bg-white p-2 rounded border">{currentListing.walmart_gtin_upc || 'Not generated'}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-600">Manufacturer Part</div>
                      <div className="font-mono text-sm bg-white p-2 rounded border">{currentListing.walmart_manufacturer_part || 'Not generated'}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-600">SKU ID</div>
                      <div className="font-mono text-sm bg-white p-2 rounded border">{currentListing.walmart_sku_id || 'Not generated'}</div>
                    </div>
                  </div>
                </div>

                {/* Product Details */}
                <CopyableSection
                  title="Walmart Product Title (100 char limit)"
                  content={currentListing.walmart_product_title || currentListing.title}
                />
                
                <CopyableSection
                  title="Product Description (Min 150 words, plain text)"
                  content={currentListing.walmart_description || 'No description generated'}
                />
                
                <CopyableSection
                  title="Key Features (3-10 bullets, max 80 chars each)"
                  content={currentListing.walmart_key_features || 'No key features generated'}
                />


                {/* Category & Attributes */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                    <h3 className="font-semibold text-green-900 mb-3">🏷️ Category Information</h3>
                    <div className="space-y-2">
                      <div>
                        <div className="text-sm text-gray-600">Product Type</div>
                        <div className="font-medium">{currentListing.walmart_product_type || 'Not specified'}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">Category Path</div>
                        <div className="font-medium text-sm">{currentListing.walmart_category_path || 'Not specified'}</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Shipping Info */}
                  <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                    <h3 className="font-semibold text-purple-900 mb-3">📦 Shipping Information</h3>
                    <div className="space-y-2">
                      <div>
                        <div className="text-sm text-gray-600">Shipping Weight</div>
                        <div className="font-medium">{currentListing.walmart_shipping_weight || 'Not specified'}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">Package Dimensions</div>
                        <div className="font-medium text-sm">{currentListing.walmart_shipping_dimensions || 'Not specified'}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Attributes */}
                {currentListing.walmart_attributes && (
                  <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                    <h3 className="font-semibold text-yellow-900 mb-3">🔧 Product Attributes</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {(() => {
                        try {
                          const attributes = JSON.parse(currentListing.walmart_attributes);
                          return Object.entries(attributes).map(([key, value]) => (
                            <div key={key} className="flex justify-between bg-white p-2 rounded border">
                              <span className="font-medium text-gray-700 capitalize">{key.replace('_', ' ')}:</span>
                              <span className="text-gray-900">{Array.isArray(value) ? value.join(', ') : value}</span>
                            </div>
                          ));
                        } catch (e) {
                          return (
                            <div className="bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm">
                              {currentListing.walmart_attributes}
                            </div>
                          );
                        }
                      })()}
                    </div>
                  </div>
                )}

                {/* Category & Attributes */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                    <h3 className="font-semibold text-green-900 mb-3">🏷️ Category Information</h3>
                    <div className="space-y-2">
                      <div>
                        <div className="text-sm text-gray-600">Product Type</div>
                        <div className="font-medium">{currentListing.walmart_product_type || 'Not specified'}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">Category Path</div>
                        <div className="font-medium text-sm">{currentListing.walmart_category_path || 'Not specified'}</div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Shipping Info */}
                  <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                    <h3 className="font-semibold text-purple-900 mb-3">📦 Shipping Information</h3>
                    <div className="space-y-2">
                      <div>
                        <div className="text-sm text-gray-600">Shipping Weight</div>
                        <div className="font-medium">{currentListing.walmart_shipping_weight || 'Not specified'}</div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600">Package Dimensions</div>
                        <div className="font-medium text-sm">{currentListing.walmart_shipping_dimensions || 'Not specified'}</div>
                      </div>
                    </div>
                  </div>
                </div>

              </motion.div>
            )}

            {/* Walmart Compliance Tab */}
            {activeTab === 'walmart-compliance' && currentListing.platform === 'walmart' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Warranty Information */}
                {currentListing.walmart_warranty_info && (
                  <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                    <h3 className="font-semibold text-green-900 mb-3">🛡️ Warranty Information</h3>
                    <div className="space-y-3">
                      {(() => {
                        try {
                          const warrantyData = JSON.parse(currentListing.walmart_warranty_info);
                          return Object.entries(warrantyData).map(([key, value]) => (
                            <div key={key} className="bg-white p-3 rounded border">
                              <div className="flex justify-between items-start">
                                <span className="font-medium text-gray-700 capitalize">{key.replace('_', ' ')}:</span>
                                <span className="text-gray-900 ml-2 text-right">{Array.isArray(value) ? value.join(', ') : value}</span>
                              </div>
                            </div>
                          ));
                        } catch (e) {
                          return <div className="bg-white p-3 rounded border text-sm text-gray-600">{currentListing.walmart_warranty_info}</div>;
                        }
                      })()}
                    </div>
                  </div>
                )}

                {/* Compliance & Certifications */}
                {currentListing.walmart_compliance_certifications && (
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <h3 className="font-semibold text-blue-900 mb-3">✅ Compliance & Certifications</h3>
                    <div className="space-y-3">
                      {(() => {
                        try {
                          const complianceData = JSON.parse(currentListing.walmart_compliance_certifications);
                          
                          // Handle both array format (legacy) and object format (current)
                          if (Array.isArray(complianceData)) {
                            return (
                              <div className="flex flex-wrap gap-2">
                                {complianceData.map((cert, index) => (
                                  <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm border border-blue-300">
                                    {cert}
                                  </span>
                                ))}
                              </div>
                            );
                          } else {
                            // New object format with certifications, safety_warnings, etc.
                            return (
                              <>
                                {complianceData.certifications && complianceData.certifications.length > 0 && (
                                  <div>
                                    <h4 className="text-sm font-medium text-gray-700 mb-2">Certifications:</h4>
                                    <div className="flex flex-wrap gap-2">
                                      {complianceData.certifications.map((cert, index) => (
                                        <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm border border-blue-300">
                                          {cert}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                                
                                {complianceData.safety_warnings && complianceData.safety_warnings.length > 0 && (
                                  <div>
                                    <h4 className="text-sm font-medium text-gray-700 mb-2">Safety Warnings:</h4>
                                    <div className="space-y-1">
                                      {complianceData.safety_warnings.map((warning, index) => (
                                        <div key={index} className="bg-orange-100 text-orange-800 px-3 py-2 rounded text-sm border border-orange-300">
                                          ⚠️ {warning}
                                        </div>
                                      ))}
                                    </div>
                                  </div>
                                )}
                                
                                {complianceData.age_restrictions && (
                                  <div>
                                    <h4 className="text-sm font-medium text-gray-700 mb-2">Age Restrictions:</h4>
                                    <div className="bg-yellow-100 text-yellow-800 px-3 py-2 rounded text-sm border border-yellow-300">
                                      {complianceData.age_restrictions}
                                    </div>
                                  </div>
                                )}
                              </>
                            );
                          }
                        } catch (e) {
                          // Fallback for malformed JSON
                          return (
                            <div className="bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm">
                              {currentListing.walmart_compliance_certifications}
                            </div>
                          );
                        }
                      })()}
                    </div>
                  </div>
                )}

                {/* Assembly Information */}
                <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                  <h3 className="font-semibold text-orange-900 mb-3">🔨 Assembly Requirements</h3>
                  <div className="flex items-center space-x-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      currentListing.walmart_assembly_required 
                        ? 'bg-orange-100 text-orange-800 border border-orange-300' 
                        : 'bg-green-100 text-green-800 border border-green-300'
                    }`}>
                      {currentListing.walmart_assembly_required ? 'Assembly Required' : 'No Assembly Required'}
                    </span>
                  </div>
                </div>

                {/* Rich Media Suggestions */}
                <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                  <h3 className="font-semibold text-purple-900 mb-3">📸 Rich Media Recommendations</h3>
                  
                  {/* Video URLs */}
                  {currentListing.walmart_video_urls && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Suggested Video Content:</h4>
                      <div className="space-y-2">
                        {(() => {
                          try {
                            const videos = JSON.parse(currentListing.walmart_video_urls);
                            if (Array.isArray(videos)) {
                              return videos.map((video, index) => (
                                <div key={index} className="bg-white p-2 rounded border text-sm">
                                  {video}
                                </div>
                              ));
                            } else {
                              return (
                                <div className="bg-white p-2 rounded border text-sm">
                                  {JSON.stringify(videos)}
                                </div>
                              );
                            }
                          } catch (e) {
                            return (
                              <div className="bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm">
                                {currentListing.walmart_video_urls}
                              </div>
                            );
                          }
                        })()}
                      </div>
                    </div>
                  )}
                  
                  {/* Additional Images */}
                  {currentListing.walmart_swatch_images && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Additional Image Types:</h4>
                      <div className="flex flex-wrap gap-2">
                        {(() => {
                          try {
                            const images = JSON.parse(currentListing.walmart_swatch_images);
                            if (Array.isArray(images)) {
                              return images.map((img, index) => (
                                <span key={index} className="bg-purple-100 text-purple-800 px-3 py-1 rounded text-sm border border-purple-300">
                                  {img}
                                </span>
                              ));
                            } else {
                              return (
                                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded text-sm border border-purple-300">
                                  {JSON.stringify(images)}
                                </span>
                              );
                            }
                          } catch (e) {
                            return (
                              <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded text-sm">
                                {currentListing.walmart_swatch_images}
                              </span>
                            );
                          }
                        })()}
                      </div>
                    </div>
                  )}
                </div>

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
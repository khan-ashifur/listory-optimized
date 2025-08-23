import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Copy, Download, Star, Tag, Video, ShoppingCart, Eye, TrendingUp } from 'lucide-react';
import toast from 'react-hot-toast';
import PlatformPreview from '../components/PlatformPreview';
import ListingOptimizationScore from '../components/ListingOptimizationScore';
import EtsyPremiumResults from '../components/EtsyPremiumResults';
import { listingAPI } from '../services/api';

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
        console.log('=== FETCHING LISTING DATA ===');
        console.log('Listing ID:', listingId);
        const response = await listingAPI.get(listingId);
        console.log('API Response:', response.data);
        console.log('Platform:', response.data.platform);
        console.log('walmart_compliance_certifications:', response.data.walmart_compliance_certifications);
        console.log('walmart_profit_maximizer:', response.data.walmart_profit_maximizer);
        console.log('=== END FETCH DEBUG ===');
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

  const CopyableSection = ({ title, content, isHtml = false, isBulletPoints = false }) => (
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
        ) : isBulletPoints && content ? (
          // Special formatting for bullet points with labels
          <div className="space-y-2">
            {content.split('\n').filter(point => point.trim()).map((point, index) => {
              const trimmedPoint = point.replace(/^[•\-*]\s*/, '').trim();
              const parts = trimmedPoint.split(' - ');
              const label = parts[0];
              const bulletContent = parts.slice(1).join(' - ');
              
              return (
                <div key={index} className="flex items-start">
                  <span className="mr-2 text-blue-600">•</span>
                  <div>
                    {label && bulletContent ? (
                      <>
                        <span className="font-semibold text-blue-700">{label}</span>
                        <span className="text-gray-700"> - {bulletContent}</span>
                      </>
                    ) : (
                      <span className="text-gray-700">{trimmedPoint}</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
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
              {currentListing.platform !== 'walmart' && (
                <TabButton
                  id="aplus"
                  label="A+ Content"
                  icon={Star}
                  active={activeTab === 'aplus'}
                  onClick={setActiveTab}
                />
              )}
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
                  <TabButton
                    id="walmart-profit"
                    label="💰 Profit Maximizer"
                    icon={TrendingUp}
                    active={activeTab === 'walmart-profit'}
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
                
                {/* Show optimized Key Features for Walmart, Bullet Points for other platforms */}
                {currentListing.platform === 'walmart' ? (
                  <CopyableSection
                    title="Key Features (3-10 bullets, max 80 chars each)"
                    content={currentListing.walmart_key_features || 'No key features generated'}
                    isBulletPoints={true}
                  />
                ) : (
                  /* Other platforms use Bullet Points */
                  <CopyableSection
                    title="Bullet Points"
                    content={currentListing.bullet_points || 'No bullet points generated'}
                    isBulletPoints={true}
                  />
                )}
                
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

                {/* Technical Specifications */}
                {currentListing.walmart_specifications && (
                  <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h3 className="font-semibold text-gray-900 mb-3">⚙️ Technical Specifications</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {(() => {
                        try {
                          const specs = JSON.parse(currentListing.walmart_specifications);
                          return Object.entries(specs).map(([key, value], index) => (
                            <div key={index} className="bg-white p-3 rounded border">
                              <div className="text-sm text-gray-600 font-medium capitalize">
                                {key.replace(/_/g, ' ')}
                              </div>
                              <div className="text-gray-900 font-medium">{value}</div>
                            </div>
                          ));
                        } catch {
                          return (
                            <div className="col-span-2 text-gray-500">
                              Technical specifications will be generated after product optimization
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
                            // New object format with required_certifications, certification_guidance, etc.
                            return (
                              <div className="space-y-4">
                                {complianceData.required_certifications && complianceData.required_certifications.length > 0 && (
                                  <div className="bg-white p-4 rounded border">
                                    <h4 className="text-sm font-medium text-blue-700 mb-2">Required Certifications:</h4>
                                    <div className="flex flex-wrap gap-2">
                                      {complianceData.required_certifications.map((cert, index) => (
                                        <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm border border-blue-300">
                                          {cert}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                                
                                {complianceData.certification_guidance && (
                                  <div className="bg-white p-4 rounded border">
                                    <h4 className="text-sm font-medium text-green-700 mb-2">Certification Guidance:</h4>
                                    <div className="text-green-900 text-sm">
                                      {complianceData.certification_guidance}
                                    </div>
                                  </div>
                                )}
                                
                                {complianceData.regulatory_requirements && (
                                  <div className="bg-white p-4 rounded border">
                                    <h4 className="text-sm font-medium text-purple-700 mb-2">Regulatory Requirements:</h4>
                                    <div className="text-purple-900 text-sm">
                                      {complianceData.regulatory_requirements}
                                    </div>
                                  </div>
                                )}
                                
                                {complianceData.labeling_requirements && (
                                  <div className="bg-white p-4 rounded border">
                                    <h4 className="text-sm font-medium text-orange-700 mb-2">Labeling Requirements:</h4>
                                    <div className="text-orange-900 text-sm">
                                      {complianceData.labeling_requirements}
                                    </div>
                                  </div>
                                )}
                                
                                {complianceData.walmart_specific_compliance && (
                                  <div className="bg-blue-50 p-4 rounded border border-blue-200">
                                    <h4 className="text-sm font-medium text-blue-700 mb-2">Walmart-Specific Compliance:</h4>
                                    <div className="text-blue-900 text-sm">
                                      {complianceData.walmart_specific_compliance}
                                    </div>
                                  </div>
                                )}
                              </div>
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

                  {/* New Rich Media Content */}
                  {currentListing.walmart_rich_media && (
                    <div className="mb-4">
                      {(() => {
                        try {
                          const richMedia = JSON.parse(currentListing.walmart_rich_media);
                          return (
                            <div className="space-y-4">
                              {/* Main Images */}
                              {richMedia.main_images && richMedia.main_images.length > 0 && (
                                <div className="bg-white p-4 rounded border">
                                  <h4 className="text-sm font-medium text-purple-700 mb-2">📸 Main Image Recommendations:</h4>
                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                    {richMedia.main_images.map((image, index) => (
                                      <div key={index} className="bg-purple-50 p-2 rounded border text-sm text-purple-800">
                                        {image}
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* Video Content */}
                              {richMedia.video_content && richMedia.video_content.length > 0 && (
                                <div className="bg-white p-4 rounded border">
                                  <h4 className="text-sm font-medium text-red-700 mb-2">🎥 Video Content Recommendations:</h4>
                                  <div className="space-y-2">
                                    {richMedia.video_content.map((video, index) => (
                                      <div key={index} className="bg-red-50 p-2 rounded border text-sm text-red-800">
                                        {video}
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* Infographics */}
                              {richMedia.infographics && richMedia.infographics.length > 0 && (
                                <div className="bg-white p-4 rounded border">
                                  <h4 className="text-sm font-medium text-green-700 mb-2">📊 Infographic Recommendations:</h4>
                                  <div className="space-y-2">
                                    {richMedia.infographics.map((infographic, index) => (
                                      <div key={index} className="bg-green-50 p-2 rounded border text-sm text-green-800">
                                        {infographic}
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* 360 View */}
                              {richMedia["360_view"] && (
                                <div className="bg-white p-4 rounded border">
                                  <h4 className="text-sm font-medium text-blue-700 mb-2">🔄 360° View Recommendation:</h4>
                                  <div className="bg-blue-50 p-2 rounded border text-sm text-blue-800">
                                    {richMedia["360_view"]}
                                  </div>
                                </div>
                              )}
                            </div>
                          );
                        } catch (e) {
                          return (
                            <div className="bg-gray-100 text-gray-700 px-3 py-2 rounded text-sm">
                              Error displaying rich media content
                            </div>
                          );
                        }
                      })()}
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

            {/* Walmart Marketplace Intelligence Tab */}
            {activeTab === 'walmart-profit' && currentListing.platform === 'walmart' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
                  <h2 className="text-xl font-bold text-blue-900 mb-4 flex items-center">
                    📊 Marketplace Intelligence Report
                    <span className="ml-3 text-xs bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-normal">
                      Data-Driven Strategy
                    </span>
                  </h2>
                  <p className="text-blue-800 text-sm">
                    Actionable growth strategies based on marketplace data and category benchmarks.
                  </p>
                </div>

                {currentListing.walmart_profit_maximizer && (() => {
                  try {
                    const intelligence = JSON.parse(currentListing.walmart_profit_maximizer);
                    return (
                      <div className="space-y-6">
                        {/* Q1 Action Plan */}
                        {intelligence.q1_action_plan && (
                          <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                            <h3 className="font-semibold text-green-900 mb-3 flex items-center">
                              🚀 Q1: Launch Strategy (Month 1-3)
                              <span className="ml-2 text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                                Action Items
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border">
                              <div className="space-y-2">
                                {intelligence.q1_action_plan.map((item, index) => (
                                  <div key={index} className="flex items-start text-sm text-green-900">
                                    <div className="font-mono mr-2">•</div>
                                    <div>{item}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Q2 Growth Tactics */}
                        {intelligence.q2_growth_tactics && (
                          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                            <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
                              📈 Q2: Growth Phase (Month 4-6)
                              <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                Scaling
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border">
                              <div className="space-y-2">
                                {intelligence.q2_growth_tactics.map((item, index) => (
                                  <div key={index} className="flex items-start text-sm text-blue-900">
                                    <div className="font-mono mr-2">•</div>
                                    <div>{item}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Q3 Optimization */}
                        {intelligence.q3_optimization && (
                          <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
                            <h3 className="font-semibold text-purple-900 mb-3 flex items-center">
                              ⚡ Q3: Peak Season (Month 7-9)
                              <span className="ml-2 text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
                                Optimize
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border">
                              <div className="space-y-2">
                                {intelligence.q3_optimization.map((item, index) => (
                                  <div key={index} className="flex items-start text-sm text-purple-900">
                                    <div className="font-mono mr-2">•</div>
                                    <div>{item}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Q4 Maximization */}
                        {intelligence.q4_maximization && (
                          <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
                            <h3 className="font-semibold text-orange-900 mb-3 flex items-center">
                              🎯 Q4: Holiday Rush (Month 10-12)
                              <span className="ml-2 text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded-full">
                                Maximize
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border">
                              <div className="space-y-2">
                                {intelligence.q4_maximization.map((item, index) => (
                                  <div key={index} className="flex items-start text-sm text-orange-900">
                                    <div className="font-mono mr-2">•</div>
                                    <div>{item}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Competitor Landscape */}
                        {intelligence.competitor_landscape && (
                          <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                            <h3 className="font-semibold text-red-900 mb-3 flex items-center">
                              🎯 Competitive Analysis
                              <span className="ml-2 text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">
                                Intelligence
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border text-sm">
                              <div className="space-y-3">
                                <div>
                                  <span className="font-medium text-red-700">Market Position: </span>
                                  <span className="text-red-900">{intelligence.competitor_landscape.market_position}</span>
                                </div>
                                <div>
                                  <span className="font-medium text-red-700">Price Strategy: </span>
                                  <span className="text-red-900">{intelligence.competitor_landscape.price_positioning}</span>
                                </div>
                                {intelligence.competitor_landscape.top_3_competitors && (
                                  <div>
                                    <span className="font-medium text-red-700">Monitor These Competitors:</span>
                                    <ul className="mt-1 space-y-1">
                                      {intelligence.competitor_landscape.top_3_competitors.map((comp, index) => (
                                        <li key={index} className="text-red-900 ml-4">• {comp}</li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Revenue Projections */}
                        {intelligence.revenue_projections && (
                          <div className="bg-indigo-50 rounded-lg p-4 border border-indigo-200">
                            <h3 className="font-semibold text-indigo-900 mb-3 flex items-center">
                              💰 Revenue Projections
                              <span className="ml-2 text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full">
                                Forecast
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border">
                              <div className="grid grid-cols-3 gap-4 text-sm">
                                {intelligence.revenue_projections.conservative && (
                                  <div className="text-center">
                                    <div className="font-medium text-gray-700 mb-2">Conservative</div>
                                    <div className="space-y-1 text-gray-600">
                                      <div>M1: {intelligence.revenue_projections.conservative.month_1}</div>
                                      <div>M3: {intelligence.revenue_projections.conservative.month_3}</div>
                                      <div>M6: {intelligence.revenue_projections.conservative.month_6}</div>
                                      <div className="font-semibold text-indigo-900">Y1: {intelligence.revenue_projections.conservative.month_12}</div>
                                    </div>
                                  </div>
                                )}
                                {intelligence.revenue_projections.realistic && (
                                  <div className="text-center bg-indigo-50 p-2 rounded">
                                    <div className="font-medium text-indigo-700 mb-2">Realistic</div>
                                    <div className="space-y-1 text-indigo-600">
                                      <div>M1: {intelligence.revenue_projections.realistic.month_1}</div>
                                      <div>M3: {intelligence.revenue_projections.realistic.month_3}</div>
                                      <div>M6: {intelligence.revenue_projections.realistic.month_6}</div>
                                      <div className="font-semibold text-indigo-900">Y1: {intelligence.revenue_projections.realistic.month_12}</div>
                                    </div>
                                  </div>
                                )}
                                {intelligence.revenue_projections.aggressive && (
                                  <div className="text-center">
                                    <div className="font-medium text-gray-700 mb-2">Aggressive</div>
                                    <div className="space-y-1 text-gray-600">
                                      <div>M1: {intelligence.revenue_projections.aggressive.month_1}</div>
                                      <div>M3: {intelligence.revenue_projections.aggressive.month_3}</div>
                                      <div>M6: {intelligence.revenue_projections.aggressive.month_6}</div>
                                      <div className="font-semibold text-indigo-900">Y1: {intelligence.revenue_projections.aggressive.month_12}</div>
                                    </div>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Key Metrics */}
                        {intelligence.key_metrics_to_track && (
                          <div className="bg-teal-50 rounded-lg p-4 border border-teal-200">
                            <h3 className="font-semibold text-teal-900 mb-3 flex items-center">
                              📊 Key Metrics to Track
                              <span className="ml-2 text-xs bg-teal-100 text-teal-800 px-2 py-1 rounded-full">
                                KPIs
                              </span>
                            </h3>
                            <div className="bg-white p-4 rounded border">
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {intelligence.key_metrics_to_track.map((metric, index) => (
                                  <div key={index} className="flex items-center text-sm">
                                    <div className="w-2 h-2 bg-teal-500 rounded-full mr-2"></div>
                                    <span className="text-teal-900">{metric}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Value Summary */}
                        <div className="bg-gradient-to-r from-green-100 to-blue-100 rounded-lg p-6 border-2 border-green-300">
                          <h3 className="font-bold text-green-900 mb-3 text-lg">🏆 Business Intelligence Summary</h3>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                            <div className="bg-white p-4 rounded-lg shadow-sm">
                              <div className="text-2xl font-bold text-green-600">$10,000+</div>
                              <div className="text-sm text-gray-600">Consultant Value</div>
                            </div>
                            <div className="bg-white p-4 rounded-lg shadow-sm">
                              <div className="text-2xl font-bold text-blue-600">7</div>
                              <div className="text-sm text-gray-600">Strategic Areas</div>
                            </div>
                            <div className="bg-white p-4 rounded-lg shadow-sm">
                              <div className="text-2xl font-bold text-purple-600">12</div>
                              <div className="text-sm text-gray-600">Month Roadmap</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  } catch (error) {
                    return (
                      <div className="bg-gray-100 p-4 rounded border text-gray-700">
                        Advanced profit strategies are being generated. Please refresh in a few moments.
                      </div>
                    );
                  }
                })()}
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
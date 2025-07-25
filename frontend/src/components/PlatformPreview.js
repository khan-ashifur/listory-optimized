import React from 'react';
import { Star, ShoppingCart, Heart, Share2, Eye } from 'lucide-react';

const PlatformPreview = ({ listing, platform }) => {
  if (!listing) return null;

  const renderAmazonPreview = () => (
    <div className="bg-white border rounded-lg p-4 max-w-4xl mx-auto">
      {/* Amazon Header */}
      <div className="border-b pb-3 mb-4">
        <div className="text-xs text-gray-500">amazon.com</div>
        <div className="flex items-center space-x-2 mt-1">
          <span className="bg-orange-500 text-white px-2 py-1 text-xs font-bold">amazon's choice</span>
          <span className="text-xs text-gray-600">in {listing.product?.categories || 'Electronics'}</span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Product Image Area */}
        <div className="space-y-4">
          <div className="bg-gray-50 aspect-square rounded-lg flex items-center justify-center">
            <div className="text-center text-gray-400">
              <div className="text-4xl mb-2">📦</div>
              <div className="text-sm">Product Image</div>
            </div>
          </div>
          <div className="flex space-x-2">
            {[1,2,3,4].map(i => (
              <div key={i} className="w-12 h-12 bg-gray-100 rounded border"></div>
            ))}
          </div>
        </div>

        {/* Product Details */}
        <div className="space-y-4">
          <h1 className="text-xl font-normal leading-tight text-gray-900">
            {listing.title}
          </h1>
          
          <div className="flex items-center space-x-2">
            <div className="flex items-center">
              {[1,2,3,4,5].map(i => (
                <Star key={i} className="w-4 h-4 text-orange-400 fill-current" />
              ))}
            </div>
            <span className="text-blue-600 text-sm">4.5</span>
            <span className="text-blue-600 text-sm">2,847 ratings</span>
          </div>

          <div className="border-t border-b py-3">
            <div className="text-sm text-gray-600">Price:</div>
            <div className="flex items-baseline space-x-2">
              <span className="text-2xl text-red-700">${listing.product?.price || '29.99'}</span>
              <span className="text-sm text-gray-500 line-through">$39.99</span>
              <span className="text-sm text-green-700">(25% off)</span>
            </div>
            <div className="text-xs text-gray-500 mt-1">FREE Returns</div>
          </div>

          <div className="space-y-2">
            <div className="font-medium text-sm">About this item</div>
            <div className="text-sm space-y-1">
              {listing.bullet_points?.split('\n').slice(0, 5).map((point, i) => (
                <div key={i} className="flex items-start">
                  <span className="mr-2">•</span>
                  <span>{point.replace(/^[•\-\*]\s*/, '').replace(/^🎯|🔥|✅|🚀|💝/, '').trim()}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <button className="w-full bg-orange-400 hover:bg-orange-500 text-white py-2 px-4 rounded-full text-sm font-medium">
              Add to Cart
            </button>
            <button className="w-full bg-yellow-400 hover:bg-yellow-500 text-black py-2 px-4 rounded-full text-sm font-medium">
              Buy Now
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const renderWalmartPreview = () => (
    <div className="bg-white border rounded-lg p-4 max-w-4xl mx-auto">
      {/* Walmart Header */}
      <div className="border-b pb-3 mb-4">
        <div className="text-xs text-blue-600">walmart.com</div>
        <div className="flex items-center space-x-2 mt-1">
          <span className="bg-blue-600 text-white px-2 py-1 text-xs font-bold">Free shipping</span>
          <span className="text-xs text-gray-600">arrives in 2 days</span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="bg-gray-50 aspect-square rounded-lg flex items-center justify-center">
            <div className="text-center text-gray-400">
              <div className="text-4xl mb-2">📦</div>
              <div className="text-sm">Product Image</div>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h1 className="text-xl font-semibold text-gray-900">
            {listing.title}
          </h1>
          
          <div className="flex items-center space-x-2">
            <div className="flex items-center">
              {[1,2,3,4,5].map(i => (
                <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
              ))}
            </div>
            <span className="text-gray-600 text-sm">(127)</span>
          </div>

          <div className="space-y-1">
            <div className="flex items-baseline space-x-2">
              <span className="text-3xl font-semibold">${listing.product?.price || '29.98'}</span>
              <span className="text-lg text-gray-500 line-through">$39.98</span>
            </div>
            <div className="text-sm text-green-600">Save $10.00</div>
          </div>

          <div className="bg-blue-50 p-3 rounded">
            <div className="text-sm font-medium text-blue-900">Key Features:</div>
            <div className="text-sm text-blue-800 mt-1">
              {listing.walmart_key_features?.split('\n').slice(0, 3).map((feature, i) => (
                <div key={i}>• {feature}</div>
              ))}
            </div>
          </div>

          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded text-sm font-medium">
            Add to cart
          </button>
        </div>
      </div>
    </div>
  );

  const renderEtsyPreview = () => (
    <div className="bg-white border rounded-lg p-4 max-w-4xl mx-auto">
      {/* Etsy Header */}
      <div className="border-b pb-3 mb-4">
        <div className="text-xs text-orange-600">etsy.com</div>
        <div className="flex items-center space-x-2 mt-1">
          <span className="bg-orange-100 text-orange-700 px-2 py-1 text-xs rounded-full">Handmade</span>
          <span className="bg-green-100 text-green-700 px-2 py-1 text-xs rounded-full">Ready to ship</span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="bg-gray-50 aspect-square rounded-lg flex items-center justify-center">
            <div className="text-center text-gray-400">
              <div className="text-4xl mb-2">🎨</div>
              <div className="text-sm">Handmade Item</div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm">
            <Heart className="w-4 h-4" />
            <span>Add to favorites</span>
          </div>
        </div>

        <div className="space-y-4">
          <h1 className="text-xl font-medium text-gray-900 leading-tight">
            {listing.title}
          </h1>
          
          <div className="flex items-center space-x-3">
            <div className="flex items-center">
              {[1,2,3,4,5].map(i => (
                <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
              ))}
            </div>
            <span className="text-gray-600 text-sm">(89 reviews)</span>
          </div>

          <div className="space-y-2">
            <div className="text-2xl font-semibold">${listing.product?.price || '45.00'}</div>
            <div className="text-sm text-gray-600">FREE shipping to United States</div>
          </div>

          <div className="space-y-3">
            <div className="text-sm">
              <span className="font-medium">Materials:</span>
              <span className="ml-1 text-gray-600">{listing.etsy_materials || 'Sterling silver, natural stones'}</span>
            </div>
            
            <div className="text-sm">
              <span className="font-medium">Ships from:</span>
              <span className="ml-1 text-gray-600">United States</span>
            </div>
          </div>

          <button className="w-full bg-black text-white py-3 px-6 rounded text-sm font-medium hover:bg-gray-800">
            Add to cart
          </button>

          <div className="text-xs text-gray-500 space-y-1">
            <div>• Handmade with love</div>
            <div>• 30-day return policy</div>
            <div>• Ships in 1-2 business days</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTikTokPreview = () => (
    <div className="bg-black text-white rounded-lg p-4 max-w-sm mx-auto">
      {/* TikTok Mobile Interface */}
      <div className="space-y-4">
        {/* Video Area */}
        <div className="bg-gray-800 aspect-[9/16] rounded-lg flex flex-col justify-between p-4 relative">
          <div className="text-center text-gray-400 flex-1 flex items-center justify-center">
            <div>
              <div className="text-3xl mb-2">📱</div>
              <div className="text-sm">Video Preview</div>
            </div>
          </div>
          
          {/* TikTok UI Elements */}
          <div className="absolute right-3 bottom-20 space-y-4">
            <div className="text-center">
              <Heart className="w-8 h-8 mx-auto mb-1" />
              <div className="text-xs">127K</div>
            </div>
            <div className="text-center">
              <Share2 className="w-8 h-8 mx-auto mb-1" />
              <div className="text-xs">1.2K</div>
            </div>
            <div className="text-center">
              <ShoppingCart className="w-8 h-8 mx-auto mb-1 text-yellow-400" />
              <div className="text-xs">Shop</div>
            </div>
          </div>
        </div>

        {/* Product Info */}
        <div className="bg-gray-900 rounded-lg p-3 space-y-2">
          <h3 className="font-medium text-sm">{listing.title}</h3>
          <div className="text-yellow-400 font-bold">${listing.product?.price || '29.99'}</div>
          <div className="text-xs text-gray-300">⭐ 4.8 (2.1K reviews)</div>
          
          <button className="w-full bg-pink-600 text-white py-2 rounded text-sm font-medium">
            Add to Cart
          </button>
          
          <div className="text-xs text-gray-400">
            {listing.tiktok_hashtags?.split(' ').slice(0, 3).join(' ')}
          </div>
        </div>
      </div>
    </div>
  );

  const renderShopifyPreview = () => (
    <div className="bg-white border rounded-lg p-4 max-w-4xl mx-auto">
      {/* Shopify Store Header */}
      <div className="border-b pb-3 mb-4">
        <div className="text-xs text-green-600">{listing.product?.brand_name?.toLowerCase() || 'yourstore'}.com</div>
        <div className="flex items-center space-x-2 mt-1">
          <span className="bg-green-100 text-green-700 px-2 py-1 text-xs rounded">Secure checkout</span>
          <span className="text-xs text-gray-600">Free shipping over $50</span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <div className="space-y-4">
          <div className="bg-gray-50 aspect-square rounded-lg flex items-center justify-center">
            <div className="text-center text-gray-400">
              <div className="text-4xl mb-2">🛍️</div>
              <div className="text-sm">Product Gallery</div>
            </div>
          </div>
          
          <div className="grid grid-cols-4 gap-2">
            {[1,2,3,4].map(i => (
              <div key={i} className="aspect-square bg-gray-100 rounded border"></div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900 mb-2">
              {listing.shopify_seo_title || listing.title}
            </h1>
            <div className="flex items-center space-x-3">
              <div className="flex items-center">
                {[1,2,3,4,5].map(i => (
                  <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                ))}
              </div>
              <span className="text-sm text-gray-600">(94 reviews)</span>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex items-baseline space-x-3">
              <span className="text-3xl font-bold text-gray-900">${listing.product?.price || '49.99'}</span>
              <span className="text-lg text-gray-500 line-through">$69.99</span>
              <span className="bg-red-100 text-red-700 px-2 py-1 text-sm rounded">30% OFF</span>
            </div>
            <div className="text-sm text-green-600">✓ In stock - Ready to ship</div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Quantity:</label>
              <input type="number" defaultValue="1" className="w-20 p-2 border rounded" />
            </div>
            
            <div className="space-y-2">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded text-sm font-medium">
                Add to Cart
              </button>
              <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 py-3 px-6 rounded text-sm font-medium">
                Buy it now
              </button>
            </div>
          </div>

          <div className="border-t pt-4 space-y-2">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <span>🚚</span>
              <span>Free shipping on orders over $50</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <span>↩️</span>
              <span>30-day returns</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <span>🛡️</span>
              <span>Secure checkout</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const previewComponents = {
    amazon: renderAmazonPreview,
    walmart: renderWalmartPreview,
    etsy: renderEtsyPreview,
    tiktok: renderTikTokPreview,
    shopify: renderShopifyPreview
  };

  const PreviewComponent = previewComponents[platform] || (() => <div>Preview not available</div>);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Platform Preview</h3>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Eye className="w-4 h-4" />
          <span>How it looks on {platform}</span>
        </div>
      </div>
      
      <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
        <PreviewComponent />
      </div>
    </div>
  );
};

export default PlatformPreview;
import React, { useState, useEffect } from 'react';

const WalmartDebugTest = ({ listingId = 1479 }) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/listings/generated/${listingId}/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        console.log('🔍 Raw API Data:', result);
        setData(result);
      } catch (err) {
        setError(err.message);
        console.error('❌ API Error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [listingId]);

  if (loading) return <div className="p-4">Loading debug test...</div>;
  if (error) return <div className="p-4 bg-red-100 text-red-800">Error: {error}</div>;
  if (!data) return <div className="p-4">No data received</div>;

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold mb-4">🔧 Walmart Enhanced Sections Debug Test</h1>
      
      {/* Raw Data Debug */}
      <div className="bg-gray-100 p-4 rounded">
        <h2 className="font-bold mb-2">📊 API Data Status</h2>
        <div className="text-sm space-y-1">
          <div>Platform: <code>{data.platform}</code></div>
          <div>Status: <code>{data.status}</code></div>
          <div>Total fields: <code>{Object.keys(data).length}</code></div>
          <div>Walmart fields: <code>{Object.keys(data).filter(k => k.startsWith('walmart_')).length}</code></div>
        </div>
      </div>

      {/* Enhanced Sections Test */}
      <div className="space-y-4">
        <h2 className="font-bold">🧪 Enhanced Sections Raw Test</h2>
        
        {/* Compliance Guidance Test */}
        <div className="border border-gray-300 rounded p-4">
          <h3 className="font-semibold mb-2">1. Compliance Guidance Field</h3>
          {data.walmart_compliance_certifications ? (
            <div className="space-y-2">
              <div className="text-green-600 font-medium">✅ Field EXISTS</div>
              <div className="text-sm">Length: {data.walmart_compliance_certifications.length} characters</div>
              <div className="bg-gray-50 p-2 rounded text-xs">
                <strong>Raw content:</strong><br/>
                {data.walmart_compliance_certifications.substring(0, 300)}...
              </div>
              
              {/* Try to parse and render */}
              {(() => {
                try {
                  const compliance = JSON.parse(data.walmart_compliance_certifications);
                  return (
                    <div className="bg-green-50 border border-green-200 rounded p-3 mt-3">
                      <div className="text-sm font-semibold text-green-900 mb-2">📋 Compliance Guidance (WORKING!)</div>
                      <div className="text-xs text-green-800 space-y-1">
                        {compliance.required_certifications && (
                          <div><strong>Certifications:</strong> {compliance.required_certifications.join(', ')}</div>
                        )}
                        {compliance.certification_guidance && (
                          <div><strong>How to get certified:</strong> {compliance.certification_guidance}</div>
                        )}
                        {compliance.regulatory_requirements && (
                          <div><strong>Regulatory:</strong> {compliance.regulatory_requirements}</div>
                        )}
                      </div>
                    </div>
                  );
                } catch (parseError) {
                  return (
                    <div className="bg-red-50 border border-red-200 rounded p-3 mt-3">
                      <div className="text-red-800">❌ JSON Parse Error: {parseError.message}</div>
                    </div>
                  );
                }
              })()}
            </div>
          ) : (
            <div className="text-red-600 font-medium">❌ Field MISSING or EMPTY</div>
          )}
        </div>

        {/* Profit Maximizer Test */}
        <div className="border border-gray-300 rounded p-4">
          <h3 className="font-semibold mb-2">2. Profit Maximizer Field</h3>
          {data.walmart_profit_maximizer ? (
            <div className="space-y-2">
              <div className="text-green-600 font-medium">✅ Field EXISTS</div>
              <div className="text-sm">Length: {data.walmart_profit_maximizer.length} characters</div>
              <div className="bg-gray-50 p-2 rounded text-xs">
                <strong>Raw content:</strong><br/>
                {data.walmart_profit_maximizer.substring(0, 300)}...
              </div>
              
              {/* Try to parse and render */}
              {(() => {
                try {
                  const profit = JSON.parse(data.walmart_profit_maximizer);
                  return (
                    <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mt-3">
                      <div className="text-sm font-semibold text-yellow-900 mb-2">💰 Profit Maximizer (WORKING!)</div>
                      <div className="text-xs text-yellow-800 space-y-1">
                        {profit.seasonal_pricing_strategy && (
                          <div><strong>Pricing Strategy:</strong> {profit.seasonal_pricing_strategy}</div>
                        )}
                        {profit.competitor_price_monitoring && (
                          <div><strong>Competitor Monitoring:</strong> {profit.competitor_price_monitoring}</div>
                        )}
                        {profit.inventory_optimization && (
                          <div><strong>Inventory Tips:</strong> {profit.inventory_optimization}</div>
                        )}
                        {profit.advertising_roi_blueprint && (
                          <div><strong>Ad ROI:</strong> {profit.advertising_roi_blueprint}</div>
                        )}
                      </div>
                    </div>
                  );
                } catch (parseError) {
                  return (
                    <div className="bg-red-50 border border-red-200 rounded p-3 mt-3">
                      <div className="text-red-800">❌ JSON Parse Error: {parseError.message}</div>
                    </div>
                  );
                }
              })()}
            </div>
          ) : (
            <div className="text-red-600 font-medium">❌ Field MISSING or EMPTY</div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded p-4">
        <h3 className="font-semibold text-blue-900 mb-2">📋 Test Results</h3>
        <div className="text-blue-800 text-sm">
          <p>If you see green "WORKING!" boxes above, then the enhanced sections are functional.</p>
          <p>If you don't see them in the main Preview tab, there's a component integration issue.</p>
        </div>
      </div>
    </div>
  );
};

export default WalmartDebugTest;
import React, { useState, useEffect } from 'react';
import { listingAPI } from '../services/api';

const WalmartEnhancedTest = () => {
  const [listing, setListing] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchListing = async () => {
      try {
        console.log('=== WALMART ENHANCED TEST ===');
        const response = await listingAPI.get(1481);
        const data = response.data;
        console.log('Raw API Response:', data);
        
        console.log('Platform:', data.platform);
        console.log('walmart_compliance_certifications exists:', !!data.walmart_compliance_certifications);
        console.log('walmart_profit_maximizer exists:', !!data.walmart_profit_maximizer);
        
        if (data.walmart_compliance_certifications) {
          console.log('Compliance raw data:', data.walmart_compliance_certifications);
          try {
            const parsed = JSON.parse(data.walmart_compliance_certifications);
            console.log('Compliance parsed:', parsed);
          } catch (e) {
            console.log('Compliance parse error:', e);
          }
        }
        
        if (data.walmart_profit_maximizer) {
          console.log('Profit raw data:', data.walmart_profit_maximizer);
          try {
            const parsed = JSON.parse(data.walmart_profit_maximizer);
            console.log('Profit parsed:', parsed);
          } catch (e) {
            console.log('Profit parse error:', e);
          }
        }
        
        setListing(data);
      } catch (err) {
        console.error('API Error:', err);
        setError(err.message);
      }
    };

    fetchListing();
  }, []);

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <strong>Error:</strong> {error}
      </div>
    );
  }

  if (!listing) {
    return <div>Loading test data...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded">
        <h2 className="font-bold mb-2">Walmart Enhanced Sections Test</h2>
        <p>Listing ID: {listing.id}</p>
        <p>Platform: {listing.platform}</p>
      </div>

      {/* Test Compliance Section */}
      <div className="bg-green-50 border border-green-200 rounded p-3">
        <h3 className="text-sm font-semibold text-green-900 mb-2">📋 Compliance Guidance Test</h3>
        <div className="text-xs text-green-800">
          <p>Data exists: {listing.walmart_compliance_certifications ? 'YES' : 'NO'}</p>
          <p>Data length: {listing.walmart_compliance_certifications ? listing.walmart_compliance_certifications.length : 0} chars</p>
          
          {listing.walmart_compliance_certifications ? (
            (() => {
              try {
                const compliance = JSON.parse(listing.walmart_compliance_certifications);
                return (
                  <div className="space-y-1 mt-2">
                    <p><strong>Type:</strong> {typeof compliance}</p>
                    <p><strong>Keys:</strong> {Object.keys(compliance).join(', ')}</p>
                    {compliance.required_certifications && (
                      <p><strong>Certifications:</strong> {compliance.required_certifications.join(', ')}</p>
                    )}
                    {compliance.certification_guidance && (
                      <p><strong>Guidance:</strong> {compliance.certification_guidance.substring(0, 100)}...</p>
                    )}
                  </div>
                );
              } catch (e) {
                return <p className="text-red-600">JSON Parse Error: {e.message}</p>;
              }
            })()
          ) : (
            <p className="text-red-600">No compliance data available</p>
          )}
        </div>
      </div>

      {/* Test Profit Section */}
      <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
        <h3 className="text-sm font-semibold text-yellow-900 mb-2">💰 Profit Maximizer Test</h3>
        <div className="text-xs text-yellow-800">
          <p>Data exists: {listing.walmart_profit_maximizer ? 'YES' : 'NO'}</p>
          <p>Data length: {listing.walmart_profit_maximizer ? listing.walmart_profit_maximizer.length : 0} chars</p>
          
          {listing.walmart_profit_maximizer ? (
            (() => {
              try {
                const profit = JSON.parse(listing.walmart_profit_maximizer);
                return (
                  <div className="space-y-1 mt-2">
                    <p><strong>Type:</strong> {typeof profit}</p>
                    <p><strong>Keys:</strong> {Object.keys(profit).join(', ')}</p>
                    {profit.seasonal_pricing_strategy && (
                      <p><strong>Pricing:</strong> {profit.seasonal_pricing_strategy.substring(0, 100)}...</p>
                    )}
                    {profit.inventory_optimization && (
                      <p><strong>Inventory:</strong> {profit.inventory_optimization.substring(0, 100)}...</p>
                    )}
                  </div>
                );
              } catch (e) {
                return <p className="text-red-600">JSON Parse Error: {e.message}</p>;
              }
            })()
          ) : (
            <p className="text-red-600">No profit data available</p>
          )}
        </div>
      </div>

      {/* Raw Data Display */}
      <div className="bg-gray-100 border border-gray-300 rounded p-3">
        <h3 className="text-sm font-semibold text-gray-900 mb-2">Raw JSON Data Preview</h3>
        <div className="text-xs font-mono bg-white p-2 rounded border overflow-auto max-h-32">
          <p><strong>Compliance:</strong> {listing.walmart_compliance_certifications}</p>
          <br />
          <p><strong>Profit:</strong> {listing.walmart_profit_maximizer}</p>
        </div>
      </div>
    </div>
  );
};

export default WalmartEnhancedTest;
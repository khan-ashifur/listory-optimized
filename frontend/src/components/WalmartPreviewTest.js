import React from 'react';

const WalmartPreviewTest = ({ listing }) => {
  console.log('=== WALMART PREVIEW TEST DEBUG ===');
  console.log('Listing object:', listing);
  console.log('walmart_compliance_certifications:', listing?.walmart_compliance_certifications);
  console.log('walmart_profit_maximizer:', listing?.walmart_profit_maximizer);
  console.log('Platform:', listing?.platform);

  if (!listing) {
    return <div>No listing data</div>;
  }

  // Test the compliance section logic
  const complianceExists = !!listing.walmart_compliance_certifications;
  const profitExists = !!listing.walmart_profit_maximizer;
  
  console.log('Compliance exists:', complianceExists);
  console.log('Profit exists:', profitExists);

  return (
    <div className="bg-white border rounded-lg p-4">
      <h2 className="text-lg font-bold mb-4">Walmart Preview Test</h2>
      
      <div className="mb-4">
        <h3 className="font-semibold">Debug Info:</h3>
        <p>Platform: {listing.platform}</p>
        <p>Compliance data exists: {complianceExists ? 'YES' : 'NO'}</p>
        <p>Profit data exists: {profitExists ? 'YES' : 'NO'}</p>
      </div>

      {/* Force render compliance section */}
      <div className="mb-4">
        <h3 className="font-semibold">Forced Compliance Section:</h3>
        {listing.walmart_compliance_certifications ? (
          <div className="bg-green-50 border border-green-200 rounded p-3">
            <div className="text-sm font-semibold text-green-900 mb-2">📋 Compliance Guidance</div>
            <div className="text-xs text-green-800">
              {(() => {
                try {
                  const compliance = JSON.parse(listing.walmart_compliance_certifications);
                  return (
                    <div className="space-y-1">
                      <div>Raw data: {JSON.stringify(compliance, null, 2)}</div>
                      {compliance.required_certifications && (
                        <div><span className="font-medium">Certifications:</span> {compliance.required_certifications.join(', ')}</div>
                      )}
                      {compliance.certification_guidance && (
                        <div><span className="font-medium">How to get certified:</span> {compliance.certification_guidance.substring(0, 100)}...</div>
                      )}
                    </div>
                  );
                } catch (error) {
                  return <div>Error parsing: {error.message}</div>;
                }
              })()}
            </div>
          </div>
        ) : (
          <div className="bg-red-50 border border-red-200 rounded p-3">
            <div className="text-red-800">No compliance data found</div>
          </div>
        )}
      </div>

      {/* Force render profit section */}
      <div className="mb-4">
        <h3 className="font-semibold">Forced Profit Section:</h3>
        {listing.walmart_profit_maximizer ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
            <div className="text-sm font-semibold text-yellow-900 mb-2">💰 Profit Maximizer (WOW!)</div>
            <div className="text-xs text-yellow-800">
              {(() => {
                try {
                  const profit = JSON.parse(listing.walmart_profit_maximizer);
                  return (
                    <div className="space-y-1">
                      <div>Raw data: {JSON.stringify(profit, null, 2)}</div>
                      {profit.seasonal_pricing_strategy && (
                        <div><span className="font-medium">Pricing Strategy:</span> {profit.seasonal_pricing_strategy.substring(0, 80)}...</div>
                      )}
                      {profit.inventory_optimization && (
                        <div><span className="font-medium">Inventory Tips:</span> {profit.inventory_optimization.substring(0, 80)}...</div>
                      )}
                      <div className="text-yellow-600 font-medium">+ Competitor monitoring & Ad ROI blueprint</div>
                    </div>
                  );
                } catch (error) {
                  return <div>Error parsing: {error.message}</div>;
                }
              })()}
            </div>
          </div>
        ) : (
          <div className="bg-red-50 border border-red-200 rounded p-3">
            <div className="text-red-800">No profit data found</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default WalmartPreviewTest;
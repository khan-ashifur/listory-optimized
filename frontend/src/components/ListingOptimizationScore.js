import React from 'react';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';

const ListingOptimizationScore = ({ listing }) => {
  if (!listing) return null;

  const checks = [
    {
      name: 'Title Length',
      status: listing.title && listing.title.length <= 150 ? 'good' : 'warning',
      message: listing.title ? `${listing.title.length}/150 characters` : 'No title',
      details: 'Keep under 150 characters for mobile display'
    },
    {
      name: 'Bullet Points',
      status: listing.bullet_points && listing.bullet_points.includes('🔥') && listing.bullet_points.includes('**') ? 'good' : 'warning',
      message: listing.bullet_points ? 'Emotional format detected' : 'No bullet points',
      details: 'Emojis + **Bold Feature**: Transformation benefit format'
    },
    {
      name: 'Description Structure',
      status: listing.long_description && listing.long_description.includes('<h3>') ? 'good' : 'warning',
      message: listing.long_description ? 'HTML structure found' : 'No description',
      details: 'Should have emotional hooks and structured content'
    },
    {
      name: 'A+ Content',
      status: listing.amazon_aplus_content && listing.amazon_aplus_content.includes('Module') ? 'good' : 'warning',
      message: listing.amazon_aplus_content ? 'Module suggestions provided' : 'No A+ content',
      details: 'Specific module headlines with actionable suggestions'
    },
    {
      name: 'Keyword Optimization',
      status: (() => {
        if (!listing.keywords) return 'warning';
        const keywordString = typeof listing.keywords === 'string' ? listing.keywords : '';
        return keywordString && keywordString.split(',').length >= 5 ? 'good' : 'warning';
      })(),
      message: (() => {
        if (!listing.keywords) return 'No keywords';
        const keywordString = typeof listing.keywords === 'string' ? listing.keywords : '';
        const keywordCount = keywordString ? keywordString.split(',').length : 0;
        return keywordCount > 0 ? `${keywordCount} keywords` : 'No keywords';
      })(),
      details: 'Mix of short and long-tail keywords for better coverage'
    },
    {
      name: 'Conversion Boosters',
      status: listing.short_description && listing.short_description.includes('📦') && listing.short_description.includes('❓') ? 'good' : 'warning',
      message: listing.short_description ? 'Sales tools included' : 'No conversion tools',
      details: 'Should include: What\'s in box, FAQs, trust builders, social proof'
    }
  ];

  const goodCount = checks.filter(check => check.status === 'good').length;
  const overallScore = Math.round((goodCount / checks.length) * 100);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'good':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-400" />;
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white border rounded-lg p-6 shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">
          Amazon Optimization Score
        </h3>
        <div className={`text-3xl font-bold ${getScoreColor(overallScore)}`}>
          {overallScore}%
        </div>
      </div>

      <div className="space-y-4">
        {checks.map((check, index) => (
          <div key={index} className="flex items-start space-x-3">
            {getStatusIcon(check.status)}
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-gray-900">
                  {check.name}
                </p>
                <span className="text-sm text-gray-500">
                  {check.message}
                </span>
              </div>
              <p className="text-xs text-gray-600 mt-1">
                {check.details}
              </p>
            </div>
          </div>
        ))}
      </div>

      {overallScore < 80 && (
        <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>Optimization Tip:</strong> Your listing could be improved. 
            Focus on the items marked with warnings to boost conversion rates.
          </p>
        </div>
      )}

      {overallScore >= 80 && (
        <div className="mt-6 p-4 bg-green-50 rounded-lg">
          <p className="text-sm text-green-800">
            <strong>Great job!</strong> Your listing follows Amazon best practices 
            and should perform well in search results.
          </p>
        </div>
      )}
    </div>
  );
};

export default ListingOptimizationScore;
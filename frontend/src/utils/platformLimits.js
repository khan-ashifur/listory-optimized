export const PLATFORM_LIMITS = {
  amazon: {
    title: { max: 200, optimal: 150 },
    bulletPoints: { max: 255, count: 5 },
    description: { max: 2000, optimal: 1500 },
    backendKeywords: { max: 250 }
  },
  walmart: {
    title: { max: 75, optimal: 65 },
    shortDescription: { max: 4000, optimal: 3000 },
    keyFeatures: { max: 1000, count: 10 }
  },
  etsy: {
    title: { max: 140, optimal: 120 },
    description: { max: 13000, optimal: 8000 },
    tags: { count: 13, maxLength: 20 }
  },
  tiktok: {
    title: { max: 60, optimal: 50 },
    description: { max: 3000, optimal: 2000 },
    hashtags: { count: 30, maxLength: 100 }
  },
  shopify: {
    seoTitle: { max: 60, optimal: 55 },
    metaDescription: { max: 160, optimal: 150 },
    productDescription: { max: 5000, optimal: 3000 }
  }
};

export const validateContent = (platform, field, content) => {
  const limits = PLATFORM_LIMITS[platform];
  if (!limits || !limits[field]) return { valid: true, warnings: [] };

  const warnings = [];
  const length = content.length;
  const limit = limits[field];

  if (limit.max && length > limit.max) {
    warnings.push(`Exceeds maximum length (${length}/${limit.max} characters)`);
  }

  if (limit.optimal && length > limit.optimal) {
    warnings.push(`Consider shortening for optimal performance (${length}/${limit.optimal} characters)`);
  }

  if (limit.count) {
    const items = content.split('\n').filter(item => item.trim());
    if (items.length > limit.count) {
      warnings.push(`Too many items (${items.length}/${limit.count} maximum)`);
    }
  }

  return {
    valid: warnings.length === 0,
    warnings,
    length,
    maxLength: limit.max,
    optimalLength: limit.optimal
  };
};

export const getPlatformRequirements = (platform) => {
  const requirements = {
    amazon: {
      title: 'Include main keyword at beginning, stay under 200 characters',
      bulletPoints: '5 benefit-focused bullets, each under 255 characters',
      description: 'Story-driven content with HTML formatting, 1500-2000 characters',
      keywords: 'Backend keywords under 250 bytes, no repetition'
    },
    walmart: {
      title: 'Brand + product + key feature, under 75 characters',
      description: 'Rich HTML content highlighting key features and benefits',
      specifications: 'Detailed product specs with measurements and materials'
    },
    etsy: {
      title: '13 keywords naturally integrated, under 140 characters',
      description: 'Personal story-driven content mentioning materials and process',
      tags: 'Exactly 13 relevant tags, each under 20 characters'
    },
    tiktok: {
      title: 'Catchy and trending language, under 60 characters',
      description: 'Casual, emoji-rich content that speaks to Gen Z',
      hashtags: 'Mix of trending and niche hashtags, up to 30 tags'
    },
    shopify: {
      seoTitle: 'Keyword-optimized for Google, under 60 characters',
      metaDescription: 'Compelling with CTA, under 160 characters',
      description: 'HTML-formatted, conversion-focused content'
    }
  };

  return requirements[platform] || {};
};
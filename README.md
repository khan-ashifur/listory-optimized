# 🚀 Listory - AI-Powered Product Listings

**Listory** is a full-stack SaaS platform that helps sellers generate high-converting product listings for multiple e-commerce platforms using AI.

## 🛍️ Supported Platforms

- **Amazon** - Complete listings with A+ content, SEO keywords, bullet points
- **Walmart** - Marketplace-optimized descriptions with specifications  
- **Etsy** - Story-driven listings with SEO tags and materials
- **TikTok Shop** - Viral-ready content with video script ideas
- **Shopify** - Conversion-focused product pages with SEO optimization

## ✨ Features

### 🎯 AI-Powered Content Generation
- **Amazon**: A+ content suggestions, backend keywords, optimized titles, bullet points
- **Walmart**: Rich descriptions, key features, product specifications
- **Etsy**: 13 SEO tags, materials list, story-driven copy
- **TikTok**: Video script ideas, trending hashtags, hooks for Gen Z
- **Shopify**: SEO titles, meta descriptions, HTML formatting

### 📊 User Experience
- Modern, responsive UI built with React & Tailwind CSS
- Platform selection with visual cards
- Comprehensive product input forms
- Real-time listing generation
- Copy-to-clipboard functionality
- Download options for all content

### 🔧 Technical Features
- Django REST API backend
- React frontend with modern UI/UX
- OpenAI integration for content generation
- User authentication & subscription management
- Credit-based usage system
- Admin dashboard for management

## 🏗️ Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **OpenAI API** - Content generation
- **SQLite/PostgreSQL** - Database
- **Celery & Redis** - Background tasks (optional)

### Frontend
- **React 18** - Frontend framework
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Axios** - HTTP client
- **React Router** - Navigation
- **Lucide React** - Icons

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. **Clone and setup backend:**
   ```bash
   cd backend
   pip install -r ../requirements.txt
   ```

2. **Environment setup:**
   ```bash
   cp ../.env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Database setup:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run backend:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```

Visit `http://localhost:3000` to see the application!

## 📱 User Flow

1. **Platform Selection** - Choose from Amazon, Walmart, Etsy, TikTok, or Shopify
2. **Product Details** - Enter product information, brand details, competitor URLs
3. **AI Generation** - Advanced AI creates optimized listings
4. **Review & Copy** - Review generated content and copy to clipboard
5. **Multi-format Output** - Get platform-specific optimizations

## 🎨 Key Components

### Landing Page (`frontend/src/pages/LandingPage.js`)
- Hero section with value proposition
- Interactive platform selection cards
- Feature highlights and benefits

### Product Form (`frontend/src/pages/ProductForm.js`)  
- Comprehensive input form for product details
- Brand tone selection
- Competitor analysis input
- Real-time validation

### Results Display (`frontend/src/pages/ListingResults.js`)
- Tabbed interface for different content types
- Copy-to-clipboard functionality
- Platform-specific optimizations
- Export options

### Django Models (`backend/apps/`)
- **Product** - Core product information
- **GeneratedListing** - AI-generated content
- **UserProfile** - Subscription & credits management

## 🔑 API Endpoints

```
GET  /api/core/products/platforms/     - Available platforms
GET  /api/core/products/brand_tones/   - Brand tone options
POST /api/core/products/               - Create product
POST /api/listings/generate/{id}/{platform}/ - Generate listing
GET  /api/listings/generated/          - User's listings
GET  /api/auth/profile/                - User profile
```

## 🎯 Platform-Specific Features

### Amazon
- A+ content suggestions with HTML structure
- Backend search keywords for SEO
- Optimized bullet points for conversions
- Character-limited titles for compliance

### TikTok Shop
- 15-30 second video script ideas
- Trending hashtag recommendations
- Gen Z-focused copy and hooks
- Viral content suggestions

### Etsy
- Story-driven, personal product descriptions
- 13 SEO-optimized tags for discoverability
- Materials and crafting information
- Handmade/unique selling propositions

### Walmart & Shopify
- Technical specifications and features
- SEO-optimized meta descriptions
- HTML-formatted rich content
- Conversion-focused copy

## 📈 Business Model

- **Free Tier**: 3 free listings
- **Basic Plan**: 50 listings/month
- **Pro Plan**: 200 listings/month  
- **Enterprise**: Unlimited with API access

## 🔧 Development

### Adding New Platforms
1. Add platform choice in `Product.PLATFORMS`
2. Create generation method in `ListingGeneratorService`
3. Add platform-specific fields to `GeneratedListing`
4. Update frontend platform selector

### Customizing AI Prompts
Edit the prompt templates in `backend/apps/listings/services.py` to adjust the AI-generated content style and structure.

## 📝 Environment Variables

```bash
SECRET_KEY=your-django-secret-key
OPENAI_API_KEY=your-openai-api-key  
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0  # Optional
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for e-commerce sellers worldwide**
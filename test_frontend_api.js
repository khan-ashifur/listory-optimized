// Test script to simulate frontend API call and data processing
const axios = require('axios');

async function testFrontendAPI() {
    try {
        console.log('=== TESTING FRONTEND API CALL ===');
        
        // Simulate the exact API call the frontend makes
        const response = await axios.get('http://localhost:8000/api/listings/generated/1479/');
        const data = response.data;
        
        console.log('API Response Status:', response.status);
        console.log('Platform:', data.platform);
        
        // Test the conditional logic from the component
        console.log('\n=== TESTING CONDITIONAL LOGIC ===');
        console.log('walmart_compliance_certifications exists:', !!data.walmart_compliance_certifications);
        console.log('walmart_profit_maximizer exists:', !!data.walmart_profit_maximizer);
        
        if (data.walmart_compliance_certifications) {
            console.log('\n=== COMPLIANCE DATA ===');
            console.log('Type:', typeof data.walmart_compliance_certifications);
            console.log('Value:', data.walmart_compliance_certifications);
            
            try {
                const compliance = JSON.parse(data.walmart_compliance_certifications);
                console.log('Parsed successfully:', compliance);
                console.log('Has required_certifications:', !!compliance.required_certifications);
                console.log('Has certification_guidance:', !!compliance.certification_guidance);
            } catch (error) {
                console.log('Parse error:', error.message);
            }
        }
        
        if (data.walmart_profit_maximizer) {
            console.log('\n=== PROFIT DATA ===');
            console.log('Type:', typeof data.walmart_profit_maximizer);
            console.log('Value:', data.walmart_profit_maximizer);
            
            try {
                const profit = JSON.parse(data.walmart_profit_maximizer);
                console.log('Parsed successfully:', profit);
                console.log('Has seasonal_pricing_strategy:', !!profit.seasonal_pricing_strategy);
                console.log('Has inventory_optimization:', !!profit.inventory_optimization);
            } catch (error) {
                console.log('Parse error:', error.message);
            }
        }
        
        console.log('\n=== CONCLUSION ===');
        if (data.walmart_compliance_certifications && data.walmart_profit_maximizer) {
            console.log('✅ Both enhanced sections should render in frontend');
        } else {
            console.log('❌ Missing enhanced sections data');
        }
        
    } catch (error) {
        console.error('❌ API Error:', error.message);
    }
}

testFrontendAPI();
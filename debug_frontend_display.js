// Debug script to check frontend data structure
// Open browser console and paste this to debug

console.log("🔍 DEBUGGING FRONTEND A+ CONTENT DISPLAY");
console.log("="*50);

// Check if we're on the results page
const currentUrl = window.location.href;
console.log("Current URL:", currentUrl);

// Check if listing data exists in React state/props
// This will help us see what data the frontend actually has
setTimeout(() => {
    // Try to find React component data
    const reactFiber = document.querySelector('[data-reactroot]')?._reactInternalFiber ||
                      document.querySelector('#root')?._reactInternalFiber;
    
    if (reactFiber) {
        console.log("✅ React detected");
        
        // Look for listing data in React DevTools
        console.log("📋 Checking for listing data...");
        
        // Check if currentListing exists
        const listingElements = document.querySelectorAll('[class*="listing"], [class*="aplus"]');
        console.log("Listing related elements found:", listingElements.length);
        
        // Check for A+ content specifically
        const aplusElements = document.querySelectorAll('[class*="aplus"]');
        console.log("A+ content elements found:", aplusElements.length);
        
        // Check tab buttons
        const tabButtons = document.querySelectorAll('button');
        const aplusTab = Array.from(tabButtons).find(btn => 
            btn.textContent.includes('A+ Content') || 
            btn.textContent.includes('aplus')
        );
        
        if (aplusTab) {
            console.log("✅ A+ Content tab found:", aplusTab);
            console.log("   Tab text:", aplusTab.textContent);
            console.log("   Tab classes:", aplusTab.className);
            console.log("   Tab disabled:", aplusTab.disabled);
            
            // Try clicking it
            console.log("🖱️ Attempting to click A+ Content tab...");
            aplusTab.click();
            
            setTimeout(() => {
                // Check what shows after clicking
                const aplusContent = document.querySelector('[class*="aplus"]');
                if (aplusContent) {
                    console.log("✅ A+ content area found after click:", aplusContent);
                    console.log("   Content length:", aplusContent.textContent.length);
                    console.log("   Content preview:", aplusContent.textContent.substring(0, 200));
                } else {
                    console.log("❌ No A+ content area found after click");
                }
            }, 500);
            
        } else {
            console.log("❌ A+ Content tab not found");
            console.log("Available tabs:", Array.from(tabButtons).map(btn => btn.textContent));
        }
        
    } else {
        console.log("❌ React not detected");
    }
    
    // Check for specific text content
    const bodyText = document.body.textContent;
    if (bodyText.includes('amazon_aplus_content')) {
        console.log("✅ 'amazon_aplus_content' text found in page");
    } else {
        console.log("❌ 'amazon_aplus_content' text NOT found in page");
    }
    
    if (bodyText.includes('No A+ content generated')) {
        console.log("❌ 'No A+ content generated' message found");
    }
    
}, 1000);

// Also check network requests
console.log("🌐 Monitoring network requests...");
const originalFetch = window.fetch;
window.fetch = function(...args) {
    console.log("📡 Fetch request:", args[0]);
    return originalFetch.apply(this, args).then(response => {
        if (args[0].includes('/listings/generated/')) {
            console.log("📋 Listing API response:", response.status);
            response.clone().json().then(data => {
                console.log("📋 Listing data keys:", Object.keys(data));
                if (data.amazon_aplus_content) {
                    console.log("✅ A+ content in API response:", data.amazon_aplus_content.length, "chars");
                } else {
                    console.log("❌ A+ content missing from API response");
                }
            }).catch(e => console.log("JSON parse error:", e));
        }
        return response;
    });
};